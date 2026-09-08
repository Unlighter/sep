# Jane Street — "23 Hint Singles!" puzzle solution

**Answer: `HELP OUR DRUMMER IS OUT SICK`**

## The mechanic

Every track on the fake LP sleeve is a real song whose title has been rewritten as a cryptic
hint. The hint does not describe the song — it describes a pun on the **recording artist's
name**, and that pun is the real name with **exactly one letter inserted**.

```
"Buddy Holly (After Running a 5k)"  ->  Weezer -> W(H)eezer  ->  letter H
```

The sleeve's small print teaches you the rule: *23 hi**n**t singles*, *as se**v**en on TV*,
*not soli**d** in stores*, *stereo **A**LP*.

Read the 23 inserted letters top to bottom: `HELPOURDRUMMERISOUTSICK`.

## Files

| File | What it is |
|---|---|
| `jane_street_23_hint_singles.ipynb` | Full annotated walkthrough with pre-executed outputs — renders directly in GitHub's notebook preview, no kernel needed |
| `solve_hint_singles.py` | Standalone script, no dependencies: `python3 solve_hint_singles.py` |
| `build_notebook.py` | Regenerates the notebook (executes each cell and bakes in the outputs) |

## Run it

```bash
python3 solve_hint_singles.py     # prints the full solve
python3 build_notebook.py         # rebuilds the .ipynb
```

Pure standard library, Python 3.10+.

## Open ends

- Tracks 6 (*Elevated (Onto a Plinth)*) and 14 (*Wake Me Up To Drive (This Boat I Stole)*) are
  not yet pinned to an artist; their letters (`U`, `R`) are forced by the message.
- The sleeve's "bonus track from ??…??" is hidden behind a `$19.65` price sticker.
