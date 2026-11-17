import json, os
from PIL import Image

REPO = "/home/user/lorenzowebsite"
IMG = REPO + "/assets/img"
M = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifest.json")))

SITE = "Lorenzo Devicienti"
DESC = ("If you are looking for a highly personalized project and need creative help to bring it to life, "
        "I would be thrilled to be part of it. Let’s create together!")
IG_PORTFOLIO = "https://www.instagram.com/dsgn.pop/"
IG_PERSONAL = "https://www.instagram.com/l0renx0/"
LINKEDIN = "https://www.linkedin.com/in/lorenzo-devicienti-5a5669278/"
TIKTOK = "https://vm.tiktok.com/ZNRYW8jPm/"
PAGES_URL = "https://l0renx0.github.io/LorenzoWebSite/"

ARROW = '<svg class="arrow" viewBox="0 0 14 14" aria-hidden="true"><path d="M3 11 11 3M4.5 3H11v6.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
CHEVRON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v15m-6-6 6 6 6-6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
LEFT = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'
RIGHT = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'

NAV = [("photo/", "Photo"), ("graphics/", "Graphics"), ("video/", "Video"), ("web-site/", "Web Site"), ("about/", "About")]


def size(f):
    w, h = Image.open(os.path.join(IMG, f)).size
    return w, h


def img(root, f, alt, cls="", lazy=True, extra=""):
    w, h = size(f)
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{root}assets/img/{f}" alt="{alt}" width="{w}" height="{h}"{c}{l}{extra}>'


def pill(href, text, ext=False, cls="pill"):
    t = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="{cls}" href="{href}"{t}>{text} {ARROW}</a>'


def head(root, title, desc, path):
    full = f"{title} · {SITE}" if title else f"{SITE} · Portfolio"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{PAGES_URL}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{PAGES_URL}assets/img/og-image.jpg">
<meta property="og:url" content="{PAGES_URL}{path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/img/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;800&family=Manrope:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
<script src="{root}assets/js/main.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(root, current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{root}{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if current == "contact/" else ""
    items.append(f'<li class="only-mobile"><a href="{root}contact/"{cur}>Contact</a></li>')
    return f"""<header class="site-header">
  <div class="site-header__inner">
    <a class="site-header__brand" href="{root}">Lorenzo Devicienti</a>
    <nav class="site-nav" aria-label="Main">
      <ul>
        {chr(10).join('        ' + i for i in items).strip()}
      </ul>
    </nav>
    <a class="site-header__cta" href="{root}contact/">Let’s talk</a>
  </div>
</header>
"""


def footer(root, plain=False):
    if plain:
        return f"""<footer class="site-footer site-footer--plain">
  <div class="wrap"><p class="site-footer__copy">© <span data-year>2026</span> · crafted by Lorenzo Devicienti</p></div>
</footer>
</body>
</html>
"""
    links = [("", "Home"), ("photo/", "Photo"), ("graphics/", "Graphics"), ("video/", "Video"),
             ("web-site/", "Website"), ("about/", "About"), ("contact/", "Contact")]
    nav = "\n".join(f'          <li><a href="{root}{h}">{t}</a></li>' for h, t in links)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <p class="label">Contact</p>
        <p class="site-footer__title">Let’s start creating together</p>
        {pill(root + "contact/", "Let’s talk", cls="pill pill--light")}
      </div>
      <nav aria-label="Footer">
        <ul class="site-footer__nav">
{nav}
        </ul>
      </nav>
      <ul class="site-footer__social">
        <li><a class="link-row" href="{IG_PORTFOLIO}" target="_blank" rel="noopener">Instagram Portfolio {ARROW}</a></li>
        <li><a class="link-row" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn {ARROW}</a></li>
        <li><a class="link-row" href="{IG_PERSONAL}" target="_blank" rel="noopener">Instagram {ARROW}</a></li>
      </ul>
    </div>
    <p class="site-footer__mega" aria-hidden="true">Lorenzo Devicienti</p>
    <div class="site-footer__bottom">
      <p class="site-footer__copy">© <span data-year>2026</span> · crafted by Lorenzo Devicienti</p>
      <a class="site-footer__top" href="#main">Back to top ↑</a>
    </div>
  </div>
</footer>
</body>
</html>
"""


def services():
    data = [("Shooting", ["Photo Shoots", "Post-Production", "Publishing Advice"]),
            ("Design", ["Posters", "Interfaces", "Presentations", "Carousels"]),
            ("Video Editing", ["Video Production", "Post-Production", "Publishing Advice"]),
            ("Web Site", ["UX/UI Design", "Figma and Framer", "WordPress"])]
    rows = []
    for n, (t, items) in enumerate(data, 1):
        lis = "".join(f"<li>{i}</li>" for i in items)
        rows.append(f'      <details class="service"><summary><span class="service__num">0{n}</span><span class="service__title">{t}</span>{CHEVRON}</summary><div class="service__body"><ul>{lis}</ul></div></details>')
    return f"""<section class="section services reveal" aria-labelledby="services-title">
  <div class="wrap">
    <h2 class="label" id="services-title">Services</h2>
    <div class="services__list">
{chr(10).join(rows)}
    </div>
  </div>
</section>
"""


def statement(label, html, button, narrow=False, wrap="wrap"):
    cls = "statement statement--narrow" if narrow else "statement"
    return f"""<section class="section reveal">
  <div class="{wrap}">
    <div class="{cls}">
      <p class="label">{label}</p>
      <p class="statement__text">{html}</p>
      {button}
    </div>
  </div>
</section>
"""


def ticker(root, files, alt, h, duration):
    imgs = "".join(img(root, f, alt) for f in files)
    dup = "".join(img(root, f, "", extra=' aria-hidden="true"') for f in files)
    return f"""<div class="ticker" style="--h:{h}px;--duration:{duration}s">
  <div class="ticker__track">{imgs}<span aria-hidden="true" style="display:contents">{dup}</span></div>
</div>"""


def photo_carousel(root, files, alt, label):
    imgs = "\n      ".join(img(root, f, alt) for f in files)
    return f"""<div class="carousel carousel--photos" role="region" aria-label="{label}">
    <button class="carousel__btn carousel__btn--prev" type="button" aria-label="Previous photos">{LEFT}</button>
    <div class="carousel__track" tabindex="0">
      {imgs}
    </div>
    <button class="carousel__btn carousel__btn--next" type="button" aria-label="Next photos">{RIGHT}</button>
    <p class="carousel__count" aria-hidden="true"><span data-current>01</span> / {len(files):02d}</p>
  </div>"""


def write(path, html):
    full = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(html)


# ---------------------------------------------------------------- HOME
r = ""
h = M["home_d"]
home = head(r, "", DESC, "") + header(r, "") + f"""<main id="main">
<section class="hero">
  <div class="wrap">
    <p class="label">Portfolio · Lorenzo Devicienti</p>
    <blockquote class="hero__quote" data-split>“To get something you don’t have,<br> <span class="muted">you have to do something you’ve never done before.”</span></blockquote>
    <p class="hero__author">— Mirko Martorana</p>
    <ul class="hero__meta">
      <li><span class="status-dot" aria-hidden="true"></span>Available for new projects</li>
      <li>Photo · Graphics · Video · Web</li>
      <li>Based in Barcelona</li>
    </ul>
  </div>
</section>

<section class="wrap projects" aria-label="Selected work">
  <a data-cursor="View" class="project project--wide project--hero reveal" href="graphics/">
    <div class="project__media">{img(r, h[0]['file'], 'Graphic posts “Jago’s David is a Woman” and “Echoverse” from the Dsgn.pop page', lazy=False)}<span class="project__badge">{ARROW}</span></div>
    <div class="project__meta"><div><p class="project__kicker">Design Pop</p><h2 class="project__title">Graphic Posts</h2></div><span class="project__num">01</span></div>
  </a>
  <a data-cursor="View" class="project reveal" href="photo/#felina">
    <div class="project__media">{img(r, h[1]['file'], 'Felina F.C. player running through coloured smoke')}<span class="project__badge">{ARROW}</span></div>
    <div class="project__meta"><div><p class="project__kicker">Felina F.C.</p><h2 class="project__title">Sport Photography</h2></div><span class="project__num">02</span></div>
  </a>
  <a data-cursor="View" class="project reveal" href="photo/#portraits">
    <div class="project__media">{img(r, h[2]['file'], 'Portrait of a young man in profile')}<span class="project__badge">{ARROW}</span></div>
    <div class="project__meta"><div><p class="project__kicker">Friends</p><h2 class="project__title">Portraits</h2></div><span class="project__num">03</span></div>
  </a>
  <a data-cursor="View" class="project project--wide reveal" href="web-site/">
    <div class="project__media">{img(r, h[3]['file'], 'Homepage of the Castelnovo ne’ Monti municipality website')}<span class="project__badge">{ARROW}</span></div>
    <div class="project__meta"><div><p class="project__kicker">Municipality of Castelnovo ne’ Monti</p><h2 class="project__title">Municipal Website</h2></div><span class="project__num">04</span></div>
  </a>
</section>

{statement("Designing Success", 'To improve and continue my passion for design, I created the Dsgn.pop page <span class="muted">where I publish posts about design.</span>', pill(IG_PORTFOLIO, "Profile", True))}
{services()}</main>
""" + footer(r)
write("index.html", home)

# ---------------------------------------------------------------- ABOUT
r = "../"
a = M["about_d"]
about = head(r, "About", "From uncertainty about the future to a degree in Digital Marketing: the story behind Lorenzo Devicienti’s work.", "about/") + header(r, "about/") + f"""<main id="main">
<section class="page-top">
  <div class="wrap wrap--1100">
    <p class="label">About Me</p>
    <h1 class="title-xl">It all started with uncertainty <span class="muted">about the future.</span></h1>
    <div class="stack" style="margin-top:40px">
      <p class="lead">When I was 18, I didn’t know what to do with my life.<br>I just knew that technology had always been a part of my life, <span class="muted">and probably always will be.</span></p>
      <p class="lead">So, after graduating from high school, I enrolled at university, in the <span class="muted">Digital Marketing</span> course at <span class="muted">Unimore, in the Department of Communication and Economics in Reggio Emilia.</span></p>
    </div>
  </div>
</section>

<section class="section reveal" aria-label="Graduation day">
  {ticker(r, [x['file'] for x in a[:4]], 'Graduation day in Reggio Emilia', 400, 35)}
</section>

<section class="reveal">
  <div class="wrap wrap--800">
    <p class="label">About Me</p>
    <h2 class="title-xl">My University <span class="muted">experience</span></h2>
    <div class="stack" style="margin-top:32px">
      <p class="lead">During my three years at university, I learned the trade of a digital marketer: video editing, programmatic advertising, graphic design, web development and ad strategy.</p>
      <p class="lead">I learned what I like, but more importantly, what I don’t. <span class="muted">I grew professionally and personally.</span></p>
      <p class="lead">I also broadened my horizons thanks to the <span class="muted">use of AI, which I learned to use as a helper to simplify my work and make everything more efficient</span>, rather than replacing me.</p>
    </div>
  </div>
</section>

<section class="section reveal">
  <div class="wrap wrap--940">
    <div class="figure">{img(r, a[4]['file'], 'Illustration of a person meditating in front of AI company logos')}</div>
  </div>
</section>

{services()}
{statement("Let’s Talk!", 'If you are looking for a highly personalized project and need creative help to bring it to life, I would be thrilled to be part of it. <span class="muted">Let’s create together!</span>', pill(r + "contact/", "Contact Me"), narrow=True)}</main>
""" + footer(r)
write("about/index.html", about)

# ---------------------------------------------------------------- PHOTO
p = M["photo_d"]
def group(y):
    g = sorted([x for x in p if x['y'] == y], key=lambda x: x['x'])
    i = next((k for k, x in enumerate(g) if x['x'] >= 200), 0)
    return [x['file'] for x in g[i:] + g[:i]]
photo = head(r, "Photo", "Sport photography for AtleticProgettoMontagna and Felina F.C., and portraits by Lorenzo Devicienti.", "photo/") + header(r, "photo/") + f"""<main id="main">
<section class="page-top">
  <div class="wrap wrap--1100">
    <h1 class="title-xl">Sport Photo Shooting</h1>
    <div class="stack" style="margin-top:24px">
      <p class="lead">This is my second year working with the AtleticProgettoMontagna sports club as Social Media Manager, <span class="muted">and I have done various photo shoots during matches</span>.</p>
      <p class="lead">Here are some of the shots…</p>
    </div>
  </div>
</section>

<section class="section reveal">
  <div class="wrap wrap--1100">
  {photo_carousel(r, group(860), 'AtleticProgettoMontagna match photo', 'AtleticProgettoMontagna photos')}
  </div>
</section>

<section id="felina" class="reveal">
  <div class="wrap wrap--940">
    <p class="lead">During the summer, I took several photos of the Felina F.C. sports club <span class="muted">as they competed in an important summer tournament</span>.</p>
    <p class="lead">Here are some of the shots…</p>
  </div>
</section>

<section class="section reveal">
  <div class="wrap wrap--1100">
  {photo_carousel(r, group(2065), 'Felina F.C. summer tournament photo', 'Felina F.C. photos')}
  </div>
</section>

<section id="portraits" class="reveal">
  <div class="wrap wrap--1100">
    <h2 class="title-xl">Portraits of people</h2>
    <div class="stack" style="margin-top:24px">
      <p class="lead">Over the past year, I’ve had the opportunity to photograph people, <span class="muted">which is something I really enjoy doing</span>.</p>
      <p class="lead">Here are some of the shots…</p>
    </div>
  </div>
</section>

<section class="section reveal">
  <div class="wrap wrap--1100">
  {photo_carousel(r, group(3365), 'Portrait photo', 'Portrait photos')}
  </div>
</section>

{statement("Let’s Talk!", 'If you are interested in my work and would like a personalized photo shoot, <span class="muted">let’s talk and create something together!</span>', pill(r + "contact/", "Contact Me"))}</main>
""" + footer(r)
write("photo/index.html", photo)

# ---------------------------------------------------------------- GRAPHICS
g = M["graphics_d"]
graphics = head(r, "Graphics", "Graphic design by Lorenzo Devicienti for the APM sports club and the Dsgn.pop Instagram page.", "graphics/") + header(r, "graphics/") + f"""<main id="main">
<section class="page-top">
  <div class="wrap wrap--940">
    <h1 class="title-xl">Designing Success</h1>
    <div class="stack" style="margin-top:24px">
      <p class="lead">Graphic design is one of those things that has always fascinated me, and something I often enjoy doing.</p>
      <p class="lead">I had the opportunity to create graphics for the APM sports club, and I also opened my own portfolio page on Instagram, called Dsgn.pop.</p>
    </div>
  </div>
</section>

<section class="section reveal" aria-label="Graphic posts">
  {ticker(r, [x['file'] for x in g], 'Graphic post by Lorenzo Devicienti', 370, 45)}
</section>

{statement("The Page", 'Besides working with the APM sports club, I share my graphic work on <span class="muted">my Instagram portfolio page, Dsgn.pop.</span>', pill(IG_PORTFOLIO, "Follow Me", True), narrow=True, wrap="wrap wrap--940")}
{statement("Let’s Talk", 'If you need graphics for your business or for an event, <span class="muted">let’s create them together!</span>', pill(r + "contact/", "Contact Me"), narrow=True, wrap="wrap wrap--940")}</main>
""" + footer(r)
write("graphics/index.html", graphics)

# ---------------------------------------------------------------- VIDEO
v = M["video_d"]
video = head(r, "Video", "Short-form video editing by Lorenzo Devicienti: rhythm, pacing and storytelling for social platforms.", "video/") + header(r, "video/") + f"""<main id="main">
<section class="page-top">
  <div class="wrap">
    <h1 class="title-xl">Video Editing</h1>
    <p class="lead" style="margin-top:24px">Built on Rhythm, <span class="muted">Crafted for Visual Impact</span>.</p>
  </div>
</section>

<section class="reveal" style="padding-top:64px">
  <div class="wrap">
    <div class="frame" style="max-width:810px;margin:0 auto">{img(r, v[0]['file'], 'Frames from the Marcus Thuram edit: “Goal” and “Tu-Tu”', lazy=False)}</div>
    <div class="text-cta" style="margin-top:48px">
      <p class="body-l">Short-form edit dedicated to Marcus Thuram, built to enhance rhythm, intensity and visual impact through fast cuts, beat-driven transitions and dynamic pacing. The video focuses on athletic movement, presence and character, translating football performance into a visually engaging narrative suited for social platforms.</p>
      {pill(TIKTOK, "Video", True)}
    </div>
  </div>
</section>

<section class="section reveal">
  <div class="wrap">
    <div class="projects" style="padding-top:0;gap:40px 120px;max-width:1150px;margin:0 auto">
      <div class="frame">{img(r, v[1]['file'], 'Frame from the edit: “Tu-Tu” celebration')}</div>
      <div class="frame">{img(r, v[2]['file'], 'Frame from the edit: “Thuram” title in the stadium')}</div>
    </div>
    <div class="text-cta" style="margin-top:56px">
      <p class="body-l">This edit was produced using Filmora, with full awareness of platform-specific formats and engagement logic (TikTok-first). Beyond this project, I am fully capable of working with DaVinci Resolve, Adobe Premiere Pro, CapCut and Procreate, adapting my workflow to advanced colour grading, professional timelines, and creative motion or graphic-driven edits, depending on the project’s needs.</p>
      {pill(TIKTOK, "Video", True)}
    </div>
    <p class="body-l" style="margin-top:72px;max-width:1100px">The goal was not only technical execution, but storytelling through motion, music and timing — turning performance into emotion.</p>
    <p class="lead" style="margin-top:40px">Where Motion <span class="muted">Meets Identity</span>.</p>
  </div>
</section>
</main>
""" + footer(r)
write("video/index.html", video)

# ---------------------------------------------------------------- WEB SITE
w = M["web_site_d"]
def shots(items):
    out = []
    for f, alt, href, label in items:
        btn = f'<div class="site-shot__links">{pill(href, label, True)}</div>' if href else ""
        out.append(f'<div><div class="site-shot">{img(r, f, alt)}</div>{btn}</div>')
    return "\n      ".join(out)
web = head(r, "Web Site", "Web development by Lorenzo Devicienti: WordPress and Elementor websites for local brands and municipalities.", "web-site/") + header(r, "web-site/") + f"""<main id="main">
<section class="page-top">
  <div class="wrap wrap--940">
    <h1 class="title-xl">Web Development</h1>
    <div class="stack" style="margin-top:24px">
      <p class="lead">During university, I was fortunate enough to do two <span class="muted">extracurricular internships</span>.</p>
      <p class="lead">I did them at Officina48 S.n.C., where I had the opportunity <span class="muted">to learn how to use WordPress and Elementor.</span></p>
    </div>
    <p style="margin-top:40px">{pill("https://www.officina48.it", "Officina48 S.n.C.", True)}</p>
  </div>
</section>

<section class="section reveal">
  <div class="wrap wrap--940">
    <div class="sites">
      {shots([(w[0]['file'], 'AGLF Education website, homepage', None, None), (w[1]['file'], 'AGLF Education website, study abroad page', None, None), (w[2]['file'], 'AGLF Education website, programme page', None, None)])}
    </div>
    <p style="margin-top:32px">{pill("https://www.aglf.academy", "AGLF", True)}</p>
    <div class="stack" style="margin-top:40px">
      <p class="lead">During my internship at Officina48, I worked inside a real creative workflow, collaborating <span class="muted">on digital projects for local brands and businesses</span>.</p>
      <p class="lead">I was involved in content creation, visual design and website development, contributing to social media materials, graphic assets and WordPress-based layouts.</p>
      <p class="body-l">This experience taught me how ideas move from concept to execution, how deadlines shape creativity, and how design must always serve a clear objective. It was a hands-on environment where <span class="muted">precision, adaptability and problem-solving</span> mattered as much as aesthetics.</p>
      <p>Screenshots above: <span class="muted">AGLF Education</span></p>
    </div>
  </div>
</section>

<section class="reveal">
  <div class="wrap wrap--940">
    <div class="sites">
      {shots([(w[3]['file'], 'Castelnovo ne’ Monti municipality website', 'https://www.comune.castelnovo-nemonti.re.it', 'Castelnovo ne’ Monti'), (w[4]['file'], 'Casina municipality website', 'https://www.comune.casina.re.it', 'Casina'), (w[5]['file'], 'Villa Minozzo municipality website', 'https://www.comune.villa-minozzo.re.it', 'Villa Minozzo')])}
    </div>
    <div class="stack" style="margin-top:56px">
      <p class="lead">During my second internship, <span class="muted">I took on a more central role in web projects</span>, working extensively on municipal and institutional websites across the local area.</p>
      <p class="lead">I was involved in structuring pages, managing content, and supporting the development of clear, accessible digital interfaces designed <span class="muted">for public communication.</span></p>
      <p class="lead">This phase strengthened my understanding of real-world workflows, responsibility, and the importance of clarity, usability and reliability in digital design.</p>
    </div>
  </div>
</section>

{statement("Let’s Talk", 'If you need a website for your business or for an event, <span class="muted">let’s create it together!</span>', pill(r + "contact/", "Contact Me"), narrow=True, wrap="wrap wrap--940")}</main>
""" + footer(r)
write("web-site/index.html", web)

# ---------------------------------------------------------------- CONTACT
contact = head(r, "Contact", "Get in touch with Lorenzo Devicienti for photography, graphic design, video editing and websites.", "contact/") + header(r, "contact/") + f"""<main id="main">
<section class="page-top">
  <div class="wrap">
    <div class="contact">
      <div>
        <p class="label label--grey" style="font-size:18px">Contact Me</p>
        <h1 class="title-xl" style="margin-top:24px">Get in touch</h1>
        <div class="contact__intro body-l" style="margin-top:32px;max-width:800px">
          <p>Have an idea worth building?</p>
          <p>Let’s turn it into something people notice.<br>Open to collaborations, freelance projects, and bold concepts where design and strategy collide.</p>
          <p>If you’re ready to do something different, you know where to find me.</p>
        </div>
        <dl class="contact__details">
          <div><dt>Email</dt><dd><a class="link-row" href="mailto:lorenzodevicienti@gmail.com">lorenzodevicienti@gmail.com {ARROW}</a></dd></div>
          <div><dt>Phone</dt><dd><a href="tel:+393337111353">+39 333 711 1353</a></dd></div>
          <div><dt>Address</dt><dd>Carrer de Londres, 23<br>Barcelona</dd></div>
        </dl>
      </div>
      <ul>
        <li><a class="link-row" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn {ARROW}</a></li>
        <li><a class="link-row" href="{IG_PERSONAL}" target="_blank" rel="noopener">Instagram Personal {ARROW}</a></li>
        <li><a class="link-row" href="{IG_PORTFOLIO}" target="_blank" rel="noopener">Instagram Portfolio {ARROW}</a></li>
      </ul>
    </div>
  </div>
</section>
</main>
""" + footer(r, plain=True)
write("contact/index.html", contact)

# ---------------------------------------------------------------- 404
r = "/LorenzoWebSite/"
nf = head(r, "Page not found", "This page doesn’t exist or has been moved.", "404.html").replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"') + header(r, "") + f"""<main id="main">
<section class="page-top">
  <div class="wrap">
    <h1 class="title-xl" style="max-width:800px">Oops. It looks like the page you’re trying to reach <span class="muted">doesn’t exist</span> or has been moved.</h1>
    <p style="margin-top:48px">{pill(r, "Go to home")}</p>
  </div>
</section>
</main>
""" + footer(r)
write("404.html", nf)

print("ok")
