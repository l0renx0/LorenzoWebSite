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
