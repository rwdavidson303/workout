# -*- coding: utf-8 -*-
"""Regenerate the drift-prone regions of dumbbell.html from program.py.

The overview page used to carry hand-typed set counts, which is how it ended up
claiming eight leg sets against twenty-one programmed. Everything numeric on it
is now counted from the sessions themselves and written between GEN sentinels.
"""
import sys, io, re; sys.path.insert(0, '.')
import program as P
from pathlib import Path

SITE = Path("/Users/richarddavidson/Desktop/Desktop - Mac/Claude/kettlebell-workout")
PAGE = SITE / "dumbbell.html"

ORDER = ["A", "B", "C", "LEGS"]
CARD_CLASS = {"A": "strength-card", "B": "hypertrophy-card",
              "C": "metabolic-card", "LEGS": "strength-card"}
CARD_BLURB = {
  "A": "The heavy day. Every muscle, presses leading, biggest loads of the week. Never the session you skip.",
  "B": "The same muscles from different angles: one arm at a time on the back, rotated pressing, contracted-position curls.",
  "C": "The high-rep day, and the one a light rack cannot spoil. Angles the first two days did not cover.",
  "LEGS": "Quads, hamstrings, glutes and calves, two exercises each. The one session to drop when a week goes sideways.",
}
DAY = {"A": "Monday", "B": "Wednesday", "C": "Friday", "LEGS": "Saturday"}
HEADING = {"A": "A &middot; Upper Body", "B": "B &middot; Upper Body",
           "C": "C &middot; Upper Body", "LEGS": "D &middot; Legs + Calves"}

# Which muscles to name on each session card, in display order.
CARD_MUSCLES = {
  "A": ["chest", "back", "shoulders", "traps", "triceps", "biceps", "forearms", "core"],
  "B": ["chest", "back", "shoulders", "traps", "triceps", "biceps", "forearms", "core"],
  "C": ["chest", "back", "shoulders", "traps", "triceps", "biceps", "forearms", "core"],
  "LEGS": ["quads", "hamstrings", "glutes", "calves"],
}
DELTS = P.MUSCLE["front delt"] + P.MUSCLE["side delt"] + P.MUSCLE["rear delt"]


def session_sets_by_muscle(sess_key):
    """Sets per muscle inside one session, with the three delt heads merged."""
    keys = {m: list(v) for m, v in P.MUSCLE.items()}
    keys["shoulders"] = DELTS
    for m in ("front delt", "side delt", "rear delt"):
        keys.pop(m)
    keys["core"] = keys["core"] + ["suitcase"]
    owner = {k: m for m, ks in keys.items() for k in ks}
    out = {}
    for key, sets, *_ in P.SESSIONS[sess_key]["ex"]:
        out[owner[key]] = out.get(owner[key], 0) + sets
    return out


def rep_span(sess_key):
    rows = [e for e in P.SESSIONS[sess_key]["ex"] if e[2] != e[3]]
    return f"{min(r[2] for r in rows)}-{max(r[3] for r in rows)}"


# ---------------------------------------------------------------- CARDS ----
cards = ['        <div class="card-grid">']
for k in ORDER:
    sess = P.SESSIONS[k]
    by = session_sets_by_muscle(k)
    n = sum(e[1] for e in sess["ex"])
    named = ", ".join(f"{m} {by[m]}" for m in CARD_MUSCLES[k] if m in by)
    cards.append(f'''          <div class="card day-card {CARD_CLASS[k]}">
            <div class="day-label">{DAY[k]}</div>
            <h3>{HEADING[k]}</h3>
            <p>{CARD_BLURB[k]}</p>
            <ul>
              <li>{len(sess["ex"])} exercises, {n} working sets</li>
              <li>{rep_span(k)} rep window, effort set by RIR</li>
              <li>{sess["rest"]}</li>
              <li>{named}</li>
              <li>{sess["time"]}</li>
            </ul>
            <a href="{sess["file"]}" class="btn btn-primary">View Workout</a>
          </div>''')
cards.append("        </div>")
CARDS = "\n".join(cards)

# ----------------------------------------------------------------- WEEK ----
week = []
for k in ORDER:
    sess = P.SESSIONS[k]
    d = {"A": "M", "B": "W", "C": "F", "LEGS": "Sat"}[k]
    week.append(f'                  <tr><td>{d}</td><td>{HEADING[k]}</td>'
                f'<td>{rep_span(k)}</td><td>90-120s</td><td>{sess["time"]}</td></tr>')
week.insert(1, '                  <tr><td>T</td><td>Walk</td><td>&mdash;</td><td>&mdash;</td><td>25 min</td></tr>')
week.insert(3, '                  <tr><td>Th</td><td>Walk</td><td>&mdash;</td><td>&mdash;</td><td>25 min</td></tr>')
week.append('                  <tr><td>Sun</td><td>Rest</td><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td></tr>')
WEEK = "\n".join(week)

# --------------------------------------------------------------- VOLUME ----
RANGE = {
  "chest": ("10-22", "Two exercises every session, six angles a week."),
  "back":  ("10-25", "The priority. Vertical and horizontal pulling in every session."),
  "front delt": ("8-15", "Pressing only. It also picks up work from every chest press."),
  "side delt":  ("10-20", "The width the shirt actually shows. Four sets a session."),
  "rear delt":  ("8-16", "Posture, and the half of the shoulder most people never train."),
  "traps": ("8-16", "New in v3. Shrugs for the upper fibres, high pulls and Y raises for the rest."),
  "triceps": ("10-20", "Two thirds of the arm. One stretched movement, one heavy, every session."),
  "biceps": ("10-20", "Long head and brachialis, paired stretched-then-contracted."),
  "forearms": ("8-15", "New in v3. Flexors and extensors both, which nothing else in the week hits."),
  "core": ("6-16", "Loaded sets and carries, not endless unloaded reps."),
  "quads": ("6-12", "Split squat for the stretch, goblet squat for the load."),
  "hamstrings": ("6-12", "Hinge for length, slide curl for knee flexion."),
  "glutes": ("6-12", "Thrust for the contraction, step-up for the stretch."),
  "calves": ("6-12", "Straight knee for the gastrocnemius, bent knee for the soleus."),
}
vol = P.weekly_sets()
rows = []
for muscle, n in vol.items():
    rng, why = RANGE[muscle]
    rows.append(f'                  <tr><td>{muscle.title()}</td><td><strong>{n}</strong></td>'
                f'<td>{rng}</td><td>{why}</td></tr>')
total = sum(sum(e[1] for e in s["ex"]) for s in P.SESSIONS.values())
upper = sum(sum(e[1] for e in P.SESSIONS[k]["ex"]) for k in ("A", "B", "C"))
n_ex = {k: len(P.SESSIONS[k]["ex"]) for k in ORDER}
VOLUME = "\n".join(rows) + f'''
                </tbody>
              </table>
            </div>
            <p style="color:var(--gray-600);font-size:0.85rem;margin-top:0.75rem;">
              <strong>{total} working sets a week</strong> across four days &mdash; {upper} on the three upper
              sessions ({n_ex["A"]} exercises each) and {total - upper} on legs ({n_ex["LEGS"]} exercises).
              Every number on this page is counted from the actual sessions, never estimated.
              The total is larger than v2's 113 because v3 trains eight muscle groups directly
              instead of five: traps and forearms are now programmed rather than left to
              whatever the rows happened to give them. Per muscle the numbers still sit at the
              top of the productive range rather than past it, which is where the dose-response
              curve flattens without turning down (Pelland et al., 2025).
            </p>'''

# ----------------------------------------------------------------- POOL ----
pool_groups = [
  ("Vertical Pull", ["pullover", "pullover_1arm"]),
  ("Horizontal Pull", ["csr", "one_arm_row", "wide_row"]),
  ("Chest", ["incline_press", "flat_press", "fly", "incline_fly", "squeeze_press", "deep_pushup"]),
  ("Shoulders", ["oh_press", "arnold", "one_arm_press", "lat_raise", "lean_raise", "rear_fly", "rear_row"]),
  ("Traps", ["shrug", "high_pull", "y_raise", "upright_row"]),
  ("Triceps", ["oh_ext", "cg_press", "skull", "bench_dip", "kickback"]),
  ("Biceps", ["incline_curl", "hammer_curl", "incline_hammer", "conc_curl", "spider_curl"]),
  ("Forearms", ["wrist_curl", "rev_curl", "rev_wrist_curl"]),
  ("Core &amp; Carries", ["crunch", "leg_raise", "side_plank", "farmers", "suitcase"]),
  ("Legs", ["split_squat", "goblet_squat", "rdl", "ham_curl", "hip_thrust", "step_up", "calf", "seated_calf"]),
]
POOL_WHY = {
  "Vertical Pull": "The width that makes the waist look smaller. Absent entirely from the pre-v2 program.",
  "Horizontal Pull": "Mid-back thickness and rear-delt balance against all the pressing.",
  "Chest": "Upper, mid and stretched-position work. Incline leads because upper chest is what reads through a shirt.",
  "Shoulders": "All three heads every session: a press for the front, a raise for the side, a fly or row for the rear.",
  "Traps": "New in v3. Shrugs build the upper fibres; high pulls and Y raises build the mid and lower ones that hold posture.",
  "Triceps": "Two thirds of the arm. Every session pairs an overhead movement for the long head with a heavy press for the lateral.",
  "Biceps": "Stretched-position curls for the long head, neutral-grip work for the brachialis underneath it.",
  "Forearms": "New in v3. Wrist curls for the flexors, reverse curls for the extensors and the brachioradialis.",
  "Core &amp; Carries": "Loaded sets, not hundreds of unloaded reps. Carries add grip, traps and bracing for free.",
  "Legs": "Each leg muscle gets a stretched movement and a contracted one, same rule as the upper days.",
}
pool = []
for label, keys in pool_groups:
    names = []
    for k in keys:
        for tier in ("full", "band", "bw"):
            n = P.TIERS[k][tier][0]
            if n not in names:
                names.append(n)
    shown = ", ".join(names[:9]) + ("&hellip;" if len(names) > 9 else "")
    pool.append(f'''              <tr>
                <td class="exercise-name">{label}</td>
                <td>{shown}</td>
                <td>{POOL_WHY[label]}</td>
              </tr>''')
POOL = "            <tbody>\n" + "\n".join(pool) + "\n            </tbody>"

# ----------------------------------------------------------------- write ---
src = PAGE.read_text()
for name, body in (("CARDS", CARDS), ("WEEK", WEEK), ("VOLUME", VOLUME), ("POOL", POOL)):
    pattern = re.compile(r"<!-- GEN:%s -->\n.*?\n<!-- /GEN:%s -->" % (name, name), re.S)
    assert pattern.search(src), f"sentinel GEN:{name} not found in dumbbell.html"
    src = pattern.sub(lambda _m, b=body, n=name:
                      f"<!-- GEN:{n} -->\n{b}\n<!-- /GEN:{n} -->", src, count=1)
PAGE.write_text(src)
print(f"dumbbell.html regenerated: {total} sets/week, {len(vol)} muscles")
