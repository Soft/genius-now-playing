# genius-now-playing 🎧

`genius-now-playing` is a tiny utility for opening currently playing song's
lyrics on [Genius.com](https://genius.com).

## Usage

`genius-now-player` requires a client access token for Genius.com. To get a
token first [register a new application](https://genius.com/api-clients/new) and
select "Generate Access Token".

```
Usage: genius-now-playing [OPTIONS]

Options:
  --client-token TEXT  Genius client token.
  --player TEXT        Media player to use.
  --help               Show this message and exit.
```

Alternatively, client token can be specified using `GENIUS_CLIENT_TOKEN`
environment variable.
