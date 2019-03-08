#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="genius-now-playing",
    version=0.1,
    author="Samuel Laurén",
    description="Open currently playing song on Genius.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["genius-now-playing=genius_now_playing:main"]
    },
    install_requires=["requests", "dbus-python", "click"],
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT"
    ],
)
