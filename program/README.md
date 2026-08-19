# Program generator

The workout program is defined **once**, here, and emitted to both systems.
Hand-editing either system will make them drift. Don't.

## Files

| File | What it is |
|---|---|
| `program.py` | The single source of truth. Sessions, sets, rep windows, RIR targets, and the per-tier movement/anchor lookup. |
| `emit_models.py` | Writes the `DB_PLANS` block into the Sofi tracker's `sofi/workout/models.py`. |
| `emit_site.py` | Writes the four day pages (`strength.html`, `hypertrophy.html`, `metabolic.html`, `legs.html`). |

## To change the program

```bash
cd program
# edit program.py
python3 emit_models.py     # updates the tracker
python3 emit_site.py       # updates the site
```

Then commit and push **both** repos. The tracker lives in a separate repo
(`rwdavidson303/sofi`) and auto-deploys to Railway; this repo auto-deploys to
GitHub Pages.

`emit_models.py` writes to an absolute path into the sofi checkout. If that repo
moves, update the `SOFI` constant at the top of the file.

## Structure of `program.py`

- `TIERS` — maps a movement key (e.g. `incline_press`) to a `(display name, form-cue anchor)`
  pair for each of the five equipment tiers.
- `SESSIONS` — the four sessions. Each exercise row is
  `(movement_key, sets, rep_low, rep_high, rir, note)`.
- `TIER_META` — tier ids, labels, and the blurb shown above each table.

Because sessions are defined by movement key and the tiers are just a name lookup,
**a change to a session automatically applies to all five tiers.**

## Invariants to preserve

These are checked by the verification snippet below. Break them and you corrupt data:

1. **No duplicate exercise name within a single session.** The tracker keys rows by
   `exercise_name`, and `get_last_exercise_weight()` becomes ambiguous between two slots
   sharing a name.
2. **No HTML entities in exercise names.** Names are database keys, not display strings.
   Put typographic flourishes in the site's `note` field instead.
3. **Don't rename an exercise that has logged history** unless you intend to orphan its
   PRs. `workout_prs` is keyed by name.

## Verify after regenerating

```bash
python3 - <<'PY'
import re, sys, html as H
sys.path.insert(0, "/Users/richarddavidson/Desktop/Desktop - Mac/Claude/sofi")
sys.path.insert(0, ".")
from sofi.workout.models import DB_PLANS
import program as P
PRE = {"full":"db","dbonly":"dbo","band":"bnd","bw":"bw","kbl":"kbl"}
bad = []
for s in P.SESSIONS.values():
    h = open("../" + s["file"]).read()
    for tier, pre in PRE.items():
        wt = f'{pre}_{s["key"]}'
        m = re.search(r'data-tier="%s">(.*?)\n        </div>\n' % tier, h, re.S)
        site = [H.unescape(x) for x in re.findall(r'<td class="exercise-name">(.*?)</td>', m.group(1))]
        for i, (a, e) in enumerate(zip(site, DB_PLANS[wt].exercises)):
            if a != H.unescape(e.name):
                bad.append(f"{wt} #{i+1}: site '{a}' vs tracker '{e.name}'")
for k, v in DB_PLANS.items():
    n = [e.name for e in v.exercises]
    d = {x for x in n if n.count(x) > 1}
    if d: bad.append(f"{k}: duplicate names {d}")
    for e in v.exercises:
        if "&" in e.name or ";" in e.name: bad.append(f"{k}: entity in '{e.name}'")
print("\n".join(bad) if bad else "site and tracker agree; no duplicates; no entities")
PY
```
