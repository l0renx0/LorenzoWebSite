// Piccoli comportamenti del sito. Senza librerie esterne.
document.documentElement.classList.add("js");

// Anno corrente nel piè di pagina
document.querySelectorAll("[data-year]").forEach((el) => {
  el.textContent = new Date().getFullYear();
});

// Comparsa morbida degli elementi quando entrano nello schermo
const revealed = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -10% 0px" }
  );
  revealed.forEach((el) => io.observe(el));
} else {
  revealed.forEach((el) => el.classList.add("is-visible"));
}

// Caroselli con frecce
document.querySelectorAll(".carousel").forEach((carousel) => {
  const track = carousel.querySelector(".carousel__track");
  const step = () => {
    const item = track.firstElementChild;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    return item ? item.getBoundingClientRect().width + gap : track.clientWidth;
  };
  const go = (dir) => {
    const max = track.scrollWidth - track.clientWidth - 2;
    if (dir > 0 && track.scrollLeft >= max) return track.scrollTo({ left: 0, behavior: "smooth" });
    if (dir < 0 && track.scrollLeft <= 2) return track.scrollTo({ left: max, behavior: "smooth" });
    track.scrollBy({ left: dir * step(), behavior: "smooth" });
  };
  carousel.querySelector(".carousel__btn--prev")?.addEventListener("click", () => go(-1));
  carousel.querySelector(".carousel__btn--next")?.addEventListener("click", () => go(1));
});

// ---------------------------------------------------------------------------
// Strato "minimal raffinato"
// ---------------------------------------------------------------------------
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Citazione e titoli principali: parole che salgono una dopo l'altra
document.querySelectorAll("[data-split]").forEach((el) => {
  if (reduceMotion) return;
  let i = 0;
  const walk = (node) => {
    [...node.childNodes].forEach((child) => {
      if (child.nodeType === Node.TEXT_NODE) {
        const frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) return frag.append(part);
          const outer = document.createElement("span");
          outer.className = "split-word";
          const inner = document.createElement("span");
          inner.style.setProperty("--i", i++);
          inner.textContent = part;
          outer.append(inner);
          frag.append(outer);
        });
        child.replaceWith(frag);
      } else if (child.nodeType === Node.ELEMENT_NODE && child.tagName !== "BR") {
        walk(child);
      }
    });
  };
  el.setAttribute("aria-label", el.textContent.replace(/\s+/g, " ").trim());
  walk(el);
  el.querySelectorAll(".split-word").forEach((w) => w.setAttribute("aria-hidden", "true"));
});

// Testata che si nasconde scendendo e ricompare risalendo
const header = document.querySelector(".site-header");
if (header) {
  let lastY = window.scrollY;
  window.addEventListener(
    "scroll",
    () => {
      const y = window.scrollY;
      header.classList.toggle("is-hidden", y > lastY && y > 160);
      lastY = y;
    },
    { passive: true }
  );
  header.addEventListener("focusin", () => header.classList.remove("is-hidden"));
}

// Immagini che compaiono dolcemente quando sono pronte
document.querySelectorAll('img[loading="lazy"]').forEach((im) => {
  const done = () => im.classList.add("is-loaded");
  if (im.complete && im.naturalWidth) done();
  else {
    im.addEventListener("load", done, { once: true });
    im.addEventListener("error", done, { once: true });
  }
});

// Contatore dei caroselli (01 / 19)
document.querySelectorAll(".carousel").forEach((carousel) => {
  const track = carousel.querySelector(".carousel__track");
  const current = carousel.querySelector("[data-current]");
  if (!track || !current) return;
  const update = () => {
    const item = track.firstElementChild;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    const w = item ? item.getBoundingClientRect().width + gap : 1;
    const idx = Math.min(track.children.length, Math.round(track.scrollLeft / w) + 1);
    current.textContent = String(idx).padStart(2, "0");
  };
  track.addEventListener("scroll", update, { passive: true });
});

// Foto a schermo intero (clic su una foto dei caroselli)
const galleries = document.querySelectorAll(".carousel--photos .carousel__track");
if (galleries.length && "HTMLDialogElement" in window) {
  const dlg = document.createElement("dialog");
  dlg.className = "lightbox";
  dlg.setAttribute("aria-label", "Photo viewer");
  dlg.innerHTML =
    '<img alt=""><button class="lightbox__close" type="button" aria-label="Close">✕</button>' +
    '<button class="lightbox__prev" type="button" aria-label="Previous photo">←</button>' +
    '<button class="lightbox__next" type="button" aria-label="Next photo">→</button>' +
    '<p class="lightbox__count" aria-live="polite"></p>';
  document.body.append(dlg);
  const view = dlg.querySelector("img");
  const count = dlg.querySelector(".lightbox__count");
  let list = [];
  let pos = 0;
  const show = (n) => {
    pos = (n + list.length) % list.length;
    const src = list[pos];
    view.src = src.currentSrc || src.src;
    view.alt = src.alt;
    view.style.animation = "none";
    void view.offsetWidth;
    view.style.animation = "";
    count.textContent = `${String(pos + 1).padStart(2, "0")} / ${String(list.length).padStart(2, "0")}`;
  };
  galleries.forEach((track) => {
    const imgs = [...track.querySelectorAll("img")];
    imgs.forEach((im, n) => {
      im.tabIndex = 0;
      im.setAttribute("role", "button");
      const open = () => {
        list = imgs;
        show(n);
        dlg.showModal();
      };
      im.addEventListener("click", open);
      im.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          open();
        }
      });
    });
  });
  dlg.querySelector(".lightbox__close").addEventListener("click", () => dlg.close());
  dlg.querySelector(".lightbox__prev").addEventListener("click", () => show(pos - 1));
  dlg.querySelector(".lightbox__next").addEventListener("click", () => show(pos + 1));
  dlg.addEventListener("click", (e) => {
    if (e.target === dlg) dlg.close();
  });
  dlg.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") show(pos - 1);
    if (e.key === "ArrowRight") show(pos + 1);
  });
}

// Cursore personalizzato: un punto che diventa "View" sopra i progetti
if (!reduceMotion && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
  const cursor = document.createElement("div");
  cursor.className = "cursor";
  cursor.setAttribute("aria-hidden", "true");
  document.body.append(cursor);
  let x = -100, y = -100, cx = x, cy = y;
  window.addEventListener("pointermove", (e) => {
    x = e.clientX;
    y = e.clientY;
    cursor.classList.add("is-active");
  }, { passive: true });
  document.addEventListener("pointerleave", () => cursor.classList.remove("is-active"));
  const loop = () => {
    cx += (x - cx) * 0.22;
    cy += (y - cy) * 0.22;
    cursor.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
    requestAnimationFrame(loop);
  };
  loop();
  document.addEventListener("pointerover", (e) => {
    const labelled = e.target.closest("[data-cursor]");
    const link = e.target.closest("a, button, summary, [role=button]");
    cursor.classList.toggle("is-label", !!labelled);
    cursor.textContent = labelled ? labelled.dataset.cursor : "";
    cursor.classList.toggle("is-link", !labelled && !!link);
  });
}
