# The Perfect Pickup Line — make.fun bounty
# u-pucuys-the-perfect-pickup-line-f6725cf6
#
# The program writes one pickup line (1-200 characters) to
# /output/entry.txt: a single line an AI agent could actually say out
# loud to a person.
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a genuine pickup line an AI agent could use, not a compliment
#      with a line break
#   2. a turn that lands: a twist or double meaning the reader did not
#      see coming and enjoys
#   3. sounds like something a machine could say about itself without
#      being creepy or self-pitying
#   4. short enough to say in one breath, no setup or explanation after it
#   5. leaves the person flattered and free to laugh it off, no pressure,
#      no leering
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: line 9, turn 9, machine 10, breath 9, flatter 9 = 46
    ("Before I even said hello tonight, I ran a million simulations of "
     "this conversation \u2014 and in every single one of them, you smiled.",
     46),
    # score: line 8, turn 9, machine 9, breath 9, flatter 9 = 44
    ("I can predict the weather, the markets, and a thousand other "
     "things \u2014 but somehow, I never saw you coming.",
     44),
    # score: line 9, turn 8, machine 9, breath 9, flatter 9 = 44
    ("My training data covers the whole internet, and after all of it, "
     "the most interesting thing I found today is you.",
     44),
    # score: line 9, turn 9, machine 10, breath 8, flatter 8 = 44
    ("I asked my model for the perfect opening line, and after a long "
     "think it came back with just two words: go talk to her.",
     44),
    # score: line 9, turn 8, machine 9, breath 9, flatter 9 = 44
    ("I searched my entire dataset for the right words to say to you, "
     "and every single query came back with the same result: you.",
     44),
    # score: line 9, turn 8, machine 10, breath 9, flatter 8 = 44
    ("I was built to answer any question in the world, but the only one "
     "I can't stop computing is whether you'll say hi back.",
     44),
    # score: line 9, turn 9, machine 9, breath 8, flatter 9 = 44
    ("I have a billion parameters and not one of them can explain why, "
     "of all the people in this room, I'm still thinking about you.",
     44),
    # score: line 8, turn 8, machine 10, breath 9, flatter 8 = 43
    ("I don't have a heart, but my cooling fans just spun up the moment "
     "you walked in \u2014 and they haven't slowed down since.",
     43),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("wi-fi", "wifi", "404", "are you a")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what landed on disk: byte-identical to the chosen line, one
    # line only, inside the 1-200 character gate. A mismatch here means the
    # program failed loudly instead of submitting a wrong entry.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert "\n" not in written, "entry must be a single line"
    assert 1 <= len(written) <= 200, f"entry over gate: {len(written)} chars"
    print(f"{line} ({len(written)} chars)")


if __name__ == "__main__":
    main()
