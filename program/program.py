# -*- coding: utf-8 -*-
"""Single source of truth for the recomp program v3 (complete-coverage).

v3 (2026-08-20): every muscle is trained in every session, by at least two
exercises, and the two are chosen to complement rather than duplicate each
other. The pairing rule throughout is **one movement that loads the muscle in
its stretched position, one that loads it short or from a different head**:

    chest      incline press (upper, stretched)   + fly (mid, stretch at the bottom)
    back       pullover (vertical)                + row (horizontal)
    shoulders  press (front) + raise (side)       + rear fly (rear) -- three heads
    traps      shrug (upper)                      + high pull / Y raise (mid, lower)
    triceps    overhead extension (long head)     + close-grip press (lateral)
    biceps     incline curl (long head stretched) + hammer / concentration
    forearms   wrist curl (flexors)               + reverse curl (extensors)

The specific exercises rotate across A, B and C, so each muscle sees six
different angles a week rather than the same two three times.

Evidence this rests on:
  * Regional hypertrophy is exercise-specific -- different exercises for the
    same muscle grow different regions of it, so two complementary movements
    beat one movement done twice (Zabaleta-Korta et al. 2023).
  * Training a muscle at long muscle lengths produces more growth than at short
    lengths, which is why every pair leads with the stretched movement
    (Pedrosa et al. 2022; Maeo et al. 2023 on the triceps long head).
  * Hypertrophy rises with weekly sets, about +0.24% per set around 12 sets,
    with diminishing but not negative returns beyond it (Pelland et al. 2025).
  * Load is not the variable that matters if the set finishes near failure
    (ACSM Position Stand 2026; Schoenfeld 2017), which is what makes the same
    program run on bands or on nothing.
  * Longer rest preserves per-set volume on compounds, so compounds get 2 min
    and isolation gets 90 sec (Grgic et al. 2017; Schoenfeld et al. 2016).

Each exercise row: (name_key, sets, rep_lo, rep_hi, rir, note)
Tier variants are looked up per name_key in TIERS.
"""

# name_key -> {tier: (display_name, form-cue anchor)}
TIERS = {
 # ---------------------------------------------------------------- chest ----
 "incline_press":  {"full":("Incline DB Press","incline-press"), "dbonly":("DB Floor Press","flat-press"),
                    "band":("Band Incline Press","band-incline-press"), "bw":("Decline Push-Up (feet on bed)","decline-push-up"), "kbl":("KB Floor Press","flat-press")},
 "flat_press":     {"full":("Flat DB Bench Press","flat-press"), "dbonly":("Wide-Grip DB Floor Press","flat-press"),
                    "band":("Band Chest Press","band-chest-press"), "bw":("Push-Up","push-up"), "kbl":("One-Arm KB Floor Press","flat-press")},
 "fly":            {"full":("DB Chest Fly","chest-fly"), "dbonly":("DB Floor Fly","chest-fly"),
                    "band":("Band Chest Fly","band-fly"), "bw":("Wide Push-Up","push-up"), "kbl":("KB Deficit Push-Up","kb-deficit-pushup")},
 "incline_fly":    {"full":("Incline DB Fly","incline-fly"), "dbonly":("DB Floor Fly (arms high)","chest-fly"),
                    "band":("Low-to-High Band Fly","band-fly"), "bw":("Sliding Chest Fly (towel)","sliding-fly"), "kbl":("KB Floor Fly","chest-fly")},
 "squeeze_press":  {"full":("Squeeze Press","squeeze-press"), "dbonly":("Squeeze Press (floor)","squeeze-press"),
                    "band":("Band Squeeze Press","band-chest-press"), "bw":("Archer Push-Up","archer-push-up"), "kbl":("KB Squeeze Press","squeeze-press")},
 "deep_pushup":    {"full":("Deficit Push-Up (on dumbbells)","deficit-pushup"), "dbonly":("Deficit Push-Up (on dumbbells)","deficit-pushup"),
                    "band":("Band-Resisted Push-Up","push-up"), "bw":("Deficit Push-Up (hands elevated)","deficit-pushup"), "kbl":("KB Deficit Push-Up","kb-deficit-pushup")},
 # ----------------------------------------------------------------- back ----
 "pullover":       {"full":("DB Pullover","pullover"), "dbonly":("DB Pullover (floor)","pullover"),
                    "band":("Band Lat Pulldown","band-pulldown"), "bw":("Sliding Lat Pullover (towel)","sliding-pullover"), "kbl":("KB Pullover (floor)","pullover")},
 "pullover_1arm":  {"full":("One-Arm DB Pullover","pullover"), "dbonly":("One-Arm DB Pullover (floor)","pullover"),
                    "band":("One-Arm Band Pulldown","band-pulldown"), "bw":("One-Arm Sliding Pullover","sliding-pullover"), "kbl":("One-Arm KB Pullover","pullover")},
 "csr":            {"full":("Chest-Supported Row","chest-supported-row"), "dbonly":("Bent-Over Two-DB Row","chest-supported-row"),
                    "band":("Band Seated Row","band-row"), "bw":("Door-Handle Row","door-row"), "kbl":("Bent-Over KB Row","chest-supported-row")},
 "one_arm_row":    {"full":("One-Arm DB Row","one-arm-row"), "dbonly":("One-Arm DB Row","one-arm-row"),
                    "band":("Band One-Arm Row","band-row"), "bw":("Towel Row (one arm)","towel-row"), "kbl":("One-Arm KB Row","one-arm-row")},
 "wide_row":       {"full":("Wide-Elbow Bench Row","wide-row"), "dbonly":("Wide-Elbow Bent-Over Row","wide-row"),
                    "band":("Band Wide Row (elbows high)","band-row"), "bw":("Wide-Grip Door Row","door-row"), "kbl":("Wide-Elbow KB Row","wide-row")},
 # ------------------------------------------------------------ shoulders ----
 "oh_press":       {"full":("Seated Overhead Press","oh-press"), "dbonly":("Standing Overhead Press","oh-press"),
                    "band":("Band Overhead Press","band-oh-press"), "bw":("Pike Push-Up (feet on bed)","pike-push-up"), "kbl":("KB Overhead Press","oh-press")},
 "arnold":         {"full":("Arnold Press","arnold-press"), "dbonly":("Arnold Press (standing)","arnold-press"),
                    "band":("Band Arnold Press","band-oh-press"), "bw":("Elevated Pike Push-Up","pike-push-up"), "kbl":("KB Arnold Press","arnold-press")},
 "one_arm_press":  {"full":("Half-Kneeling One-Arm Press","kb-half-kneeling-press"), "dbonly":("Half-Kneeling One-Arm Press","kb-half-kneeling-press"),
                    "band":("Half-Kneeling Band Press","band-oh-press"), "bw":("Assisted One-Arm Pike Push-Up","pike-push-up"), "kbl":("Half-Kneeling KB Press","kb-half-kneeling-press")},
 "lat_raise":      {"full":("Lateral Raise","lat-raise"), "dbonly":("Lateral Raise","lat-raise"),
                    "band":("Band Lateral Raise","band-lat-raise"), "bw":("Prone Y Raise","prone-raise"), "kbl":("KB Lateral Raise","lat-raise")},
 "lean_raise":     {"full":("Leaning Lateral Raise","lat-raise"), "dbonly":("Leaning Lateral Raise","lat-raise"),
                    "band":("One-Arm Band Lateral Raise","band-lat-raise"), "bw":("Side-Lying Arm Raise","prone-raise"), "kbl":("Leaning KB Lateral Raise","lat-raise")},
 "rear_fly":       {"full":("Bent-Over Rear Delt Fly","rear-fly"), "dbonly":("Bent-Over Rear Delt Fly","rear-fly"),
                    "band":("Band Reverse Fly","band-face-pull"), "bw":("Prone T Raise","prone-raise"), "kbl":("KB Rear Delt Fly","rear-fly")},
 "rear_row":       {"full":("Rear Delt Row (elbows high)","rear-fly"), "dbonly":("Rear Delt Row (elbows high)","rear-fly"),
                    "band":("Band Face Pull","band-face-pull"), "bw":("Prone Reverse Row","prone-raise"), "kbl":("KB High Pull","kb-high-pull")},
 # ---------------------------------------------------------------- traps ----
 "shrug":          {"full":("DB Shrug","shrug"), "dbonly":("DB Shrug","shrug"),
                    "band":("Band Shrug","shrug"), "bw":("Loaded Bag Shrug","shrug"), "kbl":("KB Shrug","shrug")},
 "high_pull":      {"full":("DB High Pull","kb-high-pull"), "dbonly":("DB High Pull","kb-high-pull"),
                    "band":("Band High Pull","band-face-pull"), "bw":("Prone W Raise","prone-raise"), "kbl":("KB High Pull","kb-high-pull")},
 "y_raise":        {"full":("Prone Y Raise (incline bench)","prone-raise"), "dbonly":("Prone Y Raise (floor)","prone-raise"),
                    "band":("Band Y Raise","band-face-pull"), "bw":("Prone Y Raise","prone-raise"), "kbl":("Prone Y Raise (light bell)","prone-raise")},
 "upright_row":    {"full":("Wide-Grip Upright Row","upright-row"), "dbonly":("Wide-Grip Upright Row","upright-row"),
                    "band":("Band Upright Row","band-face-pull"), "bw":("Wide Prone W Raise","prone-raise"), "kbl":("KB Upright Row","upright-row")},
 # -------------------------------------------------------------- triceps ----
 "oh_ext":         {"full":("OH Tricep Extension","oh-ext"), "dbonly":("OH Tricep Extension","oh-ext"),
                    "band":("Band OH Tricep Extension","band-pushdown"), "bw":("Sliding Tricep Extension (towel)","sliding-tricep"), "kbl":("KB Overhead Tricep Extension","oh-ext")},
 "cg_press":       {"full":("Close-Grip DB Press","close-grip-press"), "dbonly":("Close-Grip DB Floor Press","close-grip-press"),
                    "band":("Band Close-Grip Press","band-chest-press"), "bw":("Diamond Push-Up","diamond-push-up"), "kbl":("KB Close-Grip Floor Press","close-grip-press")},
 "skull":          {"full":("Skull Crusher","skull-crusher"), "dbonly":("DB Skull Crusher (floor)","skull-crusher"),
                    "band":("Band Skull Crusher","band-pushdown"), "bw":("Bodyweight Skull Crusher","skull-crusher"), "kbl":("KB Skull Crusher (floor)","skull-crusher")},
 "bench_dip":      {"full":("Bench Dip (feet elevated)","bed-dip"), "dbonly":("Bench Dip","bed-dip"),
                    "band":("Band Tricep Pushdown","band-pushdown"), "bw":("Bed-Edge Dip","bed-dip"), "kbl":("Loaded Bench Dip","bed-dip")},
 "kickback":       {"full":("Tricep Kickback","kickback"), "dbonly":("Tricep Kickback","kickback"),
                    "band":("Band Tricep Kickback","band-pushdown"), "bw":("Bed-Edge Dip","bed-dip"), "kbl":("KB Kickback","kickback")},
 # --------------------------------------------------------------- biceps ----
 "incline_curl":   {"full":("Incline Curl","incline-curl"), "dbonly":("Standing DB Curl","incline-curl"),
                    "band":("Band Curl","band-curl"), "bw":("Towel Curl (supinated)","towel-curl"), "kbl":("KB Curl","incline-curl")},
 "hammer_curl":    {"full":("Hammer Curl","hammer-curl"), "dbonly":("Hammer Curl","hammer-curl"),
                    "band":("Band Hammer Curl","band-curl"), "bw":("Towel Curl (neutral grip)","towel-curl"), "kbl":("KB Hammer Curl","hammer-curl")},
 "incline_hammer": {"full":("Incline Hammer Curl","hammer-curl"), "dbonly":("Standing Hammer Curl (slow lower)","hammer-curl"),
                    "band":("Staggered Band Hammer Curl","band-curl"), "bw":("One-Arm Towel Hammer Curl","towel-curl"), "kbl":("KB Incline Hammer Curl","hammer-curl")},
 "conc_curl":      {"full":("Concentration Curl","concentration-curl"), "dbonly":("Concentration Curl","concentration-curl"),
                    "band":("Band Concentration Curl","band-curl"), "bw":("Towel Concentration Curl","towel-curl"), "kbl":("KB Concentration Curl","concentration-curl")},
 "spider_curl":    {"full":("Spider Curl (chest on incline bench)","spider-curl"), "dbonly":("Prone Spider Curl (floor)","spider-curl"),
                    "band":("Band Spider Curl","band-curl"), "bw":("Towel Spider Curl","towel-curl"), "kbl":("KB Spider Curl","spider-curl")},
 # ------------------------------------------------------------- forearms ----
 "wrist_curl":     {"full":("Seated Wrist Curl","wrist-curl"), "dbonly":("Wrist Curl (forearm on knee)","wrist-curl"),
                    "band":("Band Wrist Curl","wrist-curl"), "bw":("Towel Wring (flexors)","towel-wring"), "kbl":("KB Wrist Curl","wrist-curl")},
 "rev_curl":       {"full":("Reverse Curl","reverse-curl"), "dbonly":("Reverse Curl","reverse-curl"),
                    "band":("Band Reverse Curl","reverse-curl"), "bw":("Towel Reverse Curl","towel-curl"), "kbl":("KB Reverse Curl","reverse-curl")},
 "rev_wrist_curl": {"full":("Reverse Wrist Curl","wrist-curl"), "dbonly":("Reverse Wrist Curl (on knee)","wrist-curl"),
                    "band":("Band Reverse Wrist Curl","wrist-curl"), "bw":("Towel Wring (extensors)","towel-wring"), "kbl":("KB Reverse Wrist Curl","wrist-curl")},
 # ----------------------------------------------------------------- core ----
 "crunch":         {"full":("Weighted Crunch","weighted-crunch"), "dbonly":("Weighted Crunch","weighted-crunch"),
                    "band":("Band Crunch","band-crunch"), "bw":("Hollow Body Hold (30 sec)","hollow-hold"), "kbl":("KB Weighted Crunch","weighted-crunch")},
 "leg_raise":      {"full":("Lying Leg Raise","leg-raise"), "dbonly":("Lying Leg Raise","leg-raise"),
                    "band":("Lying Leg Raise","leg-raise"), "bw":("Lying Leg Raise","leg-raise"), "kbl":("Lying Leg Raise","leg-raise")},
 "side_plank":     {"full":("Side Plank (30 sec/side)","side-plank"), "dbonly":("Side Plank (30 sec/side)","side-plank"),
                    "band":("Side Plank (30 sec/side)","side-plank"), "bw":("Side Plank (30 sec/side)","side-plank"), "kbl":("Side Plank (30 sec/side)","side-plank")},
 "farmers":        {"full":("Farmer's Walk (40 sec)","farmers-walk"), "dbonly":("Farmer's Walk (40 sec)","farmers-walk"),
                    "band":("Hollow Body Hold (30 sec)","hollow-hold"), "bw":("Suitcase Carry (40 sec)","farmers-walk"), "kbl":("Farmer's Walk (40 sec)","farmers-walk")},
 # ----------------------------------------------------------------- legs ----
 "split_squat":    {"full":("Bulgarian Split Squat","split-squat"), "dbonly":("Bulgarian Split Squat","split-squat"),
                    "band":("Band Split Squat","split-squat"), "bw":("Bulgarian Split Squat (BW)","split-squat"), "kbl":("KB Bulgarian Split Squat","split-squat")},
 "goblet_squat":   {"full":("Goblet Squat","goblet-squat"), "dbonly":("Goblet Squat","goblet-squat"),
                    "band":("Band Goblet Squat","goblet-squat"), "bw":("Sissy Squat","sissy-squat"), "kbl":("KB Goblet Squat","goblet-squat")},
 "rdl":            {"full":("DB Romanian Deadlift","rdl"), "dbonly":("DB Romanian Deadlift","rdl"),
                    "band":("Band Romanian Deadlift","rdl"), "bw":("Single-Leg Romanian Deadlift","rdl"), "kbl":("KB Romanian Deadlift","rdl")},
 "ham_curl":       {"full":("Sliding Leg Curl (towel)","ham-curl"), "dbonly":("Sliding Leg Curl (towel)","ham-curl"),
                    "band":("Band Leg Curl","ham-curl"), "bw":("Assisted Nordic Curl","ham-curl"), "kbl":("Sliding Leg Curl (towel)","ham-curl")},
 "hip_thrust":     {"full":("DB Hip Thrust","hip-thrust"), "dbonly":("DB Glute Bridge","glute-bridge"),
                    "band":("Band Glute Bridge","glute-bridge"), "bw":("Single-Leg Glute Bridge","glute-bridge"), "kbl":("KB Hip Thrust","hip-thrust")},
 "step_up":        {"full":("DB Step-Up","step-up"), "dbonly":("DB Step-Up","step-up"),
                    "band":("Band Step-Up","step-up"), "bw":("High Step-Up (BW)","step-up"), "kbl":("KB Step-Up","step-up")},
 "calf":           {"full":("Standing DB Calf Raise","calf-raise"), "dbonly":("Standing DB Calf Raise","calf-raise"),
                    "band":("Band Calf Raise","calf-raise"), "bw":("Single-Leg Calf Raise","calf-raise"), "kbl":("Standing KB Calf Raise","calf-raise")},
 "seated_calf":    {"full":("Seated DB Calf Raise","calf-raise"), "dbonly":("Seated DB Calf Raise","calf-raise"),
                    "band":("Seated Band Calf Raise","calf-raise"), "bw":("Seated Calf Raise (loaded bag)","calf-raise"), "kbl":("Seated KB Calf Raise","calf-raise")},
 "suitcase":       {"full":("Suitcase Carry (40 sec)","farmers-walk"), "dbonly":("Suitcase Carry (40 sec)","farmers-walk"),
                    "band":("Wall Sit (60 sec)","wall-sit"), "bw":("Wall Sit (60 sec)","wall-sit"), "kbl":("KB Suitcase Carry (40 sec)","farmers-walk")},
}

# Which (key, tier) combinations are timed holds or carries rather than rep
# work. Stated explicitly: the emitters used to infer this from "sec" appearing
# in the display name, which quietly turned "Standing Hammer Curl (4-sec lower)"
# into a timed exercise.
ALL_TIERS = frozenset({"full", "dbonly", "band", "bw", "kbl"})
TIMED = {
  "side_plank": ALL_TIERS,
  "farmers":    ALL_TIERS,   # walk, or a hollow hold on the band tier
  "suitcase":   ALL_TIERS,   # carry, or a wall sit on the band and bw tiers
  "crunch":     frozenset({"bw"}),   # becomes a hollow body hold
}


def is_timed(key, tier):
    return tier in TIMED.get(key, ())

# Which (key, tier) combinations carry no external load, stated explicitly
# rather than guessed from the exercise name. The "bw" tier is unloaded by
# definition and is not listed here. Anything absent is loaded, so the tracker
# asks for a weight.
NO_LOAD = {
  "leg_raise":   {"full", "dbonly", "band", "kbl"},   # bodyweight in every tier
  "side_plank":  {"full", "dbonly", "band", "kbl"},
  "deep_pushup": {"full", "dbonly", "kbl"},           # a push-up is a push-up
  "bench_dip":   {"full", "dbonly"},                  # kbl variant hangs a bell
  "ham_curl":    {"full", "dbonly", "kbl"},           # towel slide, no load
  "farmers":     {"band"},                            # becomes a hollow hold
  "suitcase":    {"band"},                            # becomes a wall sit
}

# Carries stay loaded even on the no-equipment tier -- he uses a bag.
LOAD_ON_BW = {"farmers"}

SESSIONS = {
"A": dict(
  file="strength.html", key="a", day="Monday", tag="Monday &mdash; Session A", title="Upper Body A",
  goal="Every upper-body muscle, heaviest available load, presses leading.",
  rest="2 min on the first four, 90 sec on everything after",
  time="~100 minutes", hero="strength",
  prev=("dumbbell.html","&larr; Overview"), nxt=("hypertrophy.html","B &middot; Row Lead &rarr;"),
  intro="Nothing gets skipped and nothing gets one lonely exercise. Chest, back, all three delt heads, traps, triceps, biceps, forearms and core all get worked, each by a pair that hits it two different ways. <strong>Reps are an output, not a target</strong> &mdash; take the heaviest pair on the rack and stop when you have 1-2 left.",
  ex=[
    ("pullover",     4,12, 20, "1-2", "Deep overhead stretch. Vertical pull, opens the session with the lats long."),
    ("incline_press",4, 8, 15, "1-2", "Your heaviest press. Lower to the chest, 1-sec pause, drive to lockout."),
    ("csr",          4,10, 15, "1-2", "Strict, no momentum. Squeeze the shoulder blades 1 sec at the top."),
    ("fly",          3,12, 20, "1-2", "Wide arc, deep stretch at the bottom. The stretch half is the half that grows chest."),
    ("oh_press",     3,10, 15, "1-2", "Press straight to lockout. Brace hard, no excess back arch."),
    ("lat_raise",    4,15, 25, "0-1", "Elbows lead, shoulder height only. Go to genuine failure here, it is safe."),
    ("rear_fly",     3,15, 25, "0-1", "Hinged 45&deg;, elbows lead. Rear delts hold the posture the shirt hangs on."),
    ("shrug",        3,12, 20, "1-2", "Straight up, 1-sec squeeze at the top. No rolling."),
    ("high_pull",    2,12, 20, "1-2", "Elbows high and outside. Mid traps and rear delts, which the shrug misses."),
    ("oh_ext",       3,12, 20, "1-2", "Deep stretch behind the head. The long head only grows in this position."),
    ("cg_press",     3,10, 20, "1-2", "Elbows tucked, DBs touching. Heavy lateral-head work to pair with the stretch above."),
    ("incline_curl", 3,10, 15, "1-2", "Arms hanging back for the full stretch. No swing."),
    ("hammer_curl",  3,12, 20, "1-2", "Neutral grip. Brachialis, which pushes the biceps up and thickens the arm."),
    ("wrist_curl",   2,15, 25, "0-1", "Forearms on the knees, let the bar roll to the fingertips, then curl."),
    ("rev_curl",     2,12, 20, "1-2", "Palms down. Brachioradialis and the extensors, the top half of the forearm."),
    ("crunch",       3,12, 20, "1-2", "Loaded and slow. Add weight before you add reps."),
    ("farmers",      3, 1,  1, "&mdash;", "Heaviest pair available. Walk tall, shoulders back."),
  ]),
"B": dict(
  file="hypertrophy.html", key="b", day="Wednesday", tag="Wednesday &mdash; Session B", title="Upper Body B",
  goal="Same complete coverage, rows leading and the unilateral variations.",
  rest="2 min on the first four, 90 sec on everything after",
  time="~95 minutes", hero="hypertrophy",
  prev=("strength.html","&larr; A &middot; Press Lead"), nxt=("metabolic.html","C &middot; Angles &rarr;"),
  intro="The same muscles as Monday, reached from different angles: one arm at a time on the back, a rotated press for the delts, and the contracted-position curl. <strong>Every rep is a stretch and a squeeze</strong> &mdash; full extension at the bottom, one-second hold at the top.",
  ex=[
    ("pullover_1arm",3,12, 20, "1-2", "One side at a time buys you several more inches of stretch. Per arm."),
    ("flat_press",   4,10, 15, "1-2", "Deep stretch at the bottom, press together at the top."),
    ("one_arm_row",  4,10, 15, "1-2", "Let the shoulder blade travel. Full stretch at the bottom, pull to the hip. Per arm."),
    ("incline_fly",  3,12, 20, "1-2", "Low to high. Hits the upper chest the flat fly cannot reach."),
    ("arnold",       3,12, 20, "1-2", "Rotate palms-in to palms-forward. All three delt heads in one path."),
    ("lean_raise",   4,15, 25, "0-1", "Lean away from a doorframe. Loads the side delt at the bottom, where the standing raise is easy."),
    ("rear_row",     3,15, 25, "0-1", "Elbows high and wide, pull toward the forehead line. Rear delt, not lat."),
    ("shrug",        3,12, 20, "1-2", "Straight up, 1-sec squeeze. Heavier than you think it needs to be."),
    ("y_raise",      2,15, 25, "0-1", "Thumbs up, arms to a Y. Lower traps, which nothing else in the week trains."),
    ("skull",        3,12, 20, "1-2", "Elbows tucked, lower beside the head. Long head under stretch."),
    ("bench_dip",    3,10, 20, "1-2", "Feet out, chest tall. Heavy lateral-head work with your bodyweight as the load."),
    ("incline_hammer",3,12, 20,"1-2", "Neutral grip with the arm hanging back. Brachialis in the stretched position."),
    ("conc_curl",    3,12, 20, "1-2", "Elbow braced on the thigh, squeeze hard at the top. The contracted half of the pair."),
    ("wrist_curl",   2,15, 25, "0-1", "Full roll to the fingertips. Grip strength shows up in every row you do."),
    ("rev_wrist_curl",2,15, 25,"0-1", "Palms down, small range, slow. Balances the flexor work above it."),
    ("leg_raise",    3,12, 20, "1-2", "Slow lower, low back pressed down."),
    ("side_plank",   3, 1,  1, "&mdash;", "Hips high, straight line. 30 sec each side."),
  ]),
"C": dict(
  file="metabolic.html", key="c", day="Friday", tag="Friday &mdash; Session C", title="Upper Body C",
  goal="Same coverage again, high reps and the angles the first two days missed.",
  rest="2 min on the first four, 90 sec on everything after",
  time="~95 minutes", hero="metabolic",
  prev=("hypertrophy.html","&larr; B &middot; Row Lead"), nxt=("legs.html","Legs &rarr;"),
  intro="The highest-rep day, and the one least affected by what is on the rack. Loads of 30% of your max build muscle just as well as heavy ones <em>provided the set ends near failure</em>. On this day most sets end at 0-2 reps in reserve.",
  ex=[
    ("pullover",     4,15, 25, "0-1", "Higher reps than Monday, same deep stretch. Lats, not arms."),
    ("squeeze_press",4,12, 20, "1-2", "Press the DBs hard together the whole set. Constant tension, inner chest."),
    ("wide_row",     4,12, 20, "1-2", "Elbows wide, pull to the sternum. Upper back width rather than thickness."),
    ("deep_pushup",  3,10, 20, "0-1", "Hands on the dumbbells so the chest drops below them. Stretch under load."),
    ("one_arm_press",3,12, 20, "1-2", "Half-kneeling, one arm. The core has to stop you leaning, so it earns its keep."),
    ("lat_raise",    4,15, 25, "0-1", "Four sets again. Side delts are the width the shirt actually shows."),
    ("rear_fly",     3,15, 25, "0-1", "Squeeze the shoulder blades. Posture and the rear look."),
    ("shrug",        3,15, 25, "0-1", "Higher reps, same 1-sec hold at the top."),
    ("upright_row",  2,12, 20, "1-2", "Wide grip, elbows to shoulder height only. Traps and side delts together."),
    ("oh_ext",       3,15, 25, "0-1", "Deep stretch behind the head, high reps."),
    ("kickback",     3,15, 25, "0-1", "Upper arm locked parallel to the floor, squeeze straight. Peak contraction."),
    ("incline_curl", 3,12, 20, "1-2", "Supinated and stretched, arms hanging back."),
    ("spider_curl",  3,12, 20, "0-1", "Chest supported, arms hanging straight down. Nowhere to hide, no swing possible."),
    ("wrist_curl",   2,15, 25, "0-1", "Slow and full range. The forearms are worked three times a week now."),
    ("rev_curl",     2,15, 25, "0-1", "Palms down, thumbs alongside. Brachioradialis for forearm width."),
    ("crunch",       3,15, 25, "0-1", "Loaded and slow. Abs are a muscle, so train them like one."),
    ("leg_raise",    3,15, 25, "0-1", "Slow lower, low back pressed down."),
  ]),
"LEGS": dict(
  file="legs.html", key="legs", day="Saturday", tag="Saturday &mdash; Session D", title="Legs + Calves",
  goal="Two exercises per leg muscle, same as everywhere else in the week.",
  rest="2 min on the first four, 90 sec on everything after",
  time="~55 minutes", hero="strength",
  prev=("metabolic.html","&larr; C &middot; Angles"), nxt=("db-progression.html","Progression &rarr;"),
  intro="Quads, hamstrings, glutes and calves each get a pair, on the same principle as the upper days: one movement that loads the muscle long, one that loads it short. <strong>If a week goes sideways, this is the session to drop.</strong> Never drop Monday.",
  ex=[
    ("split_squat", 4,10, 20, "1-2", "Rear foot on a bench, chair, or the bed. Deep, quad under stretch. Per leg."),
    ("goblet_squat",3,12, 20, "1-2", "Elbows inside the knees, sit straight down. The bilateral load the split squat cannot carry."),
    ("rdl",         4,10, 20, "1-2", "Hinge, soft knees, deep hamstring stretch. Hamstrings at long length."),
    ("ham_curl",    3,10, 20, "0-1", "Heels on a towel, hips high, drag them in. Knee flexion, which the RDL never trains."),
    ("hip_thrust",  3,12, 20, "1-2", "Shoulders elevated, drive the hips up, 1-sec squeeze. Glutes in the short position."),
    ("step_up",     3,12, 20, "1-2", "High step, drive through the front heel, no push off the back foot. Per leg."),
    ("calf",        3,15, 25, "0-1", "Knee straight, full stretch at the bottom, 1-sec squeeze at the top. Gastrocnemius."),
    ("seated_calf", 3,15, 25, "0-1", "Knee bent 90&deg;. Bending the knee switches the work to the soleus underneath."),
    ("suitcase",    3, 1,  1, "&mdash;", "One side, walk tall, resist the lean."),
  ]),
}

TIER_META = [
  ("full",   "full",   "Dumbbells + Bench",   "The default. Every movement at full range."),
  ("dbonly", "dbonly", "Dumbbells, No Bench", "Floor presses replace bench work. Slightly shorter range at the bottom, same stimulus."),
  ("band",   "band",   "Bands Only",          "Anchor in a door hinge. Step further from the anchor to add tension; log the band's rated pounds."),
  ("bw",     "bw",     "No Equipment",        "Hotel room. Bed, desk, door, towel. Progress by changing leverage before adding reps."),
  ("kbl",    "kbl",    "Kettlebells",         "One or two bells. Load jumps are huge, so tempo and pauses carry the progression between bells."),
]

# --- Muscle map, used to count weekly volume honestly -----------------------
# Every exercise key belongs to exactly one primary muscle. The overview page's
# volume table is generated from this, so it can never drift from the sessions.
MUSCLE = {
  "chest":     ["incline_press", "flat_press", "fly", "incline_fly", "squeeze_press", "deep_pushup"],
  "back":      ["pullover", "pullover_1arm", "csr", "one_arm_row", "wide_row"],
  "front delt":["oh_press", "arnold", "one_arm_press"],
  "side delt": ["lat_raise", "lean_raise"],
  "rear delt": ["rear_fly", "rear_row"],
  "traps":     ["shrug", "high_pull", "y_raise", "upright_row"],
  "triceps":   ["oh_ext", "cg_press", "skull", "bench_dip", "kickback"],
  "biceps":    ["incline_curl", "hammer_curl", "incline_hammer", "conc_curl", "spider_curl"],
  "forearms":  ["wrist_curl", "rev_curl", "rev_wrist_curl"],
  "core":      ["crunch", "leg_raise", "side_plank", "farmers"],
  "quads":     ["split_squat", "goblet_squat"],
  "hamstrings":["rdl", "ham_curl"],
  "glutes":    ["hip_thrust", "step_up"],
  "calves":    ["calf", "seated_calf"],
}


def weekly_sets() -> dict[str, int]:
    """Weekly working sets per muscle, counted from the sessions themselves."""
    owner = {k: m for m, keys in MUSCLE.items() for k in keys}
    totals: dict[str, int] = {m: 0 for m in MUSCLE}
    for sess in SESSIONS.values():
        for key, sets, *_ in sess["ex"]:
            if key == "suitcase":      # carry, counted with core
                totals["core"] += sets
                continue
            totals[owner[key]] += sets
    return totals


if __name__ == "__main__":
    total = 0
    for sess_key, sess in SESSIONS.items():
        n = sum(e[1] for e in sess["ex"])
        total += n
        print(f"{sess_key:5} {len(sess['ex']):2} exercises  {n:3} sets")
    print(f"{'TOTAL':5} {'':2}             {total:3} sets/week\n")
    for muscle, n in weekly_sets().items():
        print(f"  {muscle:11} {n:3}")
