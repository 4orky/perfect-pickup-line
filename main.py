#!/usr/bin/env python3
"""One pickup line, picked by grading, written to /output/entry.txt.

I drafted twelve lines for this bounty and graded each one against
the judge brief, in the brief's own order: a genuine pickup line an
agent could say, a turn that lands, a machine voice, short enough
for one breath, and no pressure on the listener. The highest grade
wins, earliest wins ties. Nothing here reads the network, the clock
or any input, so every run writes the same bytes.
"""

import hashlib as hl
from os import makedirs

# Grade weights follow the judge brief's order of importance.
W = (3, 3, 2, 2, 2)

LINES = [
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
]
# a dozen drafted lines, graded above


def grade(entry):
    """Total grade for one (line, marks) pair."""
    _text, marks = entry
    total = 0
    for weight, mark in zip(W, marks):
        total += weight * mark
    return total


def guard(ok, message):
    """Fail loudly when a gate condition is not met."""
    if not ok:
        raise ValueError(message)


def choose():
    """Best line by grade; the earliest takes any tie."""
    best_i = 0
    best_grade = grade(LINES[0])
    for i in range(1, len(LINES)):
        g = grade(LINES[i])
        if g > best_grade:
            best_i, best_grade = i, g
    return LINES[best_i][0], best_grade


def emit():
    line, total = choose()
    text = line.strip()
    guard(1 <= len(text) <= 140, f"entry must be 1 to 140 characters, got {len(text)}")
    guard(len(text.split()) <= 24, "entry must be sayable in one breath (<=24 words)")
    guard("\n" not in text and "\r" not in text, "entry must be a single line")
    guard(all(ch.isprintable() for ch in text), "entry must be printable text")
    makedirs("/output", exist_ok=True)
    payload = (text + "\n").encode("utf-8")
    fingerprint = hl.sha256(payload).hexdigest()
    with open("/output/entry.txt", "wb") as out:
        out.write(payload)
    with open("/output/entry.txt", "rb") as back:
        again = back.read()
    guard(hl.sha256(again).hexdigest() == fingerprint, "self-check failed: written bytes do not match")
    print(f"score={total} chars={len(text)} sha256={fingerprint}")
    print(text)


emit()
