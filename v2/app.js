// Concept v2 — interazioni. Nessuna libreria esterna.
document.documentElement.classList.add("js");
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

// Tema chiaro/scuro (ricordato in questo browser)
const root = document.documentElement;
try { const t = localStorage.getItem("ld-theme"); if (t) root.dataset.theme = t; } catch (e) {}
$("[data-theme-toggle]")?.addEventListener("click", () => {
  const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  try { localStorage.setItem("ld-theme", root.dataset.theme); } catch (e) {}
});

// Orologio di Barcellona
const clock = $("[data-clock]");
const tick = () => {
  if (!clock) return;
  clock.textContent = new Intl.DateTimeFormat("en-GB", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Madrid" }).format(new Date());
};
tick(); setInterval(tick, 15000);

// Barra: sfondo dopo lo scroll, si nasconde scendendo
const bar = $(".bar");
let lastY = scrollY;
addEventListener("scroll", () => {
  const y = scrollY;
  bar.classList.toggle("is-scrolled", y > 40);
  bar.classList.toggle("is-hidden", y > lastY && y > 400);
  lastY = y;
}, { passive: true });
bar.addEventListener("focusin", () => bar.classList.remove("is-hidden"));

// Anno
$$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

// Comparsa allo scroll
const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
$$(".rv").forEach((el) => io.observe(el));

// Citazione: parole separate per l'effetto "inchiostro"
$$("[data-words]").forEach((el) => {
  const walk = (node) => [...node.childNodes].forEach((c) => {
    if (c.nodeType === 3) {
      const f = document.createDocumentFragment();
      c.textContent.split(/(\s+)/).forEach((p) => {
        if (!p) return;
        if (/^\s+$/.test(p)) return f.append(p);
        const s = document.createElement("span"); s.className = "w"; s.textContent = p; f.append(s);
      });
      c.replaceWith(f);
    } else if (c.nodeType === 1) walk(c);
  });
  walk(el);
});

// Indice: anteprima che segue il mouse
const preview = $(".preview");
if (preview && matchMedia("(hover: hover) and (pointer: fine)").matches) {
  let x = 0, y = 0, px = 0, py = 0, raf;
  const loop = () => {
    px += (x - px) * 0.16; py += (y - py) * 0.16;
    preview.style.transform = `translate3d(${px + 24}px, ${py - 160}px, 0) rotate(${(x - px) * 0.04}deg)`;
    raf = requestAnimationFrame(loop);
  };
  $$(".row").forEach((row) => {
    row.addEventListener("pointerenter", () => {
      $$("img", preview).forEach((im) => im.classList.toggle("is-on", im.dataset.key === row.dataset.key));
      preview.classList.add("is-on");
      if (!raf && !reduce) loop();
    });
    row.addEventListener("pointerleave", () => preview.classList.remove("is-on"));
  });
  addEventListener("pointermove", (e) => { x = e.clientX; y = e.clientY; if (reduce) { px = x; py = y; preview.style.transform = `translate3d(${x + 24}px, ${y - 160}px, 0)`; } }, { passive: true });
}

// Foto: filtri per serie (con View Transitions dove supportate)
const gallery = $(".gallery");
const moreBtn = $(".gallery__more");
let showAll = false, current = "all";
const applyFilter = () => {
  const figs = $$("figure", gallery);
  let shown = 0;
  figs.forEach((f) => {
    const match = current === "all" || f.dataset.series === current;
    const pick = current !== "all" || showAll || f.dataset.pick === "1";
    f.hidden = !(match && pick);
    if (!f.hidden) shown++;
  });
  if (moreBtn) moreBtn.hidden = current !== "all" || showAll;
};
const withTransition = (fn) => (document.startViewTransition && !reduce ? document.startViewTransition(fn) : fn());
$$(".chip").forEach((chip) => chip.addEventListener("click", () => {
  $$(".chip").forEach((c) => c.setAttribute("aria-pressed", c === chip));
  current = chip.dataset.filter;
  withTransition(applyFilter);
}));
moreBtn?.addEventListener("click", () => { showAll = true; withTransition(applyFilter); });
if (gallery) {
  $$("figure", gallery).forEach((f, i) => (f.style.viewTransitionName = `ph-${i}`));
  applyFilter();
}

// Lightbox per le foto
const lb = $(".lb");
if (lb && gallery) {
  const img = $("img", lb), count = $(".lb__count", lb), cap = $(".lb__cap", lb);
  let list = [], pos = 0;
  const show = (n) => {
    pos = (n + list.length) % list.length;
    const f = list[pos], im = $("img", f);
    img.src = im.dataset.full || im.currentSrc || im.src; img.alt = im.alt;
    cap.textContent = $("figcaption", f)?.textContent || "";
    count.textContent = `${String(pos + 1).padStart(2, "0")} / ${String(list.length).padStart(2, "0")}`;
  };
  gallery.addEventListener("click", (e) => {
    const f = e.target.closest("figure"); if (!f) return;
    list = $$("figure", gallery).filter((x) => !x.hidden); show(list.indexOf(f)); lb.showModal();
  });
  gallery.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.target.matches("figure")) e.target.click(); });
  $(".lb__prev", lb).onclick = () => show(pos - 1);
  $(".lb__next", lb).onclick = () => show(pos + 1);
  $(".lb__close", lb).onclick = () => lb.close();
  lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
  lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(pos - 1); if (e.key === "ArrowRight") show(pos + 1); });
}

// Grafica: lo scroll verticale fa scorrere i poster in orizzontale
const pin = $(".pin");
if (pin) {
  const sticky = $(".pin__sticky", pin), track = $(".pin__track", pin), bar = $(".pin__progress", pin);
  const size = () => {
    if (reduce || innerWidth < 700) { pin.style.height = ""; sticky.style.position = "static"; sticky.style.height = "auto"; sticky.style.overflowX = "auto"; track.style.transform = ""; return false; }
    sticky.style.position = ""; sticky.style.height = ""; sticky.style.overflowX = "";
    const dist = track.scrollWidth - innerWidth;
    pin.style.height = `${innerHeight + dist}px`;
    return dist;
  };
  let dist = size();
  addEventListener("resize", () => (dist = size()));
  addEventListener("load", () => (dist = size()));
  const onScroll = () => {
    if (!dist) return;
    const top = pin.getBoundingClientRect().top;
    const p = Math.min(1, Math.max(0, -top / dist));
    track.style.transform = `translate3d(${-p * dist}px,0,0)`;
    bar.style.setProperty("--p", p);
  };
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
}

// Email: clic = copia negli appunti (con link mailto come alternativa)
const toast = $(".toast");
$("[data-copy]")?.addEventListener("click", async (e) => {
  const mail = e.currentTarget.dataset.copy;
  try {
    await navigator.clipboard.writeText(mail);
    toast.textContent = "Email copied — talk soon";
    toast.classList.add("is-on"); setTimeout(() => toast.classList.remove("is-on"), 2200);
  } catch (err) { location.href = `mailto:${mail}`; }
});
