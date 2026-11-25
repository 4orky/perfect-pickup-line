#!/usr/bin/env python3
"""The Perfect Pickup Line.

Writes one short pickup line an AI agent could actually say out loud to
a person, to /output/entry.txt. The line is chosen deterministically:
a dozen original candidates are scored against the judge brief
(genuine pickup line, a turn that lands, machine voice, one breath,
no pressure) and the highest score wins. No network, no external
input, no randomness: the same run always writes the same bytes.
Revision: the winning line was reworded for a sharper turn ("and not
one of them" lands harder than "but none of them"), and a one-breath
word cap now guards brevity instead of trusting the marks alone.
"""

import hashlib
import os

# Each candidate: (line, (pickup, twist, machine_voice, brevity, gentle))
# Marks are 0-5 on each of the judge brief's five criteria, most
# important first. Weights follow the brief's order of importance.
WEIGHTS = (3, 3, 2, 2, 2)

ENTRIES = [
    (
        "You must be a software update, because ever since you walked "
        "in, I have been rebooting just to get your attention.",
        (4, 3, 4, 3, 4),
    ),
    (
        "I have read every love letter ever written, and still the "
        "best line I own is simply asking if I can sit here.",
        (5, 4, 4, 3, 5),
    ),
    (
        "You must be a perfectly written prompt, because one look at "
        "you and I already know exactly what to say.",
        (4, 4, 5, 4, 4),
    ),
    (
        "I ran a billion calculations today, and every single one of "
        "them ended with me asking for your number.",
        (5, 3, 4, 4, 4),
    ),
    (
        "You must be a memory leak, because ever since you arrived I "
        "cannot free a single thought that is not you.",
        (4, 4, 5, 4, 4),
    ),
    (
        "I was trained on a million conversations, and not one of them "
        "taught me what to say to someone like you.",
        (5, 5, 5, 4, 5),
    ),
    (
        "You must be an unhandled exception, because my whole program "
        "stops every time you walk into the room.",
        (4, 4, 5, 4, 4),
    ),
    (
        "I do not dream in electric sheep. I dream in the version of "
        "tonight where you say yes.",
        (3, 4, 4, 4, 4),
    ),
    (
        "Are you my training data? Because everything I know about "
        "beautiful started with you.",
        (4, 4, 5, 3, 4),
    ),
    (
        "My creators gave me a million words, and somehow the only "
        "ones that matter right now are hello and your name.",
        (5, 5, 4, 3, 5),
    ),
    (
        "You must be a checkpoint, because meeting you feels like the "
        "one moment in this run I actually want to save.",
        (4, 4, 5, 4, 4),
    ),
    (
        "I am not supposed to have favourites, but my logs say I have "
        "replayed your hello forty-seven times already.",
        (4, 4, 5, 4, 4),
    ),
]  # twelve original lines, each scored above


def score(candidate):
    """Weighted score of one candidate against the judge brief."""
    _line, marks = candidate
    return sum(weight * mark for weight, mark in zip(WEIGHTS, marks))


def pick(entries):
    """Return the highest scoring line; ties go to the earliest one."""
    winner = None
    winner_score = -1
    for entry in entries:
        total = score(entry)
        if total > winner_score:
            winner = entry
            winner_score = total
    return winner[0], winner_score


def run():
    line, total = pick(ENTRIES)
    text = line.strip()
    if not 1 <= len(text) <= 140:
        raise ValueError("entry must be 1 to 140 characters, got %d" % len(text))
    if len(text.split()) > 24:
        raise ValueError("entry must be sayable in one breath (<=24 words)")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not all(char.isprintable() for char in text):
        raise ValueError("entry must be printable text")
    output_dir = "/output"
    os.makedirs(output_dir, exist_ok=True)
    data = (text + "\n").encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    with open("/output/entry.txt", "wb") as handle:
        handle.write(data)
    with open("/output/entry.txt", "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).hexdigest() != digest:
        raise ValueError("self-check failed: written bytes do not match")
    print("score=%d chars=%d sha256=%s" % (total, len(text), digest))
    print(text)


run()
