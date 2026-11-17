"""Genera il sito: index.html, 404.html e i reindirizzamenti dai vecchi indirizzi.

Uso: python3 _build/build.py
Testi e immagini della pagina sono in questo file; lo stile in assets/css/style.css,
le interazioni in assets/js/main.js.
"""
import json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
M = json.load(open(os.path.join(HERE, "manifest.json")))

IG = "https://www.instagram.com/dsgn.pop/"
IG_ME = "https://www.instagram.com/l0renx0/"
LI = "https://www.linkedin.com/in/lorenzo-devicienti-5a5669278/"
TIKTOK = "https://vm.tiktok.com/ZNRYW8jPm/"
ARROW = '<svg width="11" height="11" viewBox="0 0 14 14" aria-hidden="true"><path d="M3 11 11 3M4.5 3H11v6.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'


SITE = "https://l0renx0.github.io/LorenzoWebSite/"


def src(f):
    return "assets/img/" + f


def img(f, alt, lazy=True, extra=""):
    path = os.path.join(REPO, src(f))
    w, h = Image.open(path).size
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{src(f)}" alt="{alt}" width="{w}" height="{h}"{l}{extra}>'


def series(y):
    g = sorted([x for x in M["photo_d"] if x["y"] == y], key=lambda x: x["x"])
    i = next((k for k, x in enumerate(g) if x["x"] >= 200), 0)
    return [x["file"] for x in g[i:] + g[:i]]


apm, felina, portraits = series(860), series(2065), series(3365)
graphics = [x["file"] for x in M["graphics_d"]]
web = [x["file"] for x in M["web_site_d"]]
about = [x["file"] for x in M["about_d"]]

# --- Nastro iniziale
strip_files = [portraits[0], graphics[1], "vid-goal.jpg", apm[1], "poster-echoverse.jpg", felina[1],
               portraits[1], "vid-thuram.jpg", graphics[0], apm[0], "poster-jago.jpg", portraits[2]]
strip = "".join(img(f, "") for f in strip_files)
strip_html = f'<div class="strip" aria-hidden="true"><div class="strip__track">{strip}{strip}</div></div>'

# --- Galleria foto
figs = []
for key, label, files in [("apm", "AtleticProgettoMontagna", apm), ("felina", "Felina F.C.", felina), ("portraits", "Portraits", portraits)]:
    for i, f in enumerate(files):
        pick = "1" if i < 4 else "0"
        figs.append(f'<figure data-series="{key}" data-pick="{pick}" tabindex="0">{img(f, f"{label} — photo {i+1}")}<figcaption class="mono">{label}</figcaption></figure>')
gallery = "\n        ".join(figs)
total = len(apm) + len(felina) + len(portraits)

# --- Poster
posters = "\n        ".join(
    f'<figure class="poster">{img(f, f"Graphic post {i+1:02d}")}<p class="mono"><span>{i+1:02d}</span><span class="dim">/ {len(graphics):02d}</span></p></figure>'
    for i, f in enumerate(graphics))

# --- Telefoni
phones = "\n        ".join(f'<figure class="phone">{img(f, a)}</figure>' for f, a in [
    ("vid-goal.jpg", "Edit frame: “Goal” title over Marcus Thuram"),
    ("vid-tutu.jpg", "Edit frame: “Tu-Tu” title with the player on a yellow background"),
    ("vid-celebration.jpg", "Edit frame: team celebration"),
    ("vid-thuram.jpg", "Edit frame: “Thuram” title in the stadium at night")])

# --- Browser
def browser(f, url, name, href):
    return (f'<figure class="browser rv"><div class="browser__bar"><span class="browser__dots"><i></i><i></i><i></i></span>'
            f'<span class="browser__url mono">{url}</span></div>{img(f, name + " website")}'
            f'<figcaption><span>{name}</span><a class="mono ulink" href="{href}" target="_blank" rel="noopener">Visit {ARROW}</a></figcaption></figure>')
browsers = "\n        ".join([
    browser("web-apm.jpg", "atleticprogettomontagna.it", "AtleticProgettoMontagna", "https://www.atleticprogettomontagna.it"),
    browser(web[0], "aglf.academy", "AGLF Education", "https://www.aglf.academy"),
    browser(web[3], "comune.castelnovo-nemonti.re.it", "Castelnovo ne’ Monti", "https://www.comune.castelnovo-nemonti.re.it"),
    browser(web[4], "comune.casina.re.it", "Casina", "https://www.comune.casina.re.it"),
    browser(web[5], "comune.villa-minozzo.re.it", "Villa Minozzo", "https://www.comune.villa-minozzo.re.it"),
])

preview = "".join(img(f, "", lazy=False, extra=f' data-key="{k}"') for k, f in
                  [("photo", portraits[0]), ("graphics", graphics[1]), ("video", "vid-goal.jpg"), ("web", web[3])])

html = f"""<!doctype html>
<html lang="@@HTMLLANG@@" @@JSDATA@@>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Lorenzo Devicienti · Photo, Graphics, Video & Web</title>
<meta name="description" content="Lorenzo Devicienti: photography, graphic design, video editing and websites, based in Barcelona. Founder of Dsgn.pop.">
<link rel="canonical" href="@@CANON@@">
@@HREFLANG@@
<meta property="og:type" content="website">
<meta property="og:title" content="Lorenzo Devicienti">
<meta property="og:description" content="Photography, graphic design, video editing and websites, based in Barcelona.">
<meta property="og:image" content="{SITE}assets/img/og-image.jpg">
<meta property="og:url" content="@@CANON@@">
<meta property="og:locale" content="@@LOCALE@@">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0c0c0b">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
</head>
<body>
<header class="bar">
  <a class="bar__name" href="#top">Lorenzo Devicienti</a>
  <nav class="bar__nav mono" aria-label="Main">
    <a href="#index">Work</a><a href="#about">About</a><a href="#contact">Contact</a>
  </nav>
  <div class="bar__meta mono">
    <span>BCN <span data-clock>--:--</span></span>
    <span><span class="dot" aria-hidden="true"></span>Available</span>
    @@LANG@@
    <button class="bar__theme mono" type="button" data-theme-toggle aria-label="Switch to light theme"><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M7 1a6 6 0 0 1 0 12z" fill="currentColor"/></svg></button>
    <button class="bar__menu mono" type="button" aria-expanded="false" aria-controls="menu"><span class="bar__menu-open">Menu</span><span class="bar__menu-close">Close</span><svg class="bar__menu-icon" width="18" height="12" viewBox="0 0 18 12" aria-hidden="true"><path class="l1" d="M0 1h18" stroke="currentColor" stroke-width="1.5"/><path class="l2" d="M0 11h18" stroke="currentColor" stroke-width="1.5"/></svg></button>
  </div>
</header>
<nav class="menu" id="menu" aria-label="Menu">
  <ol class="menu__list">
    <li><a href="#photo"><span class="mono">01</span>Photography</a></li>
    <li><a href="#graphics"><span class="mono">02</span>Graphic design</a></li>
    <li><a href="#video"><span class="mono">03</span>Video editing</a></li>
    <li><a href="#web"><span class="mono">04</span>Websites</a></li>
    <li><a href="#about"><span class="mono">05</span>About</a></li>
    <li><a href="#services"><span class="mono">06</span>Services</a></li>
    <li><a href="#contact"><span class="mono">07</span>Contact</a></li>
  </ol>
  <div class="menu__foot mono">
    <a href="{IG}" target="_blank" rel="noopener">Dsgn.pop</a>
    <a href="{IG_ME}" target="_blank" rel="noopener">Instagram</a>
    <a href="{LI}" target="_blank" rel="noopener">LinkedIn</a>
    <button class="menu__theme" type="button" data-theme-toggle><svg width="16" height="16" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M7 1a6 6 0 0 1 0 12z" fill="currentColor"/></svg></button>
  </div>
</nav>

<main id="top">
  <section class="motto" aria-label="Motto">
@@MOTTO@@    <div class="motto__foot">
      <p class="motto__cite mono">A quote by <cite>Mirko Martorana</cite></p>
      <h1 class="motto__intro"><strong>I’m Lorenzo Devicienti.</strong> I work with photography, graphic design, video editing and websites. Based in Barcelona, founder of Dsgn.pop.</h1>
      <a class="mono motto__cta" href="#index">See the work <svg width="10" height="12" viewBox="0 0 10 12" aria-hidden="true"><path d="M5 0v11M1 7l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.4"/></svg></a>
    </div>
  </section>

  <section class="index" id="index" aria-labelledby="index-title">
    <h2 class="sr-only" id="index-title">Selected work</h2>
    <div class="index__head mono dim" aria-hidden="true"><span>No.</span><span>Discipline</span><span>Highlights</span><span>Volume</span></div>
    <a class="row" href="#photo" data-key="photo"><span class="row__n mono">01</span><span class="row__t">Photography</span><span class="row__d">AtleticProgettoMontagna · Felina F.C. · Portraits</span><span class="row__c mono">{total} photos</span></a>
    <a class="row" href="#graphics" data-key="graphics"><span class="row__n mono">02</span><span class="row__t">Graphic design</span><span class="row__d">APM match posters · Dsgn.pop</span><span class="row__c mono">{len(graphics)} posts</span></a>
    <a class="row" href="#video" data-key="video"><span class="row__n mono">03</span><span class="row__t">Video editing</span><span class="row__d">Marcus Thuram — short-form edit</span><span class="row__c mono">TikTok-first</span></a>
    <a class="row" href="#web" data-key="web"><span class="row__n mono">04</span><span class="row__t">Web design</span><span class="row__d">AtleticProgettoMontagna · AGLF · Castelnovo ne’ Monti · Casina · Villa Minozzo</span><span class="row__c mono">5 sites</span></a>
    <div class="preview" aria-hidden="true">{preview}</div>
  </section>

  <section class="chapter" id="photo" aria-labelledby="photo-title">
    <header class="chapter__head rv">
      <p class="chapter__n mono">01 — Photography</p>
      <h2 class="chapter__title" id="photo-title">Photo<span class="serif">graphy</span></h2>
      <p class="chapter__lede">Two seasons as <strong>Social Media Manager for AtleticProgettoMontagna</strong>, shooting their matches. A summer tournament with <strong>Felina F.C.</strong> And portraits of the people around me — something I really enjoy.</p>
    </header>
    <div class="filters mono" role="group" aria-label="Filter photos">
      <button class="chip" data-filter="all" aria-pressed="true">Selected<sup>12</sup></button>
      <button class="chip" data-filter="apm" aria-pressed="false">AtleticProgettoMontagna<sup>{len(apm)}</sup></button>
      <button class="chip" data-filter="felina" aria-pressed="false">Felina F.C.<sup>{len(felina)}</sup></button>
      <button class="chip" data-filter="portraits" aria-pressed="false">Portraits<sup>{len(portraits)}</sup></button>
    </div>
    <div class="gallery">
        {gallery}
    </div>
    <button class="chip mono gallery__more" type="button">Show all {total} photos</button>
  </section>

  <section class="chapter" id="graphics" aria-labelledby="graphics-title" style="padding-bottom:0">
    <header class="chapter__head rv">
      <p class="chapter__n mono">02 — Graphic design</p>
      <h2 class="chapter__title" id="graphics-title">Graphic <span class="serif">design</span></h2>
      <p class="chapter__lede">Graphics have always fascinated me. Match-day posters for the <strong>APM sports club</strong>, and editorial posts for <strong>Dsgn.pop</strong>, my design page on Instagram.</p>
    </header>
  </section>
  <section class="pin" aria-label="Graphic posts">
    <div class="pin__sticky">
      <div class="pin__track">
        <div class="poster poster--intro">
          <p class="mono dim">Scroll →</p>
          <p>Posters, carousels and editorial posts — <span class="serif">published every day</span> on Dsgn.pop.<br><br><a class="mono ulink" href="{IG}" target="_blank" rel="noopener">Follow @dsgn.pop {ARROW}</a></p>
        </div>
        {posters}
      </div>
      <div class="pin__progress" aria-hidden="true"><span></span></div>
    </div>
  </section>

  <section class="chapter" id="video" aria-labelledby="video-title">
    <header class="chapter__head rv">
      <p class="chapter__n mono">03 — Video editing</p>
      <h2 class="chapter__title" id="video-title">Built on <span class="serif">rhythm</span></h2>
      <p class="chapter__lede">Crafted for visual impact. Short-form edits where fast cuts, beat-driven transitions and pacing turn <strong>performance into emotion</strong>.</p>
    </header>
    <div class="phones rv">
        {phones}
    </div>
    <div class="video-notes rv">
      <p>A short-form edit dedicated to Marcus Thuram: athletic movement, presence and character, translated into a visually engaging story built for social platforms. <span class="dim">Where motion meets identity.</span></p>
      <div>
        <p class="mono">Toolkit</p>
        <ul class="tools mono"><li>Filmora</li><li>DaVinci Resolve</li><li>Premiere Pro</li><li>CapCut</li><li>Procreate</li></ul>
        <p style="margin-top:24px"><a class="mono ulink" href="{TIKTOK}" target="_blank" rel="noopener">Watch on TikTok {ARROW}</a></p>
      </div>
    </div>
  </section>

  <section class="chapter" id="web" aria-labelledby="web-title">
    <header class="chapter__head rv">
      <p class="chapter__n mono">04 — Web design</p>
      <h2 class="chapter__title" id="web-title">Web<span class="serif">sites</span></h2>
      <p class="chapter__lede">Two seasons managing the <strong>AtleticProgettoMontagna</strong> website. Before that, two internships at <a class="ulink" href="https://www.officina48.it" target="_blank" rel="noopener"><strong>Officina48</strong></a>: WordPress and Elementor for local brands, then a central role on <strong>municipal and institutional websites</strong> — clarity, usability and reliability for public communication.</p>
    </header>
    <div class="browsers">
        {browsers}
    </div>
  </section>

  <section class="chapter" id="about" aria-labelledby="about-title">
    <header class="chapter__head rv">
      <p class="chapter__n mono">05 — About</p>
      <h2 class="chapter__title" id="about-title">The <span class="serif">story</span></h2>
    </header>
    <div class="about">
      <figure class="about__photo rv">{img(about[0], "Lorenzo on graduation day, wearing a laurel wreath")}<figcaption class="mono dim">Graduation day — Reggio Emilia</figcaption></figure>
      <div class="about__body">
        <p class="about__big rv">At 18 I didn’t know what to do with my life. I only knew technology had always been part of it — <em>and probably always will be.</em></p>
        <ol class="timeline">
          <li class="rv"><span class="mono dim">University</span><div><h3>Unimore — Digital Marketing</h3><p>Department of Communication and Economics, Reggio Emilia. Three years of video editing, programmatic, graphic design, web development and ad strategy. I learned what I like — and, more importantly, what I don’t.</p></div></li>
          <li class="rv"><span class="mono dim">Internships</span><div><h3>Officina48 S.n.C.</h3><p>A real creative workflow: content, visual design and WordPress layouts for local businesses, then municipal websites across the territory.</p></div></li>
          <li class="rv"><span class="mono dim">Until Aug 2026</span><div><h3>Social Media Manager — APM</h3><p>Two seasons with AtleticProgettoMontagna: match photography, graphics and social content.</p></div></li>
          <li class="rv"><span class="mono dim">Now</span><div><h3>Barcelona</h3><p>Based in Barcelona and open to new projects, collaborations and roles.</p></div></li>
          <li class="rv"><span class="mono dim">Side project</span><div><h3>Dsgn.pop</h3><p>My Instagram page about design, where I keep practising in public.</p></div></li>
          <li class="rv"><span class="mono dim">Approach</span><div><h3>AI as a helper</h3><p>I use AI to simplify and speed up the work — never to replace the idea.</p></div></li>
        </ol>
      </div>
    </div>
  </section>

  <section class="chapter" id="services" aria-labelledby="services-title">
    <header class="chapter__head rv">
      <p class="chapter__n mono">06 — Services</p>
      <h2 class="chapter__title" id="services-title">How I can <span class="serif">help</span></h2>
    </header>
    <div class="services rv">
      <div class="service"><p class="mono dim">01</p><h3>Shooting</h3><ul><li>Photo shoots</li><li>Post-production</li><li>Publishing advice</li></ul></div>
      <div class="service"><p class="mono dim">02</p><h3>Design</h3><ul><li>Posters</li><li>Interfaces</li><li>Presentations</li><li>Carousels</li></ul></div>
      <div class="service"><p class="mono dim">03</p><h3>Video editing</h3><ul><li>Video production</li><li>Post-production</li><li>Publishing advice</li></ul></div>
      <div class="service"><p class="mono dim">04</p><h3>Websites</h3><ul><li>UX/UI design</li><li>Figma &amp; Framer</li><li>WordPress</li></ul></div>
    </div>
  </section>

  <section class="contact" id="contact" aria-labelledby="contact-title">
    <div class="contact__lead">
      <p class="mono dim" id="contact-title">07 — Contact</p>
      <p>Have an idea worth building? Let’s turn it into something people notice. Open to collaborations, freelance projects and bold concepts where design and strategy collide.</p>
    </div>
    <button class="mail" type="button" data-copy="lorenzodevicienti@gmail.com" aria-label="Copy email address lorenzodevicienti@gmail.com"><span>lorenzodevicienti@gmail.com</span></button>
    <p class="mail__hint">Click to copy · or <a class="ulink" href="mailto:lorenzodevicienti@gmail.com">open your mail app</a></p>
    <div class="contact__grid">
      <div><span class="mono">Phone</span><a class="ulink" href="tel:+393337111353">+39 333 711 1353</a></div>
      <div><span class="mono">Based in</span>Carrer de Londres, 23<br>Barcelona</div>
      <div><span class="mono">Elsewhere</span><a class="ulink" href="{IG}" target="_blank" rel="noopener">Dsgn.pop</a><br><a class="ulink" href="{IG_ME}" target="_blank" rel="noopener">Instagram</a><br><a class="ulink" href="{LI}" target="_blank" rel="noopener">LinkedIn</a></div>
      <div><span class="mono">© <span data-year>2026</span></span>Lorenzo Devicienti<br><a class="ulink" href="#top">Back to top ↑</a></div>
    </div>
  </section>
</main>

<dialog class="lb" aria-label="Photo viewer">
  <img alt="">
  <button class="lb__close mono" type="button">Close ✕</button>
  <div class="lb__ui mono">
    <button class="lb__prev" type="button" aria-label="Previous photo">← Prev</button>
    <span><span class="lb__cap"></span> · <span class="lb__count"></span></span>
    <button class="lb__next" type="button" aria-label="Next photo">Next →</button>
  </div>
</dialog>
<div class="toast mono" role="status" aria-live="polite"></div>
</body>
</html>
"""
from i18n import LANGS, MOTTO, JS, translate

LOCALES = {"en": "en_GB", "it": "it_IT", "es": "es_ES"}


def motto_html(lang):
    m = MOTTO[lang]
    # Il motto è una citazione (di Mirko Martorana), non il titolo della pagina: blockquote, non h1
    out = ['    <blockquote class="motto__text">', f'      <span class="sr-only">{m["label"].split(" — ")[0]}</span>']
    for kind in ("w", "n"):
        for text, tone in m[kind]:
            cls = f"motto__line motto__line--{kind}" + (f" motto__line--{tone}" if tone else "")
            out.append(f'      <span class="{cls}" aria-hidden="true">{text}</span>')
    out.append("    </blockquote>\n")
    return "\n".join(out)


for lang, info in LANGS.items():
    up = "../" if info["path"] else ""
    page = translate(html, lang)
    switch = '<nav class="lang" aria-label="Language">' + "".join(
        f'<a href="{up}{o["path"] or "./"}" hreflang="{code}" lang="{code}" title="{o["name"]}"'
        + (' aria-current="true"' if code == lang else "") + f'>{o["short"]}</a>'
        for code, o in LANGS.items()) + "</nav>"
    hreflang = "\n".join(f'<link rel="alternate" hreflang="{code}" href="{SITE}{o["path"]}">' for code, o in LANGS.items())
    hreflang += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}">'
    jsdata = " ".join(f'data-t-{k}="{v}"' for k, v in JS[lang].items())
    page = (page.replace("@@MOTTO@@", motto_html(lang)).replace("@@LANG@@", switch).replace("@@HREFLANG@@", hreflang)
                .replace("@@HTMLLANG@@", lang).replace("@@JSDATA@@", jsdata)
                .replace("@@CANON@@", SITE + info["path"]).replace("@@LOCALE@@", LOCALES[lang]))
    if up:
        page = page.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
    os.makedirs(os.path.join(REPO, info["path"]), exist_ok=True)
    open(os.path.join(REPO, info["path"], "index.html"), "w").write(page)

# --- Pagina 404 (indirizzi assoluti: viene servita su qualunque percorso)
BASE = "/LorenzoWebSite/"
not_found = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Page not found · Lorenzo Devicienti</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0c0c0b">
<link rel="icon" href="{BASE}assets/img/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{BASE}assets/css/style.css">
<script src="{BASE}assets/js/main.js" defer></script>
</head>
<body>
<header class="bar">
  <a class="bar__name" href="{BASE}">Lorenzo Devicienti</a>
</header>
<main>
  <section class="motto" aria-label="Page not found">
    <h1 class="motto__text" aria-label="Error 404: this page doesn’t exist, or has been moved.">
      <span class="motto__line" aria-hidden="true">Error 404:</span>
      <span class="motto__line motto__line--dim" aria-hidden="true">this page doesn’t</span>
      <span class="motto__line motto__line--accent" aria-hidden="true">exist (yet).</span>
    </h1>
    <div class="motto__foot">
      <p class="mono">Page not found</p>
      <p class="motto__intro">The page you’re looking for doesn’t exist or has been moved. Everything is on the home page now.</p>
      <a class="mono motto__cta ulink" href="{BASE}">Go to home {ARROW}</a>
    </div>
  </section>
</main>
</body>
</html>
"""
open(os.path.join(REPO, "404.html"), "w").write(not_found)

# --- Vecchi indirizzi del sito a più pagine: portano alla sezione giusta
for old, anchor in [("about", "about"), ("photo", "photo"), ("graphics", "graphics"), ("video", "video"),
                    ("web-site", "web"), ("contact", "contact")]:
    os.makedirs(os.path.join(REPO, old), exist_ok=True)
    open(os.path.join(REPO, old, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Lorenzo Devicienti</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}#{anchor}">
<meta http-equiv="refresh" content="0; url=../#{anchor}">
</head>
<body style="background:#0c0c0b;color:#edece7;font-family:system-ui,sans-serif">
<p><a href="../#{anchor}" style="color:inherit">This page has moved. Continue to Lorenzo Devicienti</a></p>
</body>
</html>
""")
print("ok", total)
