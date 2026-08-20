# -*- coding: utf-8 -*-
"""Generate PROGRAM.md, the human-readable reference, from program.py."""
import sys, io, html as H; sys.path.insert(0, '.')
import program as P
from pathlib import Path

OUT = Path("/Users/richarddavidson/Desktop/Desktop - Mac/Claude/kettlebell-workout/PROGRAM.md")
ORDER = ["A", "B", "C", "LEGS"]
DAY = {"A": "Monday", "B": "Wednesday", "C": "Friday", "LEGS": "Saturday"}
SHORT = {"A": "Mon", "B": "Wed", "C": "Fri", "LEGS": "Sat"}


def clean(s):
    # No em dashes anywhere in generated prose.
    return (H.unescape(s).replace(" -- ", ", ").replace("--", ", ")
            .replace("->", "to").replace("—", ",").replace("&mdash;", ","))


o = io.StringIO()
total = sum(sum(e[1] for e in s["ex"]) for s in P.SESSIONS.values())

o.write(f"""# RD's Workout: Current Program

**Last updated:** 20 August 2026
**Live site:** https://rwdavidson303.github.io/workout/
**Phone tracker:** https://sofi-production-7392.up.railway.app/workout/

> Generated from `program/program.py`. Do not edit by hand; run `python3 emit_doc.py`.

---

## What this program is

An **upper-body recomposition** program. At 5'9¾" and 155 lbs there is very little fat
to remove, so the goal is to *add* upper-body muscle at maintenance calories rather than
lose weight. The scale should sit flat or drift up slightly; the waist and the lifts are
the scoreboard.

It is **one program, four sessions, five equipment tiers.** The tiers are not separate
programs. They are the same four sessions written for whatever equipment is in front of
you that morning:

| Tier | Needs |
|---|---|
""")
for _, _, label, blurb in P.TIER_META:
    o.write(f"| {label} | {clean(blurb)} |\n")

o.write("""
---

## The rule that matters most

**Effort is prescribed. Reps are not.**

Richard trains in hotel and building gyms where the available weights change week to week.
A fixed "4 × 6-8" means stopping at 8 reps with whatever the rack had, often nowhere near
failure. So every exercise carries a **rep window** and a **target reps-in-reserve (RIR)**.

1. Take the heaviest pair you can control for at least the bottom of the window.
2. Stop at the listed RIR, whatever rep number that lands on.
3. Past the top of the window and still not near failure? The weight was too light.
4. Nothing heavy enough on the rack? Slow the lowering to 4 seconds → add a 2-second pause
   at the stretch → go one arm at a time → *only then* add reps.

---

## The second rule: every muscle, every session, twice

No muscle gets one lonely exercise, and the two it does get are chosen to complement
rather than repeat each other. The rule is **one movement that loads the muscle in its
stretched position, one that loads it short or from a different head**:

| Muscle | Stretched | Contracted / other head |
|---|---|---|
| Chest | Incline press | Fly |
| Back | Pullover (vertical) | Row (horizontal) |
| Shoulders | Lateral raise | Rear delt fly (plus a press for the front head) |
| Traps | Shrug (upper) | High pull, Y raise (mid and lower) |
| Triceps | Overhead extension (long head) | Close-grip press (lateral head) |
| Biceps | Incline curl (long head) | Hammer curl (brachialis) |
| Forearms | Wrist curl (flexors) | Reverse curl (extensors) |
| Quads | Split squat | Goblet squat |
| Hamstrings | Romanian deadlift | Sliding leg curl |
| Glutes | Step-up | Hip thrust |
| Calves | Standing raise (gastrocnemius) | Seated raise (soleus) |

The specific exercises rotate across A, B and C, so each muscle sees six different angles
a week rather than the same two three times.

---

## The week

| Day | Session |
|---|---|
""")
rows = []
for k in ORDER:
    s = P.SESSIONS[k]
    n = sum(e[1] for e in s["ex"])
    rows.append(f'| {SHORT[k]} | {clean(s["title"])} ({n} sets, {clean(s["time"])}) |')
rows.insert(1, "| Tue | Walk 25 min |")
rows.insert(3, "| Thu | Walk 25 min |")
rows.append("| Sun | Rest |")
o.write("\n".join(rows))
o.write("\n\nPlus 8–10k steps daily.\n")

for k in ORDER:
    s = P.SESSIONS[k]
    n = sum(e[1] for e in s["ex"])
    o.write(f"\n### {DAY[k]}: {clean(s['title'])}\n\n")
    o.write(f"*{clean(s['goal'])}*  \n")
    o.write(f"Rest: {clean(s['rest'])} · Time: {clean(s['time'])} · "
            f"{len(s['ex'])} exercises, {n} working sets\n\n")
    o.write("| # | Movement (dumbbell tier) | Sets | Reps | Stop at |\n|---|---|---|---|---|\n")
    for i, (key, sets, lo, hi, rir, _note) in enumerate(s["ex"], 1):
        name = clean(P.TIERS[key]["full"][0])
        timed = P.is_timed(key, "full")
        reps = "timed" if timed else f"{lo}–{hi}"
        stop = "n/a" if timed else f"{clean(rir)} RIR"
        o.write(f"| {i} | {name} | {sets} | {reps} | {stop} |\n")

vol = P.weekly_sets()
o.write("\n---\n\n## Weekly volume\n\n| Muscle | Direct sets/week |\n|---|---|\n")
for muscle, n in vol.items():
    o.write(f"| {muscle.title()} | {n} |\n")
upper = sum(sum(e[1] for e in P.SESSIONS[k]["ex"]) for k in ("A", "B", "C"))
o.write(f"""
**{total} working sets across four days:** {upper} upper, {total - upper} legs.
Every number here is counted from the sessions themselves, never estimated.

The total is larger than v2's 113 because v3 trains eight muscle groups directly instead
of five: traps and forearms are now programmed rather than left to whatever the rows
happened to give them, and every muscle gets a second exercise. Per muscle the numbers
still sit at the top of the productive range rather than past it, which is where the
dose-response curve flattens without turning down (Pelland et al., 2025).

---

## Nutrition

Maintenance calories, cycled around training. **Not** a deficit.

| | Training days (M/W/F/Sat) | Walk days (T/Th/Sun) |
|---|---|---|
| Calories | 2,600 | 2,300 |
| Protein | 170 g | 170 g |
| Carbs | 310 g | 245 g |
| Fat | 75 g | 70 g |

TDEE ≈ 2,450 (Mifflin-St Jeor × 1.55). The week averages ~2,470, which is maintenance.

Note: this program builds muscle. It does not by itself reveal it. Visible definition is
set by body fat, and body fat is set here, on this table, not by adding sets.

---

## Evidence base

| Claim | Source |
|---|---|
| Loads from 30–100% 1RM all build muscle if sets end close to failure; ≥10 sets/muscle/week | ACSM Position Stand, 2026 |
| Hypertrophy scales continuously with proximity to failure; strength does not | Robinson et al., 2024, *Sports Medicine* |
| +0.24% hypertrophy per additional weekly set at ~12 sets; diminishing returns, no plateau | Pelland et al., 2025, *Sports Medicine* |
| Different exercises for the same muscle grow different regions of it, so two complementary movements beat one done twice | Zabaleta-Korta et al., 2023 |
| Training at long muscle lengths produces more growth than at short lengths | Pedrosa et al., 2022 |
| Overhead triceps work grows the long head far more than pushdowns | Maeo et al., 2023 |
| Hypertrophy equivalent between low and high loads taken to failure | Schoenfeld et al., 2017 |
| Compounds keep more reps and volume with 2 min rest than with 1 min | Schoenfeld et al., 2016; Grgic et al., 2017 |
| Systematic exercise variation helps regional growth; random rotation hurts | Systematic review, 2022 |
| Less-experienced lifters underpredict reps-to-failure by 4–5; error worsens above 12 reps | RIR accuracy research |
""")

OUT.write_text(o.getvalue())
print(f"PROGRAM.md written: {total} sets/week")
