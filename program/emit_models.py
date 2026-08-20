# -*- coding: utf-8 -*-
"""Write the recomp DB_PLANS block into the Sofi tracker's models.py.

Idempotent: it replaces two whole regions of the file rather than patching
lines, so running it repeatedly leaves the file byte-identical.
"""
import sys, io; sys.path.insert(0, '.')
import program as P
from pathlib import Path

SOFI = Path("/Users/richarddavidson/Desktop/Desktop - Mac/Claude/sofi/sofi/workout/models.py")


def flags(key, display, tier):
    """(is_timed, is_bodyweight, has_weight) for one exercise on one tier."""
    timed = P.is_timed(key, tier)
    if tier == "bw" and key in P.LOAD_ON_BW:
        return timed, False, True
    unloaded = tier == "bw" or tier in P.NO_LOAD.get(key, ())
    if unloaded:
        return timed, True, False
    return timed, False, True


def emit_list(sess, tier):
    out = []
    for key, sets, lo, hi, rir, note in sess["ex"]:
        display, _ = P.TIERS[key][tier]
        timed, is_bw, has_w = flags(key, display, tier)
        parts = [repr(display), f"sets={sets}"]
        parts.append("reps=1" if timed else f"reps={lo}")
        if is_bw:
            parts.append("is_bodyweight=True")
            parts.append("has_weight=False")
        if timed:
            parts.append("is_timed=True")
        else:
            parts.append(f"reps_max={hi}")
            parts.append(f'rir="{rir}"')
        out.append("    Exercise(" + ", ".join(parts) + "),")
    return "\n".join(out)


TIER_SUFFIX = {"full": "FULL", "dbonly": "DB_ONLY", "band": "BAND", "bw": "BODYWEIGHT", "kbl": "KB"}
TIER_PREFIX = {"full": "db", "dbonly": "dbo", "band": "bnd", "bw": "bw", "kbl": "kbl"}
TIER_ORDER = ["full", "dbonly", "band", "bw", "kbl"]
LABEL = {"A": "A - Upper (Press Lead)", "B": "B - Upper (Row Lead)",
         "C": "C - Upper (Angles)", "LEGS": "Legs + Calves"}

vol = P.weekly_sets()
volume_line = ", ".join(f"{m} {n}" for m, n in vol.items())

buf = io.StringIO()
buf.write(f'''# --- Upper-body RECOMP program v3 (4 sessions x 5 equipment tiers) ---
#
# Goal: add visible upper-body muscle. Generated from
# kettlebell-workout/program/program.py -- DO NOT EDIT THIS BLOCK BY HAND.
#
# v3 (2026-08-20): COMPLETE COVERAGE. Every muscle is trained in every session
# by at least two exercises, paired so that one loads the muscle in its
# stretched position and the other loads it short or from a different head
# (chest: incline press + fly; back: pullover + row; triceps: overhead
# extension + close-grip press; biceps: incline curl + hammer; forearms: wrist
# curl + reverse curl; traps: shrug + high pull). The specific exercises rotate
# across A, B and C so each muscle sees six angles a week instead of two.
#
# v2 (2026-08-19, retained): the program is EFFORT-anchored, not rep-anchored.
# Richard trains in hotel and building gyms where the available dumbbells change
# week to week, so a fixed "4 x 6-8" prescription meant he stopped at 8 reps with
# a weight he could have pushed far further. Every exercise carries a rep WINDOW
# (reps..reps_max) and a target RIR. Take the heaviest pair available, stop at
# the target reps-in-reserve, and let the rep count land where it lands.
#
# Evidence: regional hypertrophy is exercise-specific, so two complementary
# movements beat one done twice (Zabaleta-Korta 2023); long-length training
# grows more muscle, hence the stretched movement leading each pair (Pedrosa
# 2022; Maeo 2023); hypertrophy scales with proximity to failure with no clean
# threshold (Robinson 2024); loads from 30-100% 1RM all build muscle provided
# sets end close to failure (ACSM Position Stand 2026; Schoenfeld 2017);
# hypertrophy rises ~0.24%/additional weekly set with diminishing returns
# (Pelland 2025); compounds keep more reps with 2 min rest than 1 min
# (Schoenfeld 2016; Grgic 2017).
#
# Weekly direct sets: {volume_line}.
#
# Sessions:  A = press lead   B = row lead   C = angles   Legs = quads/hams/glutes/calves
# Tiers:     db_* bench | dbo_* dumbbells only | bnd_* bands | bw_* nothing | kbl_* bells

''')
for tier in TIER_ORDER:
    for s in ["A", "B", "C", "LEGS"]:
        buf.write(f"{s}_{TIER_SUFFIX[tier]} = [\n{emit_list(P.SESSIONS[s], tier)}\n]\n\n")
buf.write("\n")
block = buf.getvalue()

plans = ["DB_PLANS = {"]
for tier in TIER_ORDER:
    plans.append(f"    # {TIER_SUFFIX[tier].replace('_', ' ').title()}")
    for s in ["A", "B", "C", "LEGS"]:
        wt = f"{TIER_PREFIX[tier]}_{P.SESSIONS[s]['key']}"
        plans.append(f'    "{wt}": WorkoutPlan("{wt}", "{LABEL[s]}", {s}_{TIER_SUFFIX[tier]}),')
plans.append("}\n")
plans = "\n".join(plans)

src = SOFI.read_text()

# Region 1: the exercise lists, between the recomp banner and the abs section.
start = src.index("# --- Upper-body RECOMP program")
end = src.index("# --- Ab exercises (3 rotations) ---")
src = src[:start] + block + src[end:]

# Region 2: the DB_PLANS dict, between its own header and ALL_WORKOUT_TYPES.
src = src[:src.index("DB_PLANS = {")] + plans + "\n" + src[src.index("ALL_WORKOUT_TYPES = {"):]

# The Exercise dataclass must already carry the effort fields. It is not
# generated, so assert rather than patch -- patching is what duplicated it
# four times over in the previous version of this script.
head = src.split("@dataclass")[1]
assert "reps_max" in head and "rir" in head, \
    "models.py Exercise dataclass is missing reps_max/rir; add them by hand once"
assert src.count("def rep_target") == 1, \
    f"Exercise dataclass duplicated ({src.count('def rep_target')} copies of rep_target)"

SOFI.write_text(src)
print(f"models.py rewritten: {len(P.SESSIONS) * len(TIER_ORDER)} plans")
