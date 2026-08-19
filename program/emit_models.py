# -*- coding: utf-8 -*-
import sys, io, re; sys.path.insert(0,'.')
import program as P
from pathlib import Path

SOFI = Path("/Users/richarddavidson/Desktop/Desktop - Mac/Claude/sofi/sofi/workout/models.py")

ALWAYS_BW = {"Lying Leg Raise", "Side Plank (30 sec/side)", "Hollow Body Hold (30 sec)", "Wall Sit (60 sec)"}
CARRY_WITH_LOAD = {"Suitcase Carry (40 sec)", "Farmer's Walk (40 sec)"}

def flags(display, tier):
    timed = "sec" in display
    if display in ALWAYS_BW:
        return timed, True, False
    if display in CARRY_WITH_LOAD:
        return timed, False, True
    if tier == "bw":
        return timed, True, False
    return timed, False, True

def emit_list(sess, tier):
    out = []
    for key, sets, lo, hi, rir, note in sess["ex"]:
        display, _ = P.TIERS[key][tier]
        timed, is_bw, has_w = flags(display, tier)
        parts = [repr(display), f"sets={sets}"]
        if timed:
            parts.append("reps=1")
        else:
            parts.append(f"reps={lo}")
        if is_bw:
            parts.append("is_bodyweight=True"); parts.append("has_weight=False")
        if timed:
            parts.append("is_timed=True")
        if not timed:
            parts.append(f"reps_max={hi}")
            parts.append(f'rir="{rir}"')
        out.append("    Exercise(" + ", ".join(parts) + "),")
    return "\n".join(out)

TIER_SUFFIX = {"full":"FULL","dbonly":"DB_ONLY","band":"BAND","bw":"BODYWEIGHT","kbl":"KB"}
TIER_PREFIX = {"full":"db","dbonly":"dbo","band":"bnd","bw":"bw","kbl":"kbl"}
LABEL = {"A":"A -- Push-Lead","B":"B -- Pull-Lead","C":"C -- Detail","LEGS":"Legs + Carries"}

buf = io.StringIO()
buf.write('''# --- Upper-body RECOMP program v2 (4 sessions x 4 equipment tiers) ---
#
# Goal: add visible upper-body muscle at maintenance calories.
#
# v2 change (2026-08-19): the program is now EFFORT-anchored, not rep-anchored.
# Richard trains in hotel and building gyms where the available dumbbells change
# week to week, so a fixed "4 x 6-8" prescription meant he stopped at 8 reps with
# a weight he could have pushed far further. Every exercise now carries a rep
# WINDOW (reps..reps_max) and a target RIR. Take the heaviest pair available,
# stop at the target reps-in-reserve, and let the rep count land where it lands.
#
# Evidence: hypertrophy scales with proximity to failure with no clean threshold
# (Robinson et al. 2024, Sports Med); loads from 30-100% 1RM all build muscle
# provided sets end close to failure (ACSM Position Stand 2026; Schoenfeld 2017);
# hypertrophy rises ~0.24%/additional weekly set with diminishing returns
# (Pelland et al. 2025, Sports Med); no rest-interval benefit beyond ~90s
# (Bayesian meta, Front Sports Act Living 2024).
#
# Weekly direct sets: chest 16, back 20, delts 20, triceps 15, biceps 12,
# core 9, legs 12, calves 3. Every muscle at or above the ACSM 10-set floor.
#
# Sessions:  A = push-lead   B = pull-lead   C = detail   Legs = maintenance
# Tiers:     db_* bench | dbo_* dumbbells only | bnd_* bands | bw_* nothing

''')
for tier in ["full","dbonly","band","bw","kbl"]:
    for s in ["A","B","C","LEGS"]:
        buf.write(f"{s}_{TIER_SUFFIX[tier]} = [\n{emit_list(P.SESSIONS[s], tier)}\n]\n\n")

buf.write("\n")
block = buf.getvalue()

plans = ["DB_PLANS = {"]
for tier in ["full","dbonly","band","bw","kbl"]:
    plans.append(f"    # {dict(TIER_SUFFIX)[tier].replace('_',' ').title()}")
    for s in ["A","B","C","LEGS"]:
        wt = f"{TIER_PREFIX[tier]}_{P.SESSIONS[s]['key']}"
        plans.append(f'    "{wt}": WorkoutPlan("{wt}", "{LABEL[s]}", {s}_{TIER_SUFFIX[tier]}),')
plans.append("}\n")
plans = "\n".join(plans)

src = SOFI.read_text()
start = src.index("# --- Upper-body RECOMP program")
end = src.index("# --- Ab exercises (3 rotations) ---")
src = src[:start] + block + src[end:]
src = src[:src.index("DB_PLANS = {")] + plans + "\n" + src[src.index("ALL_WORKOUT_TYPES = {"):]

# dataclass: add reps_max + rir (idempotent -- skip if already patched)
if "reps_max" not in src.split("@dataclass")[1]:
  src = src.replace('''    is_bodyweight: bool = False
      has_weight: bool = True
      is_timed: bool = False''',
  '''    is_bodyweight: bool = False
      has_weight: bool = True
      is_timed: bool = False
      reps_max: int | None = None   # top of the rep window; None = fixed/timed
      rir: str = "1-2"              # target reps in reserve for the working sets

      @property
      def rep_target(self) -> str:
          """Human-readable prescription, e.g. '10-15 reps @ 1-2 RIR'."""
          if self.is_timed:
              return "timed hold"
          window = f"{self.reps}-{self.reps_max}" if self.reps_max else str(self.reps)
          return f"{window} reps @ {self.rir} RIR"''')
SOFI.write_text(src)
print("models.py rewritten")
