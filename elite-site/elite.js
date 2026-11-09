/* Nestlewood Realty: Elite */

/* ===== SETTINGS ===== */
// Drop a mountain/drone video in the images folder and put its name here,
// e.g. "images/blue-ridge.mp4". It plays over the animated mountains in the top section.
const HERO_VIDEO = "";
const LEAD_EMAIL = "nolan@nestlewoodrealty.com";
const FORM_ENDPOINT = ""; // optional: a formspree.io URL so leads go straight to your inbox

/* ===== Animated Blue Ridge mountain scenes (drawn in code) ===== */
const PALETTES = {
  sunset: { sky: ["#1e2140", "#4e4170", "#b8687b", "#f19a62", "#fcd49a"], sun: "#ffe0a8", sunY: 600, ridges: ["#c18ea0", "#946f94", "#694f7c", "#46385e", "#2a2341", "#141220"] },
  golden: { sky: ["#36597d", "#86a3be", "#e9c495", "#f6a65a"], sun: "#fff0c8", sunY: 560, ridges: ["#b3a9bd", "#8a83a1", "#64627f", "#43445e", "#282a3e", "#14151f"] },
  dusk:   { sky: ["#121833", "#36305e", "#85507d", "#e17a68"], sun: "#ffb58a", sunY: 640, ridges: ["#8a6589", "#634a77", "#45375e", "#2d2645", "#1c182d", "#0f0d18"] },
  mist:   { sky: ["#8ea6ba", "#c3d0da", "#ece5d8"], sun: "#ffffff", sunY: 520, ridges: ["#bcc7d0", "#98a8b7", "#76899d", "#566b82", "#3a4d64", "#223040"] },
  night:  { sky: ["#04060e", "#0b1230", "#1b2452"], sun: "#e9ecff", sunY: 300, moon: true, ridges: ["#2c3463", "#232a53", "#1b2043", "#141832", "#0d1023", "#07091a"] },
  dawn:   { sky: ["#2b3a5a", "#7a83a6", "#e6b0a0", "#f5d2a7"], sun: "#fff1d0", sunY: 600, ridges: ["#b5a8bb", "#8b80a0", "#655e80", "#45425f", "#2a2a40", "#161622"] },
};
function rng(seed) { return () => (seed = (seed * 16807) % 2147483647) / 2147483647; }
function mountainSVG(name, seed = 7) {
  const P = PALETTES[name] || PALETTES.sunset, r = rng(seed), W = 1600, n = P.ridges.length, id = name + seed;
  const stops = P.sky.map((c, i) => `<stop offset="${(i / (P.sky.length - 1)) * 100}%" stop-color="${c}"/>`).join("");
  let layers = "";
  P.ridges.forEach((color, i) => {
    const base = 470 + i * 78, amp = 60 + i * 12;
    const waves = [1, 2, 3, 5, 7, 11].map((k) => ({ k, a: (r() * amp) / (k * .55 + .6), p: r() * 6.28 }));
    const y = (x) => base - waves.reduce((s, w) => s + w.a * Math.sin((2 * Math.PI * w.k * x) / W + w.p), 0);
    let d = `M0 900 L0 ${y(0).toFixed(1)}`;
    for (let x = 12; x <= W * 2; x += 12) d += ` L${x} ${y(x).toFixed(1)}`;
    d += ` L${W * 2} 900 Z`;
    let trees = "";
    if (i >= n - 2) { // pine trees along the closest ridges
      for (let t = 0; t < 70; t++) {
        const x = r() * W, h = 14 + r() * (i === n - 1 ? 34 : 18), w = h * .38;
        [x, x + W].forEach((xx) => { const yy = y(xx) + 4; trees += `M${(xx - w).toFixed(1)} ${yy.toFixed(1)} L${xx.toFixed(1)} ${(yy - h).toFixed(1)} L${(xx + w).toFixed(1)} ${yy.toFixed(1)} Z `; });
      }
    }
    const dur = 260 - i * 38;
    layers += `<g class="layer" style="animation-duration:${dur}s"><path d="${d}" fill="${color}"/>${trees ? `<path d="${trees}" fill="${color}"/>` : ""}</g>`;
    if (i < n - 1) layers += `<rect x="0" y="${base - 40}" width="${W}" height="${900 - base + 40}" fill="url(#haze${id})" opacity=".35"/>`;
  });
  const birds = name === "night" ? "" : [0, 1, 2].map((b) => `<path class="bird" style="animation-delay:-${b * 6 + r() * 4}s" d="M${b * 26} ${210 + b * 18} q8 -8 16 0 q8 -8 16 0" fill="none" stroke="rgba(30,20,30,.55)" stroke-width="2"/>`).join("");
  return `<svg viewBox="0 0 ${W} 900" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
    <defs><linearGradient id="sky${id}" x1="0" y1="0" x2="0" y2="1">${stops}</linearGradient>
      <radialGradient id="sun${id}"><stop offset="0%" stop-color="${P.sun}" stop-opacity="1"/><stop offset="18%" stop-color="${P.sun}" stop-opacity=".9"/><stop offset="100%" stop-color="${P.sun}" stop-opacity="0"/></radialGradient>
      <linearGradient id="haze${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="${P.sky[P.sky.length - 1]}" stop-opacity="0"/><stop offset="100%" stop-color="${P.sky[P.sky.length - 1]}" stop-opacity=".9"/></linearGradient></defs>
    <rect width="${W}" height="900" fill="url(#sky${id})"/>
    <circle class="sun" cx="${P.moon ? 1180 : 1040}" cy="${P.sunY}" r="${P.moon ? 140 : 300}" fill="url(#sun${id})"/>
    ${P.moon ? `<circle cx="1180" cy="${P.sunY}" r="34" fill="#f4f1e8"/>` : ""}
    ${birds}${layers}</svg>`;
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".scene").forEach((el, i) => (el.innerHTML = mountainSVG(el.dataset.scene, 11 + i * 17)));

  // Optional hero video
  const v = document.querySelector(".hero-video");
  if (HERO_VIDEO && v) { v.src = HERO_VIDEO; v.hidden = false; v.play().catch(() => {}); }

  // Headline: words slide up one by one
  document.querySelectorAll(".split-words").forEach((h) => {
    const parts = h.innerHTML.split(/(<em>.*?<\/em>|\s+)/).filter((s) => s && s.trim());
    h.innerHTML = parts.map((p, i) => `<span class="w"><span style="animation-delay:${1.5 + i * .14}s">${p}</span></span>`).join(" ");
  });
  // Staggered fade-ins in the hero
  [".hero-copy .kicker", ".hero-sub", ".hero-btns", ".trace-line", ".hero-stats", ".glass-card"].forEach((s, i) => {
    const el = document.querySelector(s); if (el) el.style.animationDelay = `${1.4 + i * .18}s`;
  });

  // Statement: words light up as you scroll
  const words = document.querySelector(".words");
  if (words) {
    words.innerHTML = words.innerHTML.split(/(<em>.*?<\/em>|\s+)/).filter((s) => s && s.trim()).map((w) => `<span class="wd">${w}</span>`).join(" ");
    const spans = words.querySelectorAll(".wd");
    const lightUp = () => {
      const r = words.getBoundingClientRect(), vh = innerHeight;
      const prog = Math.min(1, Math.max(0, (vh * .85 - r.top) / (r.height + vh * .35)));
      spans.forEach((s, i) => s.classList.toggle("lit", i / spans.length < prog));
    };
    addEventListener("scroll", lightUp, { passive: true }); lightUp();
  }

  // Count-up numbers
  const countUp = (el) => {
    const end = +el.dataset.count, pre = el.dataset.prefix || "", suf = el.dataset.suffix || "", t0 = performance.now();
    const step = (t) => { const p = Math.min(1, (t - t0) / 1800), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + Math.round(end * e) + suf; if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };

  // Reveal on scroll (+ start counters)
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    e.target.classList.add("in");
    e.target.querySelectorAll("[data-count]").forEach(countUp);
    io.unobserve(e.target);
  }), { threshold: .2 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  setTimeout(() => document.querySelectorAll(".hero-stats [data-count]").forEach(countUp), 2200);

  // Listings rail: arrows + progress bar
  const rail = document.querySelector(".rail"), bar = document.querySelector(".progress span");
  if (rail) {
    const card = () => rail.querySelector(".home-card").offsetWidth + 24;
    document.querySelector(".arr.next").onclick = () => rail.scrollBy({ left: card() });
    document.querySelector(".arr.prev").onclick = () => rail.scrollBy({ left: -card() });
    const upd = () => { const max = rail.scrollWidth - rail.clientWidth; bar.style.width = `${25 + 75 * (max ? rail.scrollLeft / max : 0)}%`; };
    rail.addEventListener("scroll", upd, { passive: true }); upd();
    // gentle auto-glide so the rail feels alive
    let auto = setInterval(() => { if (rail.scrollLeft >= rail.scrollWidth - rail.clientWidth - 4) rail.scrollTo({ left: 0 }); else rail.scrollBy({ left: card() }); }, 4500);
    ["pointerdown", "wheel", "touchstart"].forEach((ev) => rail.addEventListener(ev, () => clearInterval(auto), { once: true, passive: true }));
  }

  // Area panels expand on hover / tap
  const panels = document.querySelectorAll(".panel");
  panels.forEach((p) => ["mouseenter", "click"].forEach((ev) => p.addEventListener(ev, () => panels.forEach((q) => q.classList.toggle("open", q === p)))));

  // Reviews rotate
  const qs = document.querySelectorAll(".q"), bars = document.querySelectorAll(".q-bars i");
  let qi = 0;
  setInterval(() => {
    qs[qi].classList.remove("on"); bars[qi].classList.remove("on");
    qi = (qi + 1) % qs.length;
    qs[qi].classList.add("on"); void bars[qi].offsetWidth; bars[qi].classList.add("on");
  }, 7000);

  // Nav darkens after scrolling; cursor glow follows the mouse
  const nav = document.querySelector(".nav-wrap"), glow = document.querySelector(".cursor-glow");
  addEventListener("scroll", () => nav.classList.toggle("scrolled", scrollY > 80), { passive: true });
  addEventListener("pointermove", (e) => { glow.style.left = e.clientX + "px"; glow.style.top = e.clientY + "px"; }, { passive: true });

  // Hero parallax: copy drifts as you scroll
  const copy = document.querySelector(".hero-copy");
  addEventListener("scroll", () => { if (scrollY < innerHeight) copy.style.transform = `translateY(${scrollY * .25}px)`; }, { passive: true });

  // Lead forms
  document.querySelectorAll(".lead-form").forEach((f) => f.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = new FormData(f), btn = f.querySelector("button");
    const showGuide = () => { if (f.dataset.guide && !f.parentElement.querySelector(".guide-dl"))
      f.insertAdjacentHTML("afterend", `<a class="pill light guide-dl" style="margin-top:1.2rem" href="${f.dataset.guide}" download>Download your guide</a>`); };
    if (FORM_ENDPOINT) {
      btn.textContent = "Sending...";
      try { data.append("_subject", f.dataset.subject); const r = await fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } });
        if (!r.ok) throw 0; f.reset(); btn.textContent = "Sent!"; showGuide(); } catch { btn.textContent = "Try again"; }
      return;
    }
    showGuide();
    location.href = `mailto:${LEAD_EMAIL}?subject=${encodeURIComponent(f.dataset.subject)}&body=${encodeURIComponent([...data].map(([k, v]) => `${k}: ${v}`).join("\n"))}`;
  }));
});
