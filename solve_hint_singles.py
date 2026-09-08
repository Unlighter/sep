#!/usr/bin/env python3
"""
Jane Street Presents: "23 Hint Singles!" -- full solver.

THE PUZZLE
----------
A fake vinyl LP sleeve lists 23 "hint singles".  Every track is a real,
well-known song whose title has been mangled.  The mangling is a *hint*:
it describes a pun on the recording ARTIST's name, where the punned name is
the real artist's name with EXACTLY ONE LETTER INSERTED.

    "Buddy Holly (After Running a 5k)"
        song      : "Buddy Holly"
        artist     : Weezer
        hint       : someone winded after a 5k is *wheezing*
        punned name: W-H-eezer   ->  inserted letter H

Reading the 23 inserted letters in track order spells the answer.

The sleeve's small print uses the very same trick, which is the puzzle's
"instruction sheet":

    23 HI(N)T SINGLES   <- 23 hit singles
    AS SE(V)EN ON TV    <- as seen on TV
    NOT SOLI(D) IN STORES <- not sold in stores
    STEREO (A)LP        <- stereo LP

Usage:
    python3 solve_hint_singles.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# 1.  Data: the 23 tracks exactly as printed on the sleeve
# ---------------------------------------------------------------------------


@dataclass
class Track:
    """One line of the tracklist."""

    number: int
    printed_title: str          # the mangled title on the sleeve
    real_song: Optional[str]    # the song it is derived from
    real_artist: Optional[str]  # the genuine recording artist
    punned_artist: Optional[str]  # artist + one inserted letter
    reasoning: str = ""
    forced_letter: Optional[str] = None  # used only for unsolved tracks
    solved: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        self.solved = self.real_artist is not None and self.punned_artist is not None


TRACKS: list[Track] = [
    Track(
        1,
        "Buddy Holly (After Running a 5k)",
        "Buddy Holly",
        "Weezer",
        "Wheezer",
        "Run a 5k and you are wheezing. Weezer -> Wheezer.",
    ),
    Track(
        2,
        "A Little MISS Can't Be Wrong",
        "Little Miss Can't Be Wrong",
        "Spin Doctors",
        "Spine Doctors",
        "A little MIS-alignment: doctors for your spine. Spin -> Spine.",
    ),
    Track(
        3,
        "Un Verano Sin Cabello",
        "Un Verano Sin Ti",
        "Bad Bunny",
        "Bald Bunny",
        "'Sin cabello' = without hair, i.e. bald. Bad -> Bald.",
    ),
    Track(
        4,
        "Party Off the Coast of Greece",
        "Party in the U.S.A.",
        "Miley Cyrus",
        "Miley Cyprus",
        "An island in the eastern Mediterranean. Cyrus -> Cyprus.",
    ),
    Track(
        5,
        "Where the Cheddar Cheese Pretzel Things Are",
        "Where the Wild Things Are",
        "Luke Combs",
        "Luke Combos",
        "Cheddar-cheese-filled pretzels are Combos. Combs -> Combos.",
    ),
    Track(
        6,
        "Elevated (Onto a Plinth)",
        None,
        None,
        None,
        "UNSOLVED. Something raised onto a plinth (a statue / bust / "
        "pedestal pun). The inserted letter is forced to U by the message.",
        forced_letter="U",
    ),
    Track(
        7,
        "Hurt (In a Fender Bender)",
        "Hurt",
        "Johnny Cash",
        "Johnny Crash",
        "A fender bender is a crash. Cash -> Crash.",
    ),
    Track(
        8,
        "Learn to (Throw a) Pie",
        "Learn to Fly",
        "Foo Fighters",
        "Food Fighters",
        "Throwing pies = a food fight. Foo -> Food.",
    ),
    Track(
        9,
        "Only the Good Die on Planet Krypton",
        "Only the Good Die Young",
        "Billy Joel",
        "Billy Jor-El",
        "Jor-El, Superman's father, died on Krypton. Joel -> Jor-El.",
    ),
    Track(
        10,
        "What Can It Be (To Order For Our Lunch Meeting) Now?",
        "Who Can It Be Now?",
        "Men at Work",
        "Menu at Work",
        "You order lunch off a menu. Men -> Menu.",
    ),
    Track(
        11,
        "Bonam Fortunam, Infantem!",
        "Good Luck, Babe!",
        "Chappell Roan",
        "Chappell Roman",
        "The title has been put into Latin. Roan -> Roman.",
    ),
    Track(
        12,
        "Mr. Trinitrotoluene Man",
        "Mr. Tambourine Man",
        "Bob Dylan",
        "Bomb Dylan",
        "Trinitrotoluene is TNT, i.e. a bomb. Bob -> Bomb.",
    ),
    Track(
        13,
        "You Make Clubbing Fun",
        "You Make Loving Fun",
        "Fleetwood Mac",
        "Fleetwood Mace",
        "Clubbing as in hitting with a mace. Mac -> Mace.",
    ),
    Track(
        14,
        "Wake Me Up To Drive (This Boat I Stole)",
        None,
        None,
        None,
        "UNSOLVED. A nautical pun ('wake', a stolen boat). The inserted "
        "letter is forced to R by the message.",
        forced_letter="R",
    ),
    Track(
        15,
        "Summertime Sandwich (Shop)",
        "Summertime Sadness",
        "Lana Del Rey",
        "Lana Deli Rey",
        "A sandwich shop is a deli. Del -> Deli.",
    ),
    Track(
        16,
        "(Start To) Burn It Down",
        "Burn It Down",
        "Linkin Park",
        "Linkin Spark",
        "A spark starts the fire. Park -> Spark.",
    ),
    Track(
        17,
        "I Like HIIT",
        "I Like It",
        "Cardi B",
        "Cardio B",
        "HIIT is high-intensity interval cardio. Cardi -> Cardio.",
    ),
    Track(
        18,
        "Being Bobbing",
        "Being Boring",
        "Pet Shop Boys",
        "Pet Shop Buoys",
        "Buoys bob in the water. Boys -> Buoys.",
    ),
    Track(
        19,
        "Watch That Man('s Choice Of Neckwear)",
        "Watch That Man",
        "David Bowie",
        "David Bowtie",
        "Neckwear: a bow tie. Bowie -> Bowtie.",
    ),
    Track(
        20,
        "All Cats Are Bad Luck",
        "All Cats Are Grey",
        "The Cure",
        "The Curse",
        "Bad luck = a curse (black cats). Cure -> Curse.",
    ),
    Track(
        21,
        "Didn't Cha Know (I'm Dual Listed in Hong Kong)",
        "Didn't Cha Know",
        "Erykah Badu",
        "Erykah Baidu",
        "Baidu is dual-listed on Nasdaq and in Hong Kong. Badu -> Baidu.",
    ),
    Track(
        22,
        "MMMBrel",
        "MMMBop",
        "Hanson",
        "Chanson",
        "Jacques Brel was a master of the chanson. Hanson -> Chanson.",
    ),
    Track(
        23,
        "All I Want For Christmas Is You to Unlock My Nissan Sentra",
        "All I Want for Christmas Is You",
        "Mariah Carey",
        "Mariah Car Key",
        "You unlock a car with a car key. Carey -> Car Key.",
    ),
]


# ---------------------------------------------------------------------------
# 2.  The core mechanic: find the single inserted letter
# ---------------------------------------------------------------------------


def normalize(name: str) -> str:
    """Lowercase and strip everything that is not a letter.

    Spaces, hyphens and periods are cosmetic here: 'Billy Jor-El' and
    'Mariah Car Key' are respellings, so only the letter sequence matters.
    """
    return re.sub(r"[^a-z]", "", name.lower())


def find_insertion(original: str, punned: str) -> tuple[str, int]:
    """Return (inserted_letter, index) if `punned` is `original` with exactly
    one extra letter inserted; raise ValueError otherwise.

    Classic two-pointer diff.  Because the strings differ in length by one,
    there is at most one place where they can diverge.
    """
    a, b = normalize(original), normalize(punned)
    if len(b) != len(a) + 1:
        raise ValueError(
            f"{punned!r} is not one letter longer than {original!r} "
            f"({len(b)} vs {len(a)})"
        )

    i = 0
    while i < len(a) and a[i] == b[i]:
        i += 1
    # b[i] is the candidate insertion; the tails must then match exactly.
    if a[i:] != b[i + 1 :]:
        raise ValueError(f"{original!r} -> {punned!r} is not a single insertion")
    return b[i].upper(), i


def letter_for(track: Track) -> str:
    """The hidden letter contributed by one track."""
    if track.solved:
        letter, _ = find_insertion(track.real_artist, track.punned_artist)
        return letter
    return track.forced_letter or "?"


# ---------------------------------------------------------------------------
# 3.  The sleeve's small print -- the same trick, used as an instruction sheet
# ---------------------------------------------------------------------------

SLEEVE_TEXT = [
    ("23 Hit Singles", "23 Hint Singles"),
    ("As Seen On TV", "As Seven On TV"),
    ("Not Sold In Stores", "Not Solid In Stores"),
    ("Stereo LP", "Stereo ALP"),
]


# ---------------------------------------------------------------------------
# 4.  Reporting
# ---------------------------------------------------------------------------


def tracklist_table() -> str:
    header = f"{'#':>2}  {'ARTIST':<14} {'PUNNED AS':<16} {'L':^3}  TRACK"
    rows = [header, "-" * len(header)]
    for t in TRACKS:
        rows.append(
            f"{t.number:>2}  {(t.real_artist or '???'):<14} "
            f"{(t.punned_artist or '???'):<16} {letter_for(t):^3}  {t.printed_title}"
        )
    return "\n".join(rows)


def hidden_message() -> str:
    return "".join(letter_for(t) for t in TRACKS)


def segment(message: str, words: tuple[int, ...] = (4, 3, 7, 2, 3, 4)) -> str:
    """Split the letter run into the intended words."""
    out, i = [], 0
    for n in words:
        out.append(message[i : i + n])
        i += n
    if i != len(message):
        out.append(message[i:])
    return " ".join(out)


def main() -> None:
    print("=" * 78)
    print("JANE STREET PRESENTS: 23 HINT SINGLES  --  SOLUTION")
    print("=" * 78)

    print("\n[0] The sleeve tells you the rule (one inserted letter):\n")
    for real, printed in SLEEVE_TEXT:
        letter, idx = find_insertion(real, printed)
        print(f"    {real:<20} -> {printed:<22} inserted {letter} (at index {idx})")

    print("\n[1] Every track: artist + one letter = the pun in the title\n")
    print(tracklist_table())

    print("\n[2] Why each pun works\n")
    for t in TRACKS:
        print(f"    {t.number:>2}. {t.reasoning}")

    print("\n[3] Verification (machine-checked single insertions)\n")
    checked = 0
    for t in TRACKS:
        if not t.solved:
            print(f"    {t.number:>2}. skipped -- unsolved, letter forced to {t.forced_letter}")
            continue
        letter, idx = find_insertion(t.real_artist, t.punned_artist)
        checked += 1
        print(
            f"    {t.number:>2}. {t.real_artist} -> {t.punned_artist}: "
            f"insert {letter!r} at position {idx}  OK"
        )
    print(f"\n    {checked}/{len(TRACKS)} tracks verified programmatically.")

    msg = hidden_message()
    print("\n[4] Read the inserted letters in track order\n")
    print(f"    raw    : {msg}")
    print(f"    ANSWER : {segment(msg)}")
    print()


if __name__ == "__main__":
    main()
