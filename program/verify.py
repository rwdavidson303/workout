# -*- coding: utf-8 -*-
"""Assert the site and the tracker agree, and that the data invariants hold.

The previous version of this check anchored on data-tier="..." , which matched
the tier TAB button before the tier PANEL and captured a region with no exercise
rows in it. Comparing an empty list to anything passes, so it reported success
without ever comparing a name. Anchor on the panel and assert the row count.
"""
import re, sys, html as H
sys.path.insert(0, "/Users/richarddavidson/Desktop/Desktop - Mac/Claude/sofi")
sys.path.insert(0, ".")
from sofi.workout.models import DB_PLANS
import program as P

PRE = {"full": "db", "dbonly": "dbo", "band": "bnd", "bw": "bw", "kbl": "kbl"}
PANEL = re.compile(r'<div class="tier-panel[^"]*" data-tier="([a-z]+)">(.*?)\n        </div>\n', re.S)
NAME = re.compile(r'<td class="exercise-name">(.*?)</td>')
SETS = re.compile(r'<td><strong>(\d+)</strong></td>')

bad, compared = [], 0
for s in P.SESSIONS.values():
    html = open("../" + s["file"]).read()
    panels = dict((m.group(1), m.group(2)) for m in PANEL.finditer(html))
    if set(panels) != set(PRE):
        bad.append(f'{s["file"]}: panels found {sorted(panels)}, expected {sorted(PRE)}')
        continue
    for tier, prefix in PRE.items():
        wt = f'{prefix}_{s["key"]}'
        plan = DB_PLANS[wt]
        site_names = [H.unescape(x) for x in NAME.findall(panels[tier])]
        site_sets = [int(x) for x in SETS.findall(panels[tier])]
        plan_names = [H.unescape(e.name) for e in plan.exercises]
        plan_sets = [e.sets for e in plan.exercises]
        if not site_names:
            bad.append(f"{wt}: no exercise rows parsed from the site")
        if len(site_names) != len(plan_names):
            bad.append(f"{wt}: site {len(site_names)} rows vs tracker {len(plan_names)}")
        for i, (a, b) in enumerate(zip(site_names, plan_names), 1):
            if a != b:
                bad.append(f"{wt} #{i}: site '{a}' vs tracker '{b}'")
        for i, (a, b) in enumerate(zip(site_sets, plan_sets), 1):
            if a != b:
                bad.append(f"{wt} #{i}: site {a} sets vs tracker {b} sets")
        compared += len(plan_names)

for k, plan in DB_PLANS.items():
    names = [e.name for e in plan.exercises]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        bad.append(f"{k}: DUPLICATE exercise names {dupes}")
    for e in plan.exercises:
        if "&" in e.name or ";" in e.name:
            bad.append(f"{k}: HTML entity in database key '{e.name}'")
        if not e.is_timed and not e.reps_max:
            bad.append(f"{k}: '{e.name}' has no rep window")

# Every muscle must appear at least twice in every upper session.
UPPER = {m: keys for m, keys in P.MUSCLE.items()
         if m not in ("quads", "hamstrings", "glutes", "calves")}
for sk in ("A", "B", "C"):
    keys = [e[0] for e in P.SESSIONS[sk]["ex"]]
    for muscle, members in UPPER.items():
        n = sum(1 for k in keys if k in members)
        if muscle in ("front delt", "side delt", "rear delt"):
            continue          # the three heads together make up the shoulder pair
        if n < 2:
            bad.append(f"session {sk}: {muscle} has only {n} exercise(s)")
    delts = sum(1 for k in keys if k in P.MUSCLE["front delt"]
                + P.MUSCLE["side delt"] + P.MUSCLE["rear delt"])
    if delts < 2:
        bad.append(f"session {sk}: shoulders have only {delts} exercise(s)")

if bad:
    print("\n".join(bad))
    sys.exit(1)
print(f"PASS: {compared} exercise rows compared across {len(DB_PLANS)} plans")
print("      site == tracker, no duplicate names, no entities, "
      "every muscle >= 2 exercises per session")
