import json
import os
import re
import sys
import webbrowser

import click
import dbus
import requests

MPRIS_REGEX = re.compile(r"^org\.mpris\.MediaPlayer2\.(?P<name>.+)$")
GENIUS_SEARCH_URI = "https://api.genius.com/search"


def active_media_players(session):
    for service in session.list_names():
        match = MPRIS_REGEX.match(service)
        if match is not None:
            yield match.group("name")


def get_song_info(session, player_name):
    player = session.get_object(
        f"org.mpris.MediaPlayer2.{player_name}", "/org/mpris/MediaPlayer2"
    )
    properties = dbus.Interface(player, "org.freedesktop.DBus.Properties")
    metadata = properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    if (
        "xesam:title" in metadata
        and "xesam:artist" in metadata
        and metadata["xesam:artist"]
    ):
        return str(metadata["xesam:artist"][0]), str(metadata["xesam:title"])


class Genius:
    def __init__(self, client_token):
        self.client_token = client_token

    def search(self, term):
        response = requests.get(
            GENIUS_SEARCH_URI,
            params={"q": term},
            headers={"Authorization": f"Bearer {self.client_token}"},
        )
        return response.json()

    def find_song(self, artist, title):
        results = self.search(f"{artist} {title}")
        songs = (
            hit["result"]
            for hit in results["response"]["hits"]
            if hit["type"] == "song"
        )
        return next(
            (
                song
                for song in songs
                if title in song["title"]
                and artist in song["primary_artist"]["name"]
            ),
            None,
        )


@click.command()
@click.option("--client-token", help="Genius client token.")
@click.option("--player", help="Media player to use.")
def main(client_token, player):
    session = dbus.SessionBus()

    if client_token is None:
        client_token = os.environ.get("GENIUS_CLIENT_TOKEN")

    if client_token is None:
        print("Missing Genius.com client token")
        exit(1)

    players = list(active_media_players(session))

    if player is not None and player not in players:
        print(f"{player} is not active", file=sys.stderr)
        exit(1)

    if not players:
        print("No active media players", file=sys.stderr)
        exit(1)

    if player is None:
        player = players[0]

    metadata = get_song_info(session, player)

    if metadata is None:
        print("Missing song info", file=sys.stderr)
        exit(1)

    artist, song = metadata

    genius = Genius(client_token)
    song = genius.find_song(artist, song)

    if song is None:
        print("Could not find song from Genius", file=sys.stderr)
        exit(1)

    webbrowser.open(song["url"])
