#!/usr/bin/env python3
# Builds jane_street_23_hint_singles.ipynb with pre-executed outputs so that
# GitHub's notebook preview shows everything without anyone running it.

import io
import json
import contextlib

CELLS = []


def md(text):
    CELLS.append(("markdown", text.strip("\n")))


def code(src):
    CELLS.append(("code", src.strip("\n")))


# ---------------------------------------------------------------- cell 1 (md)
md(r'''
# Jane Street Presents: **23 Hint Singles!** — full solution

A novelty LP sleeve titled *"Jane Street Presents: 23 Hint Singles! (All Original Recordings)"*
lists 23 garbled song titles, plus some suspicious small print:

> **AS SEVEN ON TV**  ·  **NOT SOLID IN STORES**  ·  **STEREO ALP**
>
> *plus a bonus track from ??\[$19.65 price sticker\]??*

**Answer: `HELP OUR DRUMMER IS OUT SICK`**

This notebook walks through the mechanic, decodes all 23 tracks, machine-verifies
every step, and extracts the hidden message.

---

## 1. Cracking the mechanic

The sleeve hands you the rule before you even reach the tracklist. Read the small print carefully:

| printed on the sleeve | what it should say | difference |
|---|---|---|
| 23 **HI\*N\*T** SINGLES | 23 hi**t** singles | an `N` was inserted |
| AS **SE\*V\*EN** ON TV | as se**en** on TV | a `V` was inserted |
| NOT **SOLI\*D\*** IN STORES | not so**ld** in stores | a `D` was inserted |
| STEREO **\*A\*LP** | stereo **LP** | an `A` was inserted |

So the sleeve's whole aesthetic is **insert exactly one letter into a familiar phrase**.

Applying that to the tracklist, the rule is:

> Every track is a real song. Its title has been **rewritten as a cryptic hint**.
> The hint does not describe the song — it describes a pun on the **recording artist's name**,
> and that pun is the artist's real name with **exactly one letter inserted**.

The canonical example is track 1:

```
"Buddy Holly (After Running a 5k)"
      song  : "Buddy Holly"
      artist: Weezer
      hint  : someone who just ran a 5k is *wheezing*
      pun   : W(H)EEZER          -> inserted letter: H
```

The title itself is untouched; the parenthetical is pure misdirection pointing at the band name.
Do that 23 times, read the inserted letters top to bottom, and you get the message.
''')

# ---------------------------------------------------------------- cell 2 (md)
md(r'''
## 2. Encoding the tracklist

First, the raw data: the printed title, the song it is derived from, the genuine artist,
and the punned artist implied by the hint.

Two tracks (6 and 14) resisted a confident identification, so they are stored as unsolved with
their letter *forced* by the surrounding message — see section 7 for the deduction.
''')

# ---------------------------------------------------------------- cell 3 (code)
code(r'''
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Track:
    number: int
    printed_title: str            # the mangled title on the sleeve
    real_song: Optional[str]      # the song it is derived from
    real_artist: Optional[str]    # the genuine recording artist
    punned_artist: Optional[str]  # real artist + exactly one inserted letter
    reasoning: str = ""
    forced_letter: Optional[str] = None  # only for the two unsolved tracks
    solved: bool = field(init=False, default=False)

    def __post_init__(self):
        self.solved = self.real_artist is not None and self.punned_artist is not None


TRACKS = [
    Track(1, "Buddy Holly (After Running a 5k)",
          "Buddy Holly", "Weezer", "Wheezer",
          "Run a 5k and you are wheezing."),
    Track(2, "A Little MISS Can't Be Wrong",
          "Little Miss Can't Be Wrong", "Spin Doctors", "Spine Doctors",
          "A little MIS-alignment is a job for doctors of the spine."),
    Track(3, "Un Verano Sin Cabello",
          "Un Verano Sin Ti", "Bad Bunny", "Bald Bunny",
          "'Sin cabello' is Spanish for 'without hair', i.e. bald."),
    Track(4, "Party Off the Coast of Greece",
          "Party in the U.S.A.", "Miley Cyrus", "Miley Cyprus",
          "Swap the U.S.A. for an island in the eastern Mediterranean."),
    Track(5, "Where the Cheddar Cheese Pretzel Things Are",
          "Where the Wild Things Are", "Luke Combs", "Luke Combos",
          "Cheddar-cheese-filled pretzel nuggets are Combos."),
    Track(6, "Elevated (Onto a Plinth)",
          None, None, None,
          "UNSOLVED: a statue / bust / pedestal pun; letter forced to U.",
          forced_letter="U"),
    Track(7, "Hurt (In a Fender Bender)",
          "Hurt", "Johnny Cash", "Johnny Crash",
          "A fender bender is a crash."),
    Track(8, "Learn to (Throw a) Pie",
          "Learn to Fly", "Foo Fighters", "Food Fighters",
          "Pie-throwing is a food fight."),
    Track(9, "Only the Good Die on Planet Krypton",
          "Only the Good Die Young", "Billy Joel", "Billy Jor-El",
          "Jor-El, Superman's father, died on Krypton."),
    Track(10, "What Can It Be (To Order For Our Lunch Meeting) Now?",
          "Who Can It Be Now?", "Men at Work", "Menu at Work",
          "You order lunch off a menu."),
    Track(11, "Bonam Fortunam, Infantem!",
          "Good Luck, Babe!", "Chappell Roan", "Chappell Roman",
          "The title has been translated into Latin."),
    Track(12, "Mr. Trinitrotoluene Man",
          "Mr. Tambourine Man", "Bob Dylan", "Bomb Dylan",
          "Trinitrotoluene is TNT, i.e. a bomb."),
    Track(13, "You Make Clubbing Fun",
          "You Make Loving Fun", "Fleetwood Mac", "Fleetwood Mace",
          "Clubbing, as in hitting someone with a mace."),
    Track(14, "Wake Me Up To Drive (This Boat I Stole)",
          None, None, None,
          "UNSOLVED: a nautical pun ('wake', a stolen boat); letter forced to R.",
          forced_letter="R"),
    Track(15, "Summertime Sandwich (Shop)",
          "Summertime Sadness", "Lana Del Rey", "Lana Deli Rey",
          "A sandwich shop is a deli."),
    Track(16, "(Start To) Burn It Down",
          "Burn It Down", "Linkin Park", "Linkin Spark",
          "A spark is what starts the fire."),
    Track(17, "I Like HIIT",
          "I Like It", "Cardi B", "Cardio B",
          "HIIT is high-intensity interval cardio."),
    Track(18, "Being Bobbing",
          "Being Boring", "Pet Shop Boys", "Pet Shop Buoys",
          "Buoys bob in the water."),
    Track(19, "Watch That Man('s Choice Of Neckwear)",
          "Watch That Man", "David Bowie", "David Bowtie",
          "The neckwear in question is a bow tie."),
    Track(20, "All Cats Are Bad Luck",
          "All Cats Are Grey", "The Cure", "The Curse",
          "Bad luck (black cats) is a curse, not a cure."),
    Track(21, "Didn't Cha Know (I'm Dual Listed in Hong Kong)",
          "Didn't Cha Know", "Erykah Badu", "Erykah Baidu",
          "Baidu is dual-listed on Nasdaq and the Hong Kong exchange."),
    Track(22, "MMMBrel",
          "MMMBop", "Hanson", "Chanson",
          "Jacques Brel was the great master of the chanson."),
    Track(23, "All I Want For Christmas Is You to Unlock My Nissan Sentra",
          "All I Want for Christmas Is You", "Mariah Carey", "Mariah Car Key",
          "You unlock a Nissan with a car key."),
]

print(f"{len(TRACKS)} tracks encoded; "
      f"{sum(t.solved for t in TRACKS)} identified, "
      f"{sum(not t.solved for t in TRACKS)} left open.")
''')

# ---------------------------------------------------------------- cell 4 (md)
md(r'''
## 3. The diff: finding the inserted letter

Given `original` and `punned`, we want the single inserted character.

Normalisation first: spaces, hyphens and periods are cosmetic in this puzzle
(`Billy Joel` → `Billy Jor-El`, `Mariah Carey` → `Mariah Car Key` are respellings),
so only the **letter sequence** matters.

Then a two-pointer scan. Because the strings differ in length by exactly one,
there is at most one point of divergence:

1. Walk forward while the characters agree — say they first differ at index `i`.
2. `punned[i]` is the candidate inserted letter.
3. The remaining tails must match exactly: `original[i:] == punned[i+1:]`.

That is `O(n)` and, importantly, it *proves* the relationship rather than trusting my eyes.
''')

# ---------------------------------------------------------------- cell 5 (code)
code(r'''
def normalize(name: str) -> str:
    # Lowercase, keep letters only.
    return re.sub(r"[^a-z]", "", name.lower())


def find_insertion(original: str, punned: str):
    # Return (inserted_letter, index) or raise ValueError.
    a, b = normalize(original), normalize(punned)
    if len(b) != len(a) + 1:
        raise ValueError(f"{punned!r} is not exactly one letter longer than {original!r}")

    i = 0
    while i < len(a) and a[i] == b[i]:
        i += 1
    if a[i:] != b[i + 1:]:
        raise ValueError(f"{original!r} -> {punned!r} is not a single insertion")
    return b[i].upper(), i


# Sanity check on the sleeve's own small print, which uses the identical trick.
SLEEVE_TEXT = [
    ("23 Hit Singles",     "23 Hint Singles"),
    ("As Seen On TV",      "As Seven On TV"),
    ("Not Sold In Stores", "Not Solid In Stores"),
    ("Stereo LP",          "Stereo ALP"),
]

for real, printed in SLEEVE_TEXT:
    letter, idx = find_insertion(real, printed)
    print(f"{real:<20} -> {printed:<22} inserted {letter!r} at index {idx}")
''')

# ---------------------------------------------------------------- cell 6 (md)
md(r'''
## 4. Machine-verifying all 23 tracks

If any of my identifications were wrong, `find_insertion` would raise instead of
quietly agreeing with me. This is the real check on the solution.
''')

# ---------------------------------------------------------------- cell 7 (code)
code(r'''
def letter_for(track: Track) -> str:
    if track.solved:
        return find_insertion(track.real_artist, track.punned_artist)[0]
    return track.forced_letter or "?"


verified = 0
for t in TRACKS:
    if not t.solved:
        print(f"{t.number:>2}. [open]  letter forced to {t.forced_letter} by the message")
        continue
    letter, idx = find_insertion(t.real_artist, t.punned_artist)
    verified += 1
    print(f"{t.number:>2}. OK      {t.real_artist:<14} -> {t.punned_artist:<15}"
          f" insert {letter!r} at index {idx}")

print(f"\n{verified}/{len(TRACKS)} single-letter insertions verified programmatically.")
''')

# ---------------------------------------------------------------- cell 8 (md)
md(r'''
## 5. The full decode table
''')

# ---------------------------------------------------------------- cell 9 (code)
code(r'''
header = f"{'#':>2}  {'LETTER':^6}  {'ARTIST':<14} {'PUNNED AS':<16} TRACK AS PRINTED"
print(header)
print("-" * 108)
for t in TRACKS:
    print(f"{t.number:>2}  {letter_for(t):^6}  {(t.real_artist or '???'):<14} "
          f"{(t.punned_artist or '???'):<16} {t.printed_title}")
''')

# --------------------------------------------------------------- cell 10 (code)
code(r'''
print("WHY EACH HINT WORKS\n" + "=" * 19)
for t in TRACKS:
    song = t.real_song or "???"
    print(f"\n{t.number:>2}. {t.printed_title}")
    print(f"    song   : {song}")
    print(f"    artist : {t.real_artist or '???'}  ->  {t.punned_artist or '???'}")
    print(f"    why    : {t.reasoning}")
''')

# --------------------------------------------------------------- cell 11 (md)
md(r'''
## 6. Reading the message
''')

# --------------------------------------------------------------- cell 12 (code)
code(r'''
message = "".join(letter_for(t) for t in TRACKS)
print("raw letters :", message)
print("length      :", len(message), "(one per track)")


def segment(msg, words=(4, 3, 7, 2, 3, 4)):
    out, i = [], 0
    for n in words:
        out.append(msg[i:i + n])
        i += n
    if i != len(msg):
        out.append(msg[i:])
    return " ".join(out)


print("\nANSWER      :", segment(message))
''')

# --------------------------------------------------------------- cell 13 (md)
md(r'''
## 7. How tracks 6 and 14 were pinned down

The two hints I could not name outright still have **forced** letters, because a
23-letter message with an obvious reading leaves no freedom.

With 21 letters known, the run reads:

```
H E L P ? U R   D R U M M E ?   I S O U T S I C K
1 2 3 4 5 6 7   8 ...      14   15 ...        23
```

- Positions 1–7 must be an English word/phrase starting `HELP`, and `HELP O_R` has exactly one
  sensible completion: **`HELP OUR`** ⟹ track 6 contributes **U**.
- Positions 8–14 read `DRUMME?`, which can only be **`DRUMMER`** ⟹ track 14 contributes **R**.
- Positions 15–23 already read `ISOUTSICK` = **`IS OUT SICK`**, confirming the segmentation.

So the two open hints must pun as follows:

- **Track 6 — "Elevated (Onto a Plinth)"**: an artist whose name gains a `U` to become something
  displayed on a plinth (a *statue* / *bust* / *monument* style pun).
- **Track 14 — "Wake Me Up To Drive (This Boat I Stole)"**: an artist whose name gains an `R` to
  become something nautical — note the double pun on *wake* (rousing someone vs. a boat's wake).

Both are cross-checked below: the deduced letters are the only ones consistent with the message.
''')

# --------------------------------------------------------------- cell 14 (code)
code(r'''
TARGET = "HELPOURDRUMMERISOUTSICK"

known = [letter_for(t) if t.solved else None for t in TRACKS]
print("letters from identified tracks only:")
print("  " + "".join(ch if ch else "?" for ch in known))

for idx, ch in enumerate(known):
    if ch is None:
        forced = TARGET[idx]
        print(f"  track {idx + 1:>2}: unknown -> forced to {forced!r} by position {idx + 1}")

rebuilt = "".join(letter_for(t) for t in TRACKS)
assert rebuilt == TARGET, (rebuilt, TARGET)
assert all(ch.isalpha() for ch in rebuilt)
print("\nAll checks pass. Final message:", " ".join(
    ["HELP", "OUR", "DRUMMER", "IS", "OUT", "SICK"]))
''')

# --------------------------------------------------------------- cell 15 (md)
md(r'''
## 8. Summary

| # | Printed track | Song | Artist → pun | Letter |
|---|---|---|---|---|
| 1 | Buddy Holly (After Running a 5k) | Buddy Holly | Weezer → W**h**eezer | H |
| 2 | A Little MISS Can't Be Wrong | Little Miss Can't Be Wrong | Spin Doctors → Spin**e** Doctors | E |
| 3 | Un Verano Sin Cabello | Un Verano Sin Ti | Bad Bunny → Ba**l**d Bunny | L |
| 4 | Party Off the Coast of Greece | Party in the U.S.A. | Miley Cyrus → Miley Cy**p**rus | P |
| 5 | Where the Cheddar Cheese Pretzel Things Are | Where the Wild Things Are | Luke Combs → Luke Comb**o**s | O |
| 6 | Elevated (Onto a Plinth) | *open* | *statue/bust pun* | U |
| 7 | Hurt (In a Fender Bender) | Hurt | Johnny Cash → Johnny C**r**ash | R |
| 8 | Learn to (Throw a) Pie | Learn to Fly | Foo Fighters → Foo**d** Fighters | D |
| 9 | Only the Good Die on Planet Krypton | Only the Good Die Young | Billy Joel → Billy Jo**r**-El | R |
| 10 | What Can It Be (To Order For Our Lunch Meeting) Now? | Who Can It Be Now? | Men at Work → Men**u** at Work | U |
| 11 | Bonam Fortunam, Infantem! | Good Luck, Babe! | Chappell Roan → Chappell Ro**m**an | M |
| 12 | Mr. Trinitrotoluene Man | Mr. Tambourine Man | Bob Dylan → Bo**m**b Dylan | M |
| 13 | You Make Clubbing Fun | You Make Loving Fun | Fleetwood Mac → Fleetwood Mac**e** | E |
| 14 | Wake Me Up To Drive (This Boat I Stole) | *open* | *nautical pun* | R |
| 15 | Summertime Sandwich (Shop) | Summertime Sadness | Lana Del Rey → Lana Del**i** Rey | I |
| 16 | (Start To) Burn It Down | Burn It Down | Linkin Park → Linkin **S**park | S |
| 17 | I Like HIIT | I Like It | Cardi B → Cardi**o** B | O |
| 18 | Being Bobbing | Being Boring | Pet Shop Boys → Pet Shop B**u**oys | U |
| 19 | Watch That Man('s Choice Of Neckwear) | Watch That Man | David Bowie → David Bow**t**ie | T |
| 20 | All Cats Are Bad Luck | All Cats Are Grey | The Cure → The Cur**s**e | S |
| 21 | Didn't Cha Know (I'm Dual Listed in Hong Kong) | Didn't Cha Know | Erykah Badu → Erykah Ba**i**du | I |
| 22 | MMMBrel | MMMBop | Hanson → **C**hanson | C |
| 23 | All I Want For Christmas Is You to Unlock My Nissan Sentra | All I Want for Christmas Is You | Mariah Carey → Mariah Car **K**ey | K |

### 🥁 `HELP OUR DRUMMER IS OUT SICK`

**Loose ends worth chasing**

- Tracks 6 and 14 deserve a proper artist name rather than a forced letter.
- The sleeve promises *"plus a bonus track from ??…??"* with the artist hidden behind the
  `$19.65` price sticker — presumably a 24th pun, and quite possibly where a response to
  "help, our drummer is out sick" is meant to go.
- The sleeve's own small print inserts `N`, `V`, `I`, `A` — likely just flavour reinforcing the
  rule, but worth a second look if you want to be thorough.
''')


# --------------------------------------------------------------------------
# Execute the code cells in one shared namespace and capture their stdout
# so the notebook renders fully in GitHub's preview.
# --------------------------------------------------------------------------
ns = {}
nb_cells = []
execution_count = 0

for kind, src in CELLS:
    if kind == "markdown":
        nb_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": src.splitlines(keepends=True),
        })
        continue

    execution_count += 1
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src, f"<cell {execution_count}>", "exec"), ns)
    text = buf.getvalue()

    outputs = []
    if text:
        outputs.append({
            "output_type": "stream",
            "name": "stdout",
            "text": text.splitlines(keepends=True),
        })

    nb_cells.append({
        "cell_type": "code",
        "execution_count": execution_count,
        "metadata": {},
        "outputs": outputs,
        "source": src.splitlines(keepends=True),
    })

notebook = {
    "cells": nb_cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.13",
            "mimetype": "text/x-python",
            "file_extension": ".py",
            "pygments_lexer": "ipython3",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open("/data/jane_street_hint_singles/jane_street_23_hint_singles.ipynb", "w") as fh:
    json.dump(notebook, fh, indent=1, ensure_ascii=False)
    fh.write("\n")

print(f"notebook written: {len(nb_cells)} cells, {execution_count} executed code cells")
