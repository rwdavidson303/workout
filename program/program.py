# -*- coding: utf-8 -*-
"""Single source of truth for the recomp program v2 (effort-anchored).

Each exercise: (name_key, sets, rep_lo, rep_hi, rir, note, anchor)
Tier variants are looked up per name_key in TIERS.
"""

# name_key -> {tier: (display_name, anchor)}
TIERS = {
 "incline_press":  {"full":("Incline DB Press","incline-press"), "dbonly":("DB Floor Press","flat-press"),
                    "band":("Band Incline Press","band-chest-press"), "bw":("Decline Push-Up (feet on bed)","decline-push-up"), "kbl":('KB Floor Press','flat-press')},
 "flat_press":     {"full":("Flat DB Bench Press","flat-press"), "dbonly":("Wide-Grip DB Floor Press","flat-press"),
                    "band":("Band Chest Press","band-chest-press"), "bw":("Push-Up","push-up"), "kbl":('One-Arm KB Floor Press','flat-press')},
 "fly":            {"full":("DB Chest Fly","chest-fly"), "dbonly":("DB Floor Fly","chest-fly"),
                    "band":("Band Chest Fly","band-fly"), "bw":("Wide Push-Up","push-up"), "kbl":('KB Deficit Push-Up','kb-deficit-pushup')},
 "csr":            {"full":("Chest-Supported Row","chest-supported-row"), "dbonly":("Bent-Over Two-DB Row","chest-supported-row"),
                    "band":("Band Seated Row","band-row"), "bw":("Door-Handle Row","door-row"), "kbl":('Bent-Over KB Row','chest-supported-row')},
 "one_arm_row":    {"full":("One-Arm DB Row","one-arm-row"), "dbonly":("One-Arm DB Row","one-arm-row"),
                    "band":("Band One-Arm Row","band-row"), "bw":("Towel Row (one arm)","towel-row"), "kbl":('One-Arm KB Row','one-arm-row')},
 "pullover":       {"full":("DB Pullover","pullover"), "dbonly":("DB Pullover (floor)","pullover"),
                    "band":("Band Lat Pulldown","band-pulldown"), "bw":("Sliding Lat Pullover (towel)","sliding-pullover"), "kbl":('KB Pullover (floor)','pullover')},
 "oh_press":       {"full":("Seated Overhead Press","oh-press"), "dbonly":("Standing Overhead Press","oh-press"),
                    "band":("Band Overhead Press","band-oh-press"), "bw":("Pike Push-Up (feet on bed)","pike-push-up"), "kbl":('KB Overhead Press','oh-press')},
 "arnold":         {"full":("Arnold Press","arnold-press"), "dbonly":("Arnold Press (standing)","arnold-press"),
                    "band":("Band Overhead Press","band-oh-press"), "bw":("Pike Push-Up (feet on bed)","pike-push-up"), "kbl":('Half-Kneeling KB Press','kb-half-kneeling-press')},
 "lat_raise":      {"full":("Lateral Raise","lat-raise"), "dbonly":("Lateral Raise","lat-raise"),
                    "band":("Band Lateral Raise","band-lat-raise"), "bw":("Prone Y Raise","prone-raise"), "kbl":('KB Lateral Raise','lat-raise')},
 "rear_fly":       {"full":("Bent-Over Rear Delt Fly","rear-fly"), "dbonly":("Bent-Over Rear Delt Fly","rear-fly"),
                    "band":("Band Face Pull","band-face-pull"), "bw":("Prone T Raise","prone-raise"), "kbl":('KB High Pull','kb-high-pull')},
 "cg_press":       {"full":("Close-Grip DB Press","close-grip-press"), "dbonly":("Close-Grip DB Floor Press","close-grip-press"),
                    "band":("Band Close-Grip Press","band-chest-press"), "bw":("Diamond Push-Up","diamond-push-up"), "kbl":('KB Close-Grip Floor Press','close-grip-press')},
 "skull":          {"full":("Skull Crusher","skull-crusher"), "dbonly":("DB Skull Crusher (floor)","skull-crusher"),
                    "band":("Band Tricep Pushdown","band-pushdown"), "bw":("Bed-Edge Dip","bed-dip"), "kbl":('KB Skull Crusher (floor)','skull-crusher')},
 "oh_ext":         {"full":("OH Tricep Extension","oh-ext"), "dbonly":("OH Tricep Extension","oh-ext"),
                    "band":("Band OH Tricep Extension","band-pushdown"), "bw":("Diamond Push-Up","diamond-push-up"), "kbl":('KB Overhead Tricep Extension','oh-ext')},
 "incline_curl":   {"full":("Incline Curl","incline-curl"), "dbonly":("Standing DB Curl","incline-curl"),
                    "band":("Band Curl","band-curl"), "bw":("Towel Curl (supinated)","towel-curl"), "kbl":('KB Curl','incline-curl')},
 "hammer_curl":    {"full":("Hammer Curl","hammer-curl"), "dbonly":("Hammer Curl","hammer-curl"),
                    "band":("Band Hammer Curl","band-curl"), "bw":("Towel Curl (neutral grip)","towel-curl"), "kbl":('KB Hammer Curl','hammer-curl')},
 "crunch":         {"full":("Weighted Crunch","weighted-crunch"), "dbonly":("Weighted Crunch","weighted-crunch"),
                    "band":("Band Crunch","band-crunch"), "bw":("Hollow Body Hold (30 sec)","hollow-hold"), "kbl":('KB Weighted Crunch','weighted-crunch')},
 "leg_raise":      {"full":("Lying Leg Raise","leg-raise"), "dbonly":("Lying Leg Raise","leg-raise"),
                    "band":("Lying Leg Raise","leg-raise"), "bw":("Lying Leg Raise","leg-raise"), "kbl":('Lying Leg Raise','leg-raise')},
 "side_plank":     {"full":("Side Plank (30 sec/side)","side-plank"), "dbonly":("Side Plank (30 sec/side)","side-plank"),
                    "band":("Side Plank (30 sec/side)","side-plank"), "bw":("Side Plank (30 sec/side)","side-plank"), "kbl":('Side Plank (30 sec/side)','side-plank')},
 "farmers":        {"full":("Farmer's Walk (40 sec)","farmers-walk"), "dbonly":("Farmer's Walk (40 sec)","farmers-walk"),
                    "band":("Hollow Body Hold (30 sec)","hollow-hold"), "bw":("Suitcase Carry (40 sec)","farmers-walk"), "kbl":("Farmer's Walk (40 sec)",'farmers-walk')},
 # legs
 "split_squat":    {"full":("Bulgarian Split Squat","split-squat"), "dbonly":("Bulgarian Split Squat","split-squat"),
                    "band":("Band Split Squat","split-squat"), "bw":("Bulgarian Split Squat (BW)","split-squat"), "kbl":('KB Bulgarian Split Squat','split-squat')},
 "rdl":            {"full":("DB Romanian Deadlift","rdl"), "dbonly":("DB Romanian Deadlift","rdl"),
                    "band":("Band Romanian Deadlift","rdl"), "bw":("Single-Leg Romanian Deadlift","rdl"), "kbl":('KB Romanian Deadlift','rdl')},
 "rev_lunge":      {"full":("Reverse Lunge","reverse-lunge"), "dbonly":("Reverse Lunge","reverse-lunge"),
                    "band":("Band Reverse Lunge","reverse-lunge"), "bw":("Reverse Lunge (BW)","reverse-lunge"), "kbl":('KB Reverse Lunge','reverse-lunge')},
 "calf":           {"full":("DB Calf Raise","calf-raise"), "dbonly":("DB Calf Raise","calf-raise"),
                    "band":("Band Calf Raise","calf-raise"), "bw":("Calf Raise (BW)","calf-raise"), "kbl":('KB Calf Raise','calf-raise')},
 "glute_bridge":   {"full":("DB Glute Bridge","glute-bridge"), "dbonly":("DB Glute Bridge","glute-bridge"),
                    "band":("Band Glute Bridge","glute-bridge"), "bw":("Single-Leg Glute Bridge","glute-bridge"), "kbl":('Kettlebell Swings','kb-swing')},
 "suitcase":       {"full":("Suitcase Carry (40 sec)","farmers-walk"), "dbonly":("Suitcase Carry (40 sec)","farmers-walk"),
                    "band":("Wall Sit (60 sec)","wall-sit"), "bw":("Wall Sit (60 sec)","wall-sit"), "kbl":('KB Suitcase Carry (40 sec)','farmers-walk')},
}

TIMED = {"farmers", "side_plank", "suitcase"}
TIMED_BW_ALSO = {"crunch"}   # crunch -> hollow hold on bw tier only
BODYWEIGHT_KEYS = {"leg_raise", "side_plank"}   # always bodyweight in every tier

SESSIONS = {
"A": dict(
  file="strength.html", key="a", day="Monday", tag="Monday &mdash; Session A", title="Push-Lead Upper",
  goal="Add upper-body muscle. Heaviest available load, taken close to failure.",
  rest="90 sec between sets", time="~60 minutes", hero="strength",
  prev=("dumbbell.html","&larr; Overview"), nxt=("hypertrophy.html","B &middot; Pull-Lead &rarr;"),
  intro="The session that builds the most muscle. <strong>Reps are an output, not a target.</strong> Take the heaviest pair on the rack and stop when you have 1-2 reps left, whatever number that lands on. If you sail past the top of the window, the weight was too light &mdash; go up next set.",
  ex=[
    ("incline_press", 4, 8, 15, "1-2", "Your heaviest press. Lower to the chest, 1-sec pause, drive to lockout."),
    ("csr",           4,10, 15, "1-2", "Strict, no momentum. Squeeze the shoulder blades 1 sec at the top."),
    ("flat_press",    3,10, 15, "1-2", "Deep stretch at the bottom, press together at the top."),
    ("one_arm_row",   3,10, 15, "1-2", "Full stretch at the bottom, pull to the hip. Per arm."),
    ("oh_press",      3,10, 15, "1-2", "Press straight to lockout. Brace hard, no excess back arch."),
    ("lat_raise",     3,15, 25, "0-1", "Elbows lead, shoulder height only. Go to genuine failure here, it is safe."),
    ("cg_press",      3,10, 20, "1-2", "Elbows tucked, DBs touching. Triceps mass that the program was missing."),
    ("skull",         3,10, 15, "1-2", "Elbows tucked, lower beside the head. Long head under stretch."),
    ("incline_curl",  3,10, 15, "1-2", "Arms hanging back for the full stretch. No swing."),
    ("crunch",        3,12, 20, "1-2", "Loaded and slow. Add weight before you add reps."),
    ("farmers",       3, 1,  1, "&mdash;", "Heaviest pair available. Walk tall, shoulders back."),
  ]),
"B": dict(
  file="hypertrophy.html", key="b", day="Wednesday", tag="Wednesday &mdash; Session B", title="Pull-Lead Upper",
  goal="Build the back and rear delts. Width is what makes the waist read smaller.",
  rest="90 sec between sets", time="~50 minutes", hero="hypertrophy",
  prev=("strength.html","&larr; A &middot; Push-Lead"), nxt=("metabolic.html","C &middot; Detail &rarr;"),
  intro="Back leads. <strong>Every rep is a stretch and a squeeze</strong>: full extension at the bottom, one-second hold at the contraction. If the rack is light, slow the lowering to four seconds rather than adding reps forever.",
  ex=[
    ("pullover",     3,12, 20, "1-2", "Deep overhead stretch, pull over the chest. Lats, not arms."),
    ("csr",          4,12, 20, "1-2", "Elbows wide for upper back. Hold the squeeze."),
    ("one_arm_row",  3,12, 20, "1-2", "Let the shoulder blade travel. Per arm."),
    ("incline_press",3,12, 20, "1-2", "Full range, 1-sec pause at the chest stretch."),
    ("rear_fly",     4,15, 25, "0-1", "Hinged 45&deg;, elbows lead. Rear delts were the weakest link, hence four sets."),
    ("hammer_curl",  3,12, 20, "1-2", "Neutral grip. Builds arm thickness, not just the peak."),
    ("oh_ext",       3,12, 20, "1-2", "Deep stretch behind the head. Long head of the triceps."),
    ("leg_raise",    3,12, 20, "1-2", "Slow lower, low back pressed down."),
  ]),
"C": dict(
  file="metabolic.html", key="c", day="Friday", tag="Friday &mdash; Session C", title="Detail Upper",
  goal="Delts and arms at high reps, where a light rack is no disadvantage at all.",
  rest="75 sec between sets", time="~55 minutes", hero="metabolic",
  prev=("hypertrophy.html","&larr; B &middot; Pull-Lead"), nxt=("legs.html","Legs &rarr;"),
  intro="The highest-rep session, and the one least affected by what is on the rack. Loads of 30% of your max build muscle just as well as heavy ones <em>provided the set ends near failure</em>. On this day, that means most sets end at 0-2 reps in reserve.",
  ex=[
    ("incline_press",3,12, 20, "1-2", "Full range, pause at the stretch."),
    ("fly",          3,12, 20, "1-2", "Wide arc, deep stretch, squeeze at the top."),
    ("csr",          3,12, 20, "1-2", "Strict rowing, hold the contraction."),
    ("arnold",       3,12, 20, "1-2", "Rotate palms-in to palms-forward. All three delt heads."),
    ("lat_raise",    4,15, 25, "0-1", "Four sets. Side delts are the width the shirt shows."),
    ("rear_fly",     3,15, 25, "0-1", "Squeeze the shoulder blades. Posture and the rear look."),
    ("skull",        3,12, 20, "1-2", "Elbows tucked, long-head stretch."),
    ("oh_ext",       3,12, 20, "1-2", "Second triceps movement, different angle."),
    ("hammer_curl",  3,12, 20, "1-2", "Neutral grip, elbows pinned."),
    ("incline_curl", 3,12, 20, "1-2", "Supinated and stretched. Different angle to the hammer."),
    ("side_plank",   3, 1,  1, "&mdash;", "Hips high, straight line. 30 sec each side."),
  ]),
"LEGS": dict(
  file="legs.html", key="legs", day="Saturday", tag="Saturday &mdash; Session D", title="Legs + Carries",
  goal="Maintain the legs in half an hour. Deliberately a maintenance dose.",
  rest="90 sec between sets", time="~30 minutes", hero="strength",
  prev=("metabolic.html","&larr; C &middot; Detail"), nxt=("db-progression.html","Progression &rarr;"),
  intro="Nine hard leg sets a week holds what you have while the upper body gets the attention. <strong>If a week goes sideways, this is the session to drop.</strong> Never drop Monday.",
  ex=[
    ("split_squat", 3,10, 20, "1-2", "Rear foot on a bench, chair, or the bed. Per leg."),
    ("rdl",         3,10, 20, "1-2", "Hinge, soft knees, deep hamstring stretch."),
    ("rev_lunge",   3,12, 20, "1-2", "Step back, drive through the front heel. Per leg."),
    ("glute_bridge",3,15, 25, "1-2", "Drive the hips up, squeeze 1 sec at the top."),
    ("calf",        3,15, 25, "0-1", "Full stretch at the bottom, 1-sec squeeze at the top."),
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
