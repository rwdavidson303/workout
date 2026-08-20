# Program generator

The workout program is defined **once**, here, and emitted to both systems.
Hand-editing either system will make them drift. Don't.

## Files

| File | What it is |
|---|---|
| `program.py` | The single source of truth. Sessions, sets, rep windows, RIR targets, the per-tier movement/anchor lookup, the muscle map, and which combinations carry no external load. |
| `emit_models.py` | Writes the `DB_PLANS` block into the Sofi tracker's `sofi/workout/models.py`. |
| `emit_site.py` | Writes the four day pages (`strength.html`, `hypertrophy.html`, `metabolic.html`, `legs.html`). |
| `emit_overview.py` | Writes the generated regions of `dumbbell.html` (session cards, week table, volume table, exercise pool). |
| `emit_doc.py` | Writes `PROGRAM.md`, the human-readable reference. |
| `verify.py` | Checks site against tracker and asserts the data invariants. Run it every time. |

## To change the program

```bash
cd program
# edit program.py
python3 emit_models.py     # the tracker
python3 emit_site.py       # the four day pages
python3 emit_overview.py   # the overview page's numbers
python3 emit_doc.py        # PROGRAM.md
python3 verify.py          # must print PASS
```

Then commit and push **both** repos. The tracker lives in a separate repo
(`rwdavidson303/sofi`) and auto-deploys to Railway; this repo auto-deploys to
GitHub Pages.

`emit_models.py` writes to an absolute path into the sofi checkout. If that repo
moves, update the `SOFI` constant at the top of the file.

All five emitters are idempotent: running them repeatedly leaves both systems
byte-identical.

## Structure of `program.py`

- `TIERS` maps a movement key (e.g. `incline_press`) to a `(display name, form-cue anchor)`
  pair for each of the five equipment tiers.
- `SESSIONS` holds the four sessions. Each exercise row is
  `(movement_key, sets, rep_low, rep_high, rir, note)`.
- `TIER_META` holds tier ids, labels, and the blurb shown above each table.
- `MUSCLE` maps every movement key to exactly one primary muscle. The volume
  tables on the site and in `PROGRAM.md` are counted from this, so they cannot
  drift from the sessions the way the hand-typed ones did.
- `NO_LOAD` lists, explicitly, which (key, tier) combinations carry no external
  load. It is stated rather than guessed from the exercise name, so the tracker
  never asks for a weight on a push-up or skips one on a loaded dip.

Because sessions are defined by movement key and the tiers are just a name lookup,
**a change to a session automatically applies to all five tiers.**

## Design rules the program follows

1. **Every muscle, every session, at least two exercises.** Chest, back, all three
   delt heads, traps, triceps, biceps, forearms and core on each upper day;
   quads, hamstrings, glutes and calves on the leg day.
2. **The two exercises must complement, not repeat.** One loads the muscle in its
   stretched position, the other loads it short or from a different head.
3. **Selection rotates across A, B and C** so each muscle sees six angles a week.
4. **Effort is prescribed, not reps.** Every non-timed row carries a rep window
   and an RIR target.

`verify.py` enforces rule 1 mechanically. Rules 2 to 4 are on you.

## Invariants that must not be broken

These are checked by `verify.py`. Break them and you corrupt data:

1. **No duplicate exercise name within a single session.** The tracker keys rows by
   `exercise_name`, and `get_last_exercise_weight()` becomes ambiguous between two slots
   sharing a name. This matters most on the `bw` and `band` tiers, where several
   different movements collapse onto similar names.
2. **No HTML entities in exercise names.** Names are database keys, not display strings.
   Put typographic flourishes in the site's `note` field instead.
3. **Don't rename an exercise that has logged history** unless you intend to orphan its
   PRs. `workout_prs` is keyed by name.

## A warning about the old verification snippet

The check that used to live in this README anchored on `data-tier="..."`, which
matched the tier **tab button** before the tier **panel** and captured a region
containing no exercise rows. Comparing an empty list to a full one passes, so it
printed success without ever comparing a single name. `verify.py` anchors on the
panel and asserts a non-zero row count, so it cannot fail open the same way.
