# -*- coding: utf-8 -*-
import sys, io, os; sys.path.insert(0,'.')
import program as P

SITE = "/Users/richarddavidson/Desktop/Desktop - Mac/Claude/kettlebell-workout"
SUBNAV = [("dumbbell.html","Overview"),("strength.html","A &middot; Push (M)"),("hypertrophy.html","B &middot; Pull (W)"),
          ("metabolic.html","C &middot; Detail (F)"),("legs.html","Legs (Sat)"),
          ("db-exercises.html","Exercises"),("db-progression.html","Progression")]

RACK_RULE = '''        <div class="card rack-rule">
          <h3>The Rack Rule</h3>
          <p>You train in gyms where the dumbbells change week to week, so this program prescribes
          <strong>effort, not reps</strong>. The rep window is a guide. The RIR column is the actual instruction.</p>
          <ol>
            <li><strong>Take the heaviest pair you can control</strong> for at least the bottom of the window with clean form.</li>
            <li><strong>Stop at the listed reps in reserve</strong>, whatever rep number that lands on. That number is the output, not the target.</li>
            <li><strong>Sailed past the top of the window and still not close to failure?</strong> The weight was too light. Go up on the next set.</li>
            <li><strong>Nothing on the rack heavy enough?</strong> Work down this ladder, in order:
              slow the lowering to 4 seconds &rarr; add a 2-second pause at the deepest stretch &rarr;
              switch to one arm at a time &rarr; only then keep adding reps.</li>
          </ol>
          <p class="rack-why">Loads anywhere from 30% to 100% of your maximum build muscle equally well
          <em>provided the set finishes close to failure</em> (ACSM Position Stand, 2026). A light rack costs you
          nothing. Stopping early costs you everything.</p>
        </div>

'''

def nav(active):
    links="\n".join(f'        <a href="{h}"{" class=\"active\"" if h==active else ""}>{l}</a>' for h,l in SUBNAV)
    return f'''  <nav class="nav">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">RD's <span>Workout</span></a>
      <ul class="nav-links">
        <li><a href="index.html">Home</a></li>
        <li><a href="kettlebell.html">Kettlebell</a></li>
        <li><a href="dumbbell.html" class="active">Dumbbell</a></li>
        <li><a href="abs.html">Abs</a></li>
        <li><a href="nutrition.html">Nutrition</a></li>
      </ul>
      <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
  <div class="subnav">
    <div class="subnav-inner">
{links}
    </div>
  </div>
'''

def table(sess, tier):
    o=io.StringIO()
    o.write('''          <table>
            <thead>
              <tr><th>#</th><th>Exercise</th><th>Sets</th><th>Rep Window</th><th>Stop At</th><th>Notes</th><th>Demo</th></tr>
            </thead>
            <tbody>
''')
    for i,(key,sets,lo,hi,rir,note) in enumerate(sess["ex"],1):
        disp,anchor = P.TIERS[key][tier]
        timed = "sec" in disp
        window = "&mdash;" if timed else f"{lo}&ndash;{hi}"
        eff = "&mdash;" if timed else f'<strong>{rir} RIR</strong>'
        o.write(f'''              <tr>
                <td>{i}</td>
                <td class="exercise-name">{disp}</td>
                <td><strong>{sets}</strong></td>
                <td>{window}</td>
                <td>{eff}</td>
                <td>{note}</td>
                <td><a href="db-exercises.html#{anchor}" class="demo-link">Form Cues</a></td>
              </tr>
''')
    o.write("            </tbody>\n          </table>\n")
    return o.getvalue()

def build(sess):
    f=sess["file"]
    tabs="\n".join(f'          <button class="tier-tab{" active" if i==0 else ""}" data-tier="{k}">{lbl}</button>'
                   for i,(k,_,lbl,_) in enumerate(P.TIER_META))
    panels=""
    for i,(k,_,lbl,blurb) in enumerate(P.TIER_META):
        panels+=f'''        <div class="tier-panel{" active" if i==0 else ""}" data-tier="{k}">
          <p class="tier-blurb"><strong>{lbl}.</strong> {blurb}</p>
          <div class="table-wrap">
{table(sess,k)}          </div>
        </div>
'''
    nsets=sum(e[1] for e in sess["ex"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{sess["title"]} | DB Recomp Program</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body class="has-subnav">

{nav(f)}
  <main>
    <section class="day-hero {sess["hero"]}">
      <div class="container">
        <div class="day-tag">{sess["tag"]}</div>
        <h1>{sess["title"]}</h1>
        <div class="day-info">
          <div class="day-info-item"><strong>Goal:</strong> {sess["goal"]}</div>
          <div class="day-info-item"><strong>Rest:</strong> {sess["rest"]}</div>
          <div class="day-info-item"><strong>Effort:</strong> Stop at the listed RIR, not the listed reps</div>
          <div class="day-info-item"><strong>Time:</strong> {sess["time"]}</div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <p style="text-align:center; color:var(--gray-600); margin-bottom:1.5rem; font-size:0.9rem;">
          {sess["intro"]}
        </p>

{RACK_RULE}        <div class="tier-tabs">
{tabs}
        </div>

{panels}
        <div class="total-reps">{nsets} working sets &mdash; every one finishing at the listed reps in reserve</div>

        <div class="day-nav">
          <a href="{sess["prev"][0]}">{sess["prev"][1]}</a>
          <a href="{sess["nxt"][0]}">{sess["nxt"][1]}</a>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <p>RD's Workout &mdash; Science-Based Training &mdash; <strong>August 2026</strong></p>
  </footer>

  <script src="js/main.js"></script>
  <script>
    document.querySelectorAll('.tier-tab').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        var tier = btn.dataset.tier;
        document.querySelectorAll('.tier-tab').forEach(function (b) {{ b.classList.toggle('active', b === btn); }});
        document.querySelectorAll('.tier-panel').forEach(function (p) {{ p.classList.toggle('active', p.dataset.tier === tier); }});
        try {{ localStorage.setItem('rdTier', tier); }} catch (e) {{}}
      }});
    }});
    try {{
      var saved = localStorage.getItem('rdTier');
      if (saved) {{ var b = document.querySelector('.tier-tab[data-tier="' + saved + '"]'); if (b) b.click(); }}
    }} catch (e) {{}}
  </script>
</body>
</html>
'''

for s in P.SESSIONS.values():
    open(os.path.join(SITE, s["file"]), "w").write(build(s))
    print("wrote", s["file"])
