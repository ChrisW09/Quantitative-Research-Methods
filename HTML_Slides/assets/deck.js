/* ==========================================================================
   Quantitative Research Methods -- HTML slide engine

   Authoring (see README.md in this folder):
     <body data-part="1" data-part-title="Descriptive Statistics"
           data-subtitle="Part 1: Descriptive Statistics -- Revision Material"
           data-revision data-notebook="Part_1_.../Part_1_....ipynb">
     <div id="stage"><main id="deck">
       <section class="slide" data-auto="title"></section>
       <section class="slide" data-section="Fundamentals" data-subsection="Basic Concepts">
         <h2>Basic Concepts</h2> ... </section>

   Keys: ->/space next, <- previous, Home/End, number + Enter = go to slide,
         m outline, d dark mode, f fullscreen, n speaker notes, b back, ? help.
   ========================================================================== */
(function () {
  "use strict";

  const COLAB = "https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/";
  const PYCOURSE = "https://github.com/ChrisW09/Quantitative-Research-Methods/tree/main/Python_Course";
  const REPO = "https://github.com/ChrisW09/Quantitative-Research-Methods";
  const PHOTO = "../Weisser_Feed_Portrait_4x5_HighRes.jpg";

  const PARTS = [
    { n: 1, name: "Descriptive Statistics", content: "<i>Revision:</i> basic concepts, levels of measurement, frequencies, measures of central tendency and dispersion", file: "Part_1_Descriptive_Statistics.html" },
    { n: 2, name: "Graphical Representations", content: "<i>Revision:</i> empirical CDF, histogram, boxplot", file: "Part_2_Graphical_Representations.html" },
    { n: 3, name: "Statistical Inference", content: "Normal distribution, CLT, confidence intervals, sample size, tests, $p$-values, types of error (appendix: one-sided, power)", file: "Part_3_Statistical_Inference.html" },
    { n: 4, name: "Regression", content: "Correlation, least squares, goodness of fit, inference for regression, multiple regression (appendix: residual analysis)", file: "Part_4_Regression.html" },
    { n: 5, name: "Classification", content: "Conditional probability, logistic regression, classification rules, confusion matrix, ROC/AUC, Bayes classifiers", file: "Part_5_Classification.html" },
  ];

  const KATEX_MACROS = {
    "\\blue": "\\htmlClass{m-blue}{#1}",
    "\\orange": "\\htmlClass{m-orange}{#1}",
    "\\green": "\\htmlClass{m-green}{#1}",
    "\\violet": "\\htmlClass{m-violet}{#1}",
    "\\red": "\\htmlClass{m-red}{#1}",
    "\\grey": "\\htmlClass{m-grey}{#1}",
    "\\ink": "\\htmlClass{m-ink}{#1}",
    "\\hl": "\\htmlClass{m-hl}{#1}",
    "\\tsum": "\\textstyle\\sum",
    "\\E": "\\operatorname{E}",
    "\\Var": "\\operatorname{Var}",
    "\\SE": "\\mathrm{SE}",
  };
  const KATEX_OPTS = {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "\\[", right: "\\]", display: true },
      { left: "\\begin{align*}", right: "\\end{align*}", display: true },
      { left: "\\begin{alignat*}", right: "\\end{alignat*}", display: true },
      { left: "\\begin{gather*}", right: "\\end{gather*}", display: true },
      { left: "\\(", right: "\\)", display: false },
      { left: "$", right: "$", display: false },
    ],
    macros: KATEX_MACROS,
    trust: (ctx) => ctx.command === "\\htmlClass" || ctx.command === "\\href",
    throwOnError: false,
    strict: "ignore",
    ignoredClasses: ["no-math"],
  };

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const el = (tag, attrs = {}, html) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v === null || v === undefined || v === false) continue;
      if (k === "class") e.className = v; else e.setAttribute(k, v === true ? "" : v);
    }
    if (html !== undefined) e.innerHTML = html;
    return e;
  };
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };

  // ---------------------------------------------------------------- state
  const D = {
    slides: [], sections: [], idx: 0, history: [],
    cfg: {}, typed: "",
  };
  window.Deck = D;

  // ---------------------------------------------------------------- math
  function renderMath(root) {
    if (!window.renderMathInElement) return;
    try { window.renderMathInElement(root, KATEX_OPTS); } catch (e) { console.error(e); }
    glueMath(root);
  }
  // Keep inline maths together with the characters that touch it ("$p$-value", "$250$&nbsp;g",
  // "level-$\alpha$", "$x_i$)."): browsers would otherwise break the line right next to the formula.
  function glueMath(root) {
    root.querySelectorAll(".katex").forEach((k) => {
      if (k.closest(".katex-display, .glue, svg, pre") || k.parentNode.closest(".katex")) return;
      // auto-render wraps each formula in an anonymous <span>: use that wrapper as the unit
      const w = k.parentNode;
      const unit = w.tagName === "SPAN" && !w.className && w.childNodes.length === 1 ? w : k;
      const prev = unit.previousSibling, next = unit.nextSibling;
      const pm = prev && prev.nodeType === 3 ? prev.nodeValue.match(/[^\s]+$/) : null;
      const nm = next && next.nodeType === 3 ? next.nodeValue.match(/^[^\s]+/) : null;
      if (!pm && !nm) return;
      const g = document.createElement("span");
      g.className = "glue";
      unit.parentNode.insertBefore(g, unit);
      if (pm) { const t = prev.splitText(prev.nodeValue.length - pm[0].length); g.appendChild(t); }
      g.appendChild(unit);
      if (nm) { const rest = next.splitText(nm[0].length); g.appendChild(next); void rest; }
    });
  }
  D.renderMath = renderMath;
  D.katexMacros = KATEX_MACROS;
  /** Render a TeX string to HTML (used by viz.js for labels). */
  D.tex = function (src, display = false) {
    if (!window.katex) return src;
    return window.katex.renderToString(src, { displayMode: display, macros: KATEX_MACROS, throwOnError: false, trust: KATEX_OPTS.trust, strict: "ignore" });
  };

  // ---------------------------------------------------------------- code highlighting
  const PY_KW = new Set("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield".split(" "));
  const PY_BI = new Set("print len range round sum min max sorted abs list dict set tuple int float str zip enumerate map filter type isinstance open any all".split(" "));
  function escapeHtml(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function dedent(text) {
    const lines = text.replace(/\t/g, "    ").split("\n");
    while (lines.length && !lines[0].trim()) lines.shift();
    while (lines.length && !lines[lines.length - 1].trim()) lines.pop();
    const ind = Math.min(...lines.filter((l) => l.trim()).map((l) => l.match(/^ */)[0].length));
    return lines.map((l) => l.slice(isFinite(ind) ? ind : 0)).join("\n");
  }
  function highlightPython(src) {
    const re = /(#[^\n]*)|([rRbBfF]{0,2}"""[\s\S]*?"""|[rRbBfF]{0,2}'''[\s\S]*?'''|[rRbBfF]{0,2}"(?:\\.|[^"\\\n])*"|[rRbBfF]{0,2}'(?:\\.|[^'\\\n])*')|(\b\d+\.?\d*(?:[eE][+-]?\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)/g;
    let out = "", last = 0, m;
    while ((m = re.exec(src))) {
      out += escapeHtml(src.slice(last, m.index));
      const t = escapeHtml(m[0]);
      if (m[1]) out += `<span class="com">${t}</span>`;
      else if (m[2]) out += `<span class="str">${t}</span>`;
      else if (m[3]) out += `<span class="num">${t}</span>`;
      else if (PY_KW.has(m[4])) out += `<span class="kw">${t}</span>`;
      else if (PY_BI.has(m[4])) out += `<span class="bi">${t}</span>`;
      else out += t;
      last = re.lastIndex;
    }
    return out + escapeHtml(src.slice(last));
  }
  function prepCode(root) {
    $$("pre.py", root).forEach((p) => { if (!p._hl) { p.innerHTML = highlightPython(dedent(p.textContent)); p._hl = true; } });
    $$("pre.out", root).forEach((p) => { if (!p._hl) { p.textContent = dedent(p.textContent); p._hl = true; } });
  }

  // ---------------------------------------------------------------- generated slides
  const ICON_IN = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#fff" d="M6.6 9.4h2.7V18H6.6zM8 5.2a1.55 1.55 0 1 1 0 3.1 1.55 1.55 0 0 1 0-3.1zM10.9 9.4h2.6v1.2h.04c.36-.68 1.24-1.4 2.56-1.4 2.74 0 3.24 1.8 3.24 4.14V18h-2.7v-4.1c0-.98-.02-2.24-1.36-2.24-1.37 0-1.58 1.07-1.58 2.17V18h-2.7z"/></svg>';
  const ICON_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="6" fill="none" stroke="#E4405F" stroke-width="2.2"/><circle cx="12" cy="12" r="4.4" fill="none" stroke="#E4405F" stroke-width="2.2"/><circle cx="17.4" cy="6.6" r="1.4" fill="#E4405F"/></svg>';

  function partMotif(n) {
    // faint decorative motif on the title slide, one per part
    const W = 1280, H = 720, g = [];
    const col = "#ffffff", col2 = "#f5b83d";
    if (n === 1) {
      const xs = [37, 38, 39, 39, 40, 40, 40, 41, 42, 43, 44];
      const cnt = {};
      xs.forEach((x) => { cnt[x] = (cnt[x] || 0) + 1; const cx = 120 + (x - 37) * 44, cy = 650 - cnt[x] * 36; g.push(`<circle cx="${cx}" cy="${cy}" r="14" fill="${col}" opacity=".18"/>`); });
      g.push(`<line x1="${120 + 3.73 * 44}" y1="420" x2="${120 + 3.73 * 44}" y2="670" stroke="${col2}" stroke-width="4" opacity=".35"/>`);
    } else if (n === 2) {
      const hs = [2, 5, 9, 14, 11, 7, 3, 1];
      hs.forEach((h, i) => g.push(`<rect x="${880 + i * 44}" y="${660 - h * 18}" width="40" height="${h * 18}" rx="4" fill="${col}" opacity=".16"/>`));
      g.push(`<path d="M80 660 C 200 655, 230 470, 300 470 S 400 640, 520 650" stroke="${col2}" stroke-width="4" fill="none" opacity=".3"/>`);
    } else if (n === 3) {
      let d = "M0 680";
      for (let x = 0; x <= W; x += 8) { const z = (x - 640) / 170; d += ` L${x} ${680 - 300 * Math.exp(-z * z / 2)}`; }
      g.push(`<path d="${d} L${W} 680 Z" fill="${col}" opacity=".07"/><path d="${d.replace("M0 680", "M0 680")}" stroke="${col}" stroke-width="3" fill="none" opacity=".22"/>`);
      let d2 = "M" + (640 + 1.96 * 170) + " 680";
      for (let x = 640 + 1.96 * 170; x <= W; x += 8) { const z = (x - 640) / 170; d2 += ` L${x} ${680 - 300 * Math.exp(-z * z / 2)}`; }
      g.push(`<path d="${d2} L${W} 680 Z" fill="${col2}" opacity=".25"/>`);
    } else if (n === 4) {
      const pts = [[1, 33], [3, 30], [4, 37], [5, 33], [6, 38], [8, 41], [8, 39], [9, 43], [10, 45], [11, 40], [12, 42], [13, 47]];
      const X = (x) => 860 + x * 28, Y = (y) => 700 - (y - 25) * 13;
      pts.forEach(([x, y]) => g.push(`<circle cx="${X(x)}" cy="${Y(y)}" r="9" fill="${col}" opacity=".2"/>`));
      g.push(`<line x1="${X(0)}" y1="${Y(30)}" x2="${X(14)}" y2="${Y(46.8)}" stroke="${col2}" stroke-width="4" opacity=".4"/>`);
    } else if (n === 5) {
      let d = "M80 660";
      for (let x = 80; x <= 560; x += 6) { const p = 1 / (1 + Math.exp(-(x - 320) / 40)); d += ` L${x} ${660 - 250 * p}`; }
      g.push(`<path d="${d}" stroke="${col}" stroke-width="4" fill="none" opacity=".25"/>`);
      for (let i = 0; i < 18; i++) { const x = 90 + i * 27; g.push(`<circle cx="${x}" cy="${x < 320 ? 668 : 402}" r="7" fill="${x < 320 ? col : col2}" opacity=".22"/>`); }
    }
    return `<svg class="t-art" viewBox="0 360 ${W} 340" preserveAspectRatio="xMidYMax slice" aria-hidden="true">${g.join("")}</svg>`;
  }

  function buildTitle(s) {
    const c = D.cfg;
    s.classList.add("title-slide");
    s.innerHTML = `
      <div class="t-kicker">Part ${c.part}${c.revision ? " &middot; revision material" : ""}</div>
      <div class="t-band">${partMotif(c.part)}
        <div class="t-title">Quantitative Research</div>
        <div class="t-sub">${c.subtitle}</div>
      </div>
      <div class="t-author">Prof. Dr. Christoph Weisser</div>
      <div class="t-hint">&rarr; / space: next &nbsp;&middot;&nbsp; m: outline &nbsp;&middot;&nbsp; d: dark mode &nbsp;&middot;&nbsp; ?: all keys</div>`;
    s.dataset.notitle = "1";
  }

  function buildLecturer(s) {
    s.innerHTML = `<h2>About the Lecturer</h2>
      <div class="cols lect mid" style="--cols: 38fr 58fr; --gap: 44px">
        <div style="align-items:center">
          <img class="photo" src="${PHOTO}" alt="Portrait of Christoph Weisser" onerror="this.style.visibility='hidden'">
          <div class="social stack" style="gap:6px; align-items:center">
            <a href="https://www.linkedin.com/in/christophweisser/" target="_blank" rel="noopener">${ICON_IN}christophweisser</a>
            <a href="https://www.instagram.com/christoph.j.weisser/" target="_blank" rel="noopener">${ICON_IG}christoph.j.weisser</a>
          </div>
        </div>
        <div>
          <p style="font-size:28px"><b>Prof. Dr. rer. pol. Christoph Weisser</b></p>
          <p>MLitt (St Andrews), MSc (Oxford)</p>
          <p>Professor of Mathematics, specialising in Business Data Science</p>
          <ul style="margin-top:8px">
            <li>Former Technical Lead for Artificial Intelligence and supervisor of industrial doctoral projects at BASF</li>
            <li>Research: Data Science, Machine Learning and Artificial Intelligence</li>
            <li>Focus: Application of AI in business and industry</li>
          </ul>
          <p class="fs-s"><b>Course materials:</b><br><a href="${REPO}" target="_blank" rel="noopener" style="white-space:nowrap">github.com/ChrisW09/Quantitative-Research-Methods</a></p>
        </div>
      </div>`;
  }

  function buildCourse(s) {
    const cur = D.cfg.part;
    const rows = PARTS.map((p) => {
      const on = p.n === cur;
      const name = `<a href="${p.file}" style="color:inherit;text-decoration:none">${p.n} &ndash; ${p.name}</a>`;
      return `<tr${on ? ' class="cur-part"' : ""}><td style="width:28px">${on ? "&#9654;" : ""}</td>
        <td class="l" style="white-space:nowrap">${on ? `<b class="c-blue">${name}</b>` : name}</td>
        <td class="l">${on ? `<span class="c-blue"><b>${p.content}</b></span>` : p.content}</td></tr>`;
    }).join("");
    s.innerHTML = `<h2>The lecture at a glance</h2>
      <table class="bt left fs-s" style="width:100%">
        <thead><tr><th></th><th>Part</th><th>Content</th></tr></thead>
        <tbody>${rows}
          <tr class="mid"><td></td><td><a class="c-green" href="${PYCOURSE}" target="_blank" rel="noopener">Python course</a></td>
          <td>Separate course: Python basics, pandas, plots, machine learning (Colab notebooks)</td></tr>
        </tbody></table>
      <p class="center fs-s" style="margin-top:6px">All analyses in <b>Python</b> (NumPy, pandas, SciPy, statsmodels, matplotlib); every deck comes with a Python script and a Jupyter notebook &ndash; also in Google Colab.
      These HTML slides add <b>interactive figures</b>: drag, slide and hover to explore.</p>`;
  }

  // ---------------------------------------------------------------- sections and TOC
  function scanSections() {
    let sec = null, sub = null, nMain = 0, nApx = 0;
    D.sections = [];
    for (const s of D.slides) {
      if (s.dataset.section) {
        const apx = s.hasAttribute("data-appendix");
        sec = {
          title: s.dataset.section, short: s.dataset.short || s.dataset.section,
          appendix: apx, no: apx ? String.fromCharCode(65 + nApx++) : String(++nMain),
          subs: [], first: s, slides: [],
        };
        D.sections.push(sec);
        sub = null;
      }
      if (s.dataset.subsection && sec) {
        const m = sec.subs.length + 1;
        // appendix subsections carry their own number in the title ("A.1 Properties of estimators")
        const am = sec.appendix ? s.dataset.subsection.match(/^([A-Z]\.\d+)\s+(.*)$/) : null;
        sub = am ? { title: am[2], no: am[1], first: s }
                 : { title: s.dataset.subsection, no: sec.appendix ? "" : `${sec.no}.${m}`, first: s };
        sec.subs.push(sub);
      }
      s._sec = sec; s._sub = sub;
      if (sec) sec.slides.push(s);
    }
  }

  function tocHTML(opts) {
    // opts: { current: sec|null, subs: "none"|"current"|"all", shade: bool, split: n|null, compact: bool }
    const secHTML = (sec) => {
      const isCur = opts.current === sec;
      const dim = opts.shade && opts.current && !isCur;
      const showSubs = opts.subs === "all" || (opts.subs === "current" && isCur);
      const subs = showSubs && sec.subs.length
        ? `<div class="subs">${sec.subs.map((u) => `<a href="#" data-go-slide="${u.first._n}"><span class="no">${u.no}</span>${u.title}</a>`).join("")}</div>` : "";
      return `<div class="sec${isCur ? " cur" : ""}${dim ? " dim" : ""}"><a href="#" data-go-slide="${sec.first._n}"><span class="no">${sec.no}</span><span>${sec.title}</span></a>${subs}</div>`;
    };
    // Beamer treats the appendix as its own part: the main part lists the main sections only,
    // the appendix lists the appendix sections only (scope "all" lists both)
    const scope = opts.scope || "main";
    const secs = D.sections.filter((x) => scope === "all" || (scope === "appendix" ? x.appendix : !x.appendix));
    const split = opts.split;
    if (split && secs.length > split) {
      return `<div class="toc${opts.compact ? " compact" : ""}" style="--toc-cols: 1fr 1fr"><div>${secs.slice(0, split).map(secHTML).join("")}</div><div>${secs.slice(split).map(secHTML).join("")}</div></div>`;
    }
    return `<div class="toc${opts.compact ? " compact" : ""}">${secs.map(secHTML).join("")}</div>`;
  }

  function insertSectionOverviews() {
    for (const sec of D.sections) {
      if (sec.first.hasAttribute("data-no-overview")) continue;
      const ov = el("section", { class: "slide section-slide generated" });
      ov.innerHTML = `<h2>Overview</h2>`;
      ov._overviewOf = sec;
      sec.first.parentNode.insertBefore(ov, sec.first);
      // the overview belongs to the new section: move the markers onto it
      ov.dataset.section = sec.first.dataset.section;
      if (sec.first.dataset.short) ov.dataset.short = sec.first.dataset.short;
      if (sec.first.hasAttribute("data-appendix")) ov.setAttribute("data-appendix", "");
      ov.id = "sec-" + sec.no;
      // ... and off the content slide (it keeps its subsection marker)
      delete sec.first.dataset.section;
      delete sec.first.dataset.short;
      sec.first.removeAttribute("data-appendix");
    }
  }

  // ---------------------------------------------------------------- chrome
  function buildChrome() {
    const c = D.cfg;
    const N = D.slides.length;
    const split = c.tocSplit;
    D.slides.forEach((s, i) => {
      s._n = i + 1;
    });
    D.slides.forEach((s, i) => {
      if (s._built) return;
      s._built = true;
      const auto = s.dataset.auto;
      if (auto === "title") buildTitle(s);
      else if (auto === "lecturer") buildLecturer(s);
      else if (auto === "course") buildCourse(s);

      // title and body
      const h2 = $(":scope > h2", s);
      const ttl = el("div", { class: "ttl" });
      const bd = el("div", { class: "bd" });
      if (h2) ttl.appendChild(h2);
      while (s.firstChild) bd.appendChild(s.firstChild);
      if (s._overviewOf) {
        const sec = s._sec;
        bd.innerHTML = tocHTML({ current: sec, subs: "current", shade: true, split: sec.appendix ? null : split,
          compact: D.sections.length > 5, scope: sec.appendix ? "appendix" : "main" });
      }
      // badges
      const t = h2 ? h2.textContent.trim() : "";
      if (!s.classList.contains("no-badge")) {
        if (/^Exercise\b/i.test(t) && !s.classList.contains("solution")) s.classList.add("exercise");
        if (/^Solution\b/i.test(t)) s.classList.add("solution");
      }
      let badge = s.dataset.badge;
      if (!badge && s.classList.contains("exercise")) badge = "Exercise";
      if (!badge && s.classList.contains("solution")) badge = "Solution";
      if (badge && h2) ttl.insertBefore(el("span", { class: "badge" }, badge), h2);

      // headline with section navigation
      const hdr = el("nav", { class: "hdr" });
      const inApx = !!(s._sec && s._sec.appendix);
      hdr.innerHTML = D.sections.filter((x) => x.appendix === inApx).map((x) =>
        `<a href="#" data-go-slide="${x.first._n}" class="${s._sec === x ? "on" : ""}">${x.short}</a>`).join("") +
        `<span class="sp"></span><span>Quantitative Research</span>`;
      // footline
      const ftr = el("footer", { class: "ftr" });
      const secTitle = s._sec ? ` &nbsp;|&nbsp; ${s._sec.short}` : "";
      ftr.innerHTML = `<div class="prog" style="width:${(100 * (i + 1) / N).toFixed(2)}%"></div>
        <span>Part ${c.part}${c.revision ? " (revision)" : ""}${secTitle}</span><span class="sp"></span>
        <a class="back" href="#" title="Back to where you came from (b)">&#8617; back</a>
        <span>${i + 1} / ${N}</span>`;

      if (auto !== "title") s.appendChild(hdr);
      if (h2) s.appendChild(ttl);
      s.appendChild(bd);
      if (auto !== "title") s.appendChild(ftr);
      if (s.closest("[data-appendix]") || (s._sec && s._sec.appendix)) s.classList.add("appendix-slide");

      // contents placeholders
      $$(".toc[data-mode]", bd).forEach((ph) => {
        const mode = ph.dataset.mode;
        const html = tocHTML({ current: null, subs: mode === "full" ? "all" : "none", shade: false, split: ph.dataset.split ? +ph.dataset.split : null, compact: ph.classList.contains("compact"), scope: ph.dataset.scope || "main" });
        ph.outerHTML = html;
      });
      // pointers
      $$("a.trynb", bd).forEach((a) => {
        a.href = COLAB + (c.notebook || "");
        a.target = "_blank"; a.rel = "noopener";
        if (!a.innerHTML.trim()) a.innerHTML = `&#9654;&thinsp;<b>Try it:</b> notebook, ${a.dataset.sec || "all examples"} (Colab)`;
      });
      $$("a.pycourse", bd).forEach((a) => {
        a.href = PYCOURSE; a.target = "_blank"; a.rel = "noopener";
        if (!a.innerHTML.trim()) a.innerHTML = `&#9654;&thinsp;<b>New to Python?</b> Python course: ${a.dataset.what || ""}`;
      });
      $$(".apxnote", bd).forEach((a) => { if (!a._p) { a.innerHTML = "&rarr; Appendix: " + a.innerHTML; a._p = 1; } });
      $$(".srcnote", bd).forEach((a) => { if (!a._p) { a.innerHTML = "Source: " + a.innerHTML; a._p = 1; } });
      $$('a[href^="http"]', s).forEach((a) => { if (!a.target) { a.target = "_blank"; a.rel = "noopener"; } });
      // images that may be missing
      $$("img", bd).forEach((im) => { if (!im.getAttribute("onerror")) im.addEventListener("error", () => { im.style.visibility = "hidden"; }); });
    });
  }

  // ---------------------------------------------------------------- navigation
  function fit() {
    const st = $("#stage");
    let W = window.innerWidth, H = window.innerHeight, x0 = 0, y0 = 0;
    if (D.speaker) { W = Math.round(window.innerWidth * 0.62) - 24; H = window.innerHeight - 64; x0 = 16; y0 = 48; }
    const sc = Math.min(W / 1280, H / 720);
    st.style.transform = `scale(${sc})`;
    st.style.left = (x0 + (D.speaker ? 0 : (W - 1280 * sc) / 2)) + "px";
    st.style.top = (y0 + (D.speaker ? 0 : (H - 720 * sc) / 2)) + "px";
    if (D.speaker) layoutSpeaker(sc);
  }

  // ---------------------------------------------------------------- speaker view
  // "s" opens a second window for the laptop screen: current slide, next slide, notes, timer.
  // Both windows stay in sync (postMessage between the deck window and its speaker window).
  let spkWin = null, spk = null, spkT0 = Date.now(), spkPaused = 0, spkPauseAt = 0;
  const MSG = "qrm-deck";
  function send(win, data) { try { if (win && !win.closed) win.postMessage(Object.assign({ [MSG]: true }, data), "*"); } catch (e) { /* closed */ } }
  function openSpeaker() {
    if (D.speaker) return;
    const url = location.href.split("#")[0].split("?")[0] + "?speaker#" + (D.idx + 1);
    spkWin = window.open(url, "qrm-speaker-" + D.cfg.part, "popup,width=1280,height=760");
    if (!spkWin) alert("The browser blocked the speaker window. Allow pop-ups for this page and press s again.");
  }
  function buildSpeaker() {
    document.body.classList.add("speaker");
    spk = el("div", { class: "spk" });
    spk.innerHTML = `<div class="spk-bar"><b>Speaker view</b> <span class="spk-pos"></span>
        <span class="sp"></span><span class="spk-clock"></span>
        <span class="spk-timer" title="Elapsed time">00:00</span>
        <button data-a="pause" title="Pause / resume the timer">&#10074;&#10074;</button><button data-a="reset" title="Reset the timer">&#8635;</button></div>
      <div class="spk-next"><div class="spk-lbl">Next</div><div class="spk-thumb"></div><div class="spk-ntitle"></div></div>
      <div class="spk-notes"><div class="spk-lbl">Notes</div><div class="spk-ntext"></div></div>
      <div class="spk-help">&larr; &rarr; navigate both windows &middot; the deck window shows what the audience sees</div>`;
    document.body.appendChild(spk);
    spk.addEventListener("click", (e) => {
      const a = e.target.closest("button"); if (!a) return;
      if (a.dataset.a === "reset") { spkT0 = Date.now(); spkPaused = 0; spkPauseAt = 0; }
      if (a.dataset.a === "pause") { if (spkPauseAt) { spkPaused += Date.now() - spkPauseAt; spkPauseAt = 0; } else spkPauseAt = Date.now(); }
      a.blur(); tick();
    });
    setInterval(tick, 1000);
    tick();
  }
  function tick() {
    if (!spk) return;
    const ms = (spkPauseAt || Date.now()) - spkT0 - spkPaused;
    const m = Math.floor(ms / 60000), s2 = Math.floor(ms / 1000) % 60;
    $(".spk-timer", spk).textContent = `${String(m).padStart(2, "0")}:${String(s2).padStart(2, "0")}`;
    $(".spk-timer", spk).classList.toggle("paused", !!spkPauseAt);
    const d = new Date();
    $(".spk-clock", spk).textContent = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }
  function layoutSpeaker(sc) {
    if (!spk) return;
    const left = Math.round(window.innerWidth * 0.62);
    spk.style.left = left + "px";
    const th = $(".spk-thumb", spk);
    const w = window.innerWidth - left - 32;
    th.style.width = w + "px"; th.style.height = Math.round(w * 720 / 1280) + "px";
    const inner = th.firstElementChild;
    if (inner) inner.style.transform = `scale(${w / 1280})`;
  }
  function updateSpeaker() {
    if (!spk) return;
    $(".spk-pos", spk).textContent = `slide ${D.idx + 1} / ${D.slides.length}`;
    const n = $("aside.notes", D.slides[D.idx]);
    const nt = $(".spk-ntext", spk);
    nt.innerHTML = n ? n.innerHTML : "<i>No notes for this slide.</i>";
    renderMath(nt);
    const th = $(".spk-thumb", spk);
    th.innerHTML = "";
    const nx = D.slides[D.idx + 1];
    $(".spk-ntitle", spk).innerHTML = nx ? (nx.querySelector(".ttl h2") || {}).innerHTML || (nx.classList.contains("title-slide") ? "Title" : "") : "<i>End of the deck</i>";
    if (nx) {
      // a static copy of the next slide (charts drawn, no interaction)
      prepare(nx);
      const shown = nx.classList.contains("active");
      if (!shown) nx.classList.add("active");
      if (window.QV) QV._mountAll(nx);
      fitSlide(nx);
      const c = nx.cloneNode(true);
      if (!shown) nx.classList.remove("active");
      c.querySelectorAll("[id]").forEach((e) => e.removeAttribute("id"));
      c.removeAttribute("id");
      c.querySelectorAll("script, .qv-tip").forEach((e) => e.remove());
      c.classList.add("active", "spk-clone");
      c.style.position = "absolute"; c.style.left = "0"; c.style.top = "0"; c.style.transformOrigin = "0 0"; c.style.pointerEvents = "none";
      th.appendChild(c);
    }
    layoutSpeaker();
  }
  function onMessage(e) {
    const d = e.data;
    if (!d || !d[MSG]) return;
    if (d.type === "go" && typeof d.n === "number" && d.n - 1 !== D.idx) go(d.n - 1, { fromPeer: true });
    if (d.type === "hello" && !D.speaker) { spkWin = e.source; send(spkWin, { type: "go", n: D.idx + 1 }); }
  }

  function prepare(s) {
    if (!s || s._prepared) return;
    s._prepared = true;
    renderMath(s);
  }

  // ---------------------------------------------------------------- fit: size and vertical balance
  // Text-only slides are enlarged (CSS zoom on the body's children, up to MAXZOOM) as long as
  // everything still fits; then the content is placed optically centred (a third of the free
  // space above it), as Beamer centres frames vertically. Pointers stay at the bottom.
  const MAXZOOM = 1.35, ZSTEP = 0.05;
  const isPointer = (e) => e.matches("a.trynb, a.pycourse, .apxnote, .srcnote, .pointers");
  const isInvisible = (e) => e.matches("script, style, aside.notes, template, .fit-mark") || getComputedStyle(e).display === "none";
  function fitSlide(s) {
    if (!s || !s.classList.contains("active") || s.classList.contains("title-slide") || s.classList.contains("no-fit")) return;
    const bd = $(":scope > .bd", s);
    if (!bd) return;
    bd.querySelectorAll(":scope > .fit-mark").forEach((e) => e.remove());
    const kids = Array.from(bd.children).filter((e) => !isInvisible(e));
    const content = kids.filter((e) => !isPointer(e));
    const ptrs = kids.filter(isPointer);
    if (!content.length) return;
    bd.querySelectorAll(":scope > .fit-mark").forEach((e) => e.remove());
    content.forEach((e) => { e.style.zoom = ""; });
    bd.style.paddingTop = "";
    const cs = getComputedStyle(bd);
    const gap = parseFloat(cs.rowGap) || 0;
    const sc = bd.getBoundingClientRect().height / bd.offsetHeight || 1;      // stage scale
    // The end of the content is read from an unzoomed marker placed right after it: browsers differ in how they
    // report the size of a zoomed element (WebKit/Safari gives its unzoomed size), but they all lay out the
    // element after it correctly. Horizontal overflow is read from scroll widths, which do not depend on zoom.
    const mark = document.createElement("div");
    mark.className = "fit-mark";
    mark.style.cssText = "height:0;margin:0;padding:0;border:0;flex:none;align-self:stretch";
    const lastContent = content[content.length - 1];
    lastContent.after(mark);
    const measure = () => {
      const r = bd.getBoundingClientRect();
      const innerTop = r.top + parseFloat(cs.paddingTop) * sc;
      const innerBottom = r.bottom - parseFloat(cs.paddingBottom) * sc;
      const innerRight = r.right - parseFloat(cs.paddingRight) * sc;
      const zoomed = content.some((e) => e.style.zoom && e.style.zoom !== "1");
      let bottom = mark.getBoundingClientRect().top - gap * sc, wide = bd.scrollWidth > bd.clientWidth + 2;
      // horizontal overflow from layout sizes (offset/client/scroll widths are in each element's own units,
      // consistent inside a zoomed subtree in every browser). A block's title bar deliberately bleeds into its
      // padding (negative margins), so blocks are judged by their content, not by their own scroll width.
      const tooWide = (d) => {
        if (d.matches(".block > h4")) return false;
        // (a block's own scroll width includes its bleeding title bar in WebKit: skip that test for blocks)
        if (!d.matches(".block") && d.clientWidth > 0 && d.scrollWidth > d.clientWidth + 2) return true;
        const par = d.parentElement;
        if (!par || d.offsetWidth === undefined) return false;
        const st = getComputedStyle(d);
        if (st.position === "absolute" || st.position === "fixed" || st.display.startsWith("inline")) return false;
        const ps = getComputedStyle(par);
        const inner = par.clientWidth - parseFloat(ps.paddingLeft) - parseFloat(ps.paddingRight);
        // a zoomed child reports its width in its own (unzoomed) units: convert to the parent's units
        const z = par === bd ? parseFloat(d.style.zoom) || 1 : 1;
        return par.clientWidth > 0 && d.offsetWidth * z > inner + 2 && parseFloat(st.marginLeft) >= 0 && parseFloat(st.marginRight) >= 0;
      };
      content.forEach((e) => {
        const q = e.getBoundingClientRect();
        if (!zoomed && q.right > innerRight + 1) wide = true;
        if (tooWide(e)) wide = true;
        // descendants that stick out of their parents (nowrap rows, wide formulas, tables, diagrams)
        e.querySelectorAll("*").forEach((d) => {
          // skip tooltips, notes, SVG internals and KaTeX's invisible MathML copy (laid out wider than the visible maths)
          if (d.closest(".qv-tip, aside.notes, .katex-mathml, .katex") || (d.ownerSVGElement && d.tagName !== "svg")) return;
          if (d.tagName !== "svg" && tooWide(d)) wide = true;
          if (zoomed) return;
          const r2 = d.getBoundingClientRect();
          if (!r2.width && !r2.height) return;
          if (r2.right > innerRight + 1) wide = true;
          if (r2.bottom > bottom) bottom = r2.bottom;
        });
      });
      bd.querySelectorAll("pre").forEach((e) => { if (e.scrollWidth > e.clientWidth + 1) wide = true; });
      // a clipped block (overflow hidden) counts as not fitting
      bd.querySelectorAll(".block, pre").forEach((e) => { if (e.scrollHeight > e.clientHeight + 1) bottom = Infinity; });
      const ptrH = ptrs.reduce((h, e) => h + e.getBoundingClientRect().height, 0) + ptrs.length * gap * sc;   // one gap before each pointer
      return { free: innerBottom - ptrH - bottom, bottom, innerTop, wide };
    };
    let m = measure();
    const textOnly = !bd.querySelector(".viz, .no-zoom, iframe, video, canvas");
    if (textOnly && m.free > 8 && !m.wide) {
      let best = 1;
      for (let z = MAXZOOM; z > 1.001; z -= ZSTEP) {
        content.forEach((e) => { e.style.zoom = z.toFixed(2); });
        const t = measure();
        if (t.free >= 0 && !t.wide) { best = z; break; }
      }
      content.forEach((e) => { e.style.zoom = best > 1 ? best.toFixed(2) : ""; });
      m = measure();
    }
    mark.remove();
    // optical centring: a third of the free space goes above the content
    if (m.free > 2 && !s.classList.contains("top")) {
      bd.style.paddingTop = (parseFloat(cs.paddingTop) + (m.free / sc) / 3).toFixed(1) + "px";
    }
    s._fitted = true;
  }
  D.fit = fitSlide;
  function scheduleFit(s) {
    void s.offsetHeight;                       // trigger layout so pending web fonts start loading
    fitSlide(s);
    // refit once late content has settled (web fonts, charts that finish drawing asynchronously)
    const again = () => { if (s.classList.contains("active")) fitSlide(s); };
    requestAnimationFrame(again);
    setTimeout(again, 150);
    if (document.fonts && document.fonts.status !== "loaded") document.fonts.ready.then(again);
  }

  function go(i, opts = {}) {
    i = Math.max(0, Math.min(D.slides.length - 1, i));
    const prev = D.slides[D.idx];
    const next = D.slides[i];
    if (opts.remember && i !== D.idx) D.history.push(D.idx);
    if (prev && prev !== next) { prev.classList.remove("active"); if (window.QV) QV._hide(prev); }
    D.idx = i;
    prepare(next);
    next.classList.add("active");
    if (window.QV) QV._show(next);
    scheduleFit(next);
    // prefetch neighbours (math only)
    setTimeout(() => { prepare(D.slides[i + 1]); prepare(D.slides[i - 1]); }, 60);
    const back = $(".ftr .back", next);
    if (back) back.classList.toggle("show", D.history.length > 0);
    // keep the address in sync, but only once navigation pauses: Safari allows at most
    // 100 replaceState calls per 10 seconds (holding an arrow key would exceed that)
    clearTimeout(D._hashTimer);
    D._hashTimer = setTimeout(() => {
      const h = "#" + (D.idx + 1);
      try { if (location.hash !== h) history.replaceState(null, "", h); } catch (e) { /* throttled */ }
    }, 120);
    updateNotes();
    updateOutlineCurrent();
    if (!opts.fromPeer) send(D.speaker ? window.opener : spkWin, { type: "go", n: i + 1 });
    if (D.speaker) updateSpeaker();
  }
  D.go = (n) => go(n - 1);
  D.next = () => go(D.idx + 1);
  D.prev = () => go(D.idx - 1);
  D.back = () => { if (D.history.length) go(D.history.pop()); };
  D.current = () => D.idx + 1;

  function slideIndexForHash(h) {
    h = decodeURIComponent((h || "").replace(/^#\/?/, ""));
    if (!h) return 0;
    if (/^\d+$/.test(h)) return Math.max(0, Math.min(D.slides.length - 1, +h - 1));
    const t = document.getElementById(h);
    if (t) { const s = t.closest(".slide"); if (s) return D.slides.indexOf(s); }
    return null;
  }

  /** Render math and mount every chart (print, checks). */
  D.renderAll = function () {
    D.slides.forEach((s) => {
      prepare(s);
      if (!window.QV) return;
      // charts need a laid-out slide to size themselves: show it while mounting
      const shown = s.classList.contains("active");
      if (!shown) s.classList.add("active");
      QV._mountAll(s);
      fitSlide(s);
      if (!shown) s.classList.remove("active");
    });
  };

  // ---------------------------------------------------------------- outline, help, notes
  let outline, help, notes;
  function buildPanels() {
    outline = el("aside", { class: "panel", id: "outline" });
    const items = [];
    let lastSec = null, lastSub = null;
    D.slides.forEach((s, i) => {
      if (s._sec !== lastSec && s._sec) { items.push(`<div class="s">${s._sec.no} &nbsp;${s._sec.title}</div>`); lastSec = s._sec; lastSub = null; }
      if (s._sub !== lastSub && s._sub) { items.push(`<div class="ss">${s._sub.no ? s._sub.no + " " : ""}${s._sub.title}</div>`); lastSub = s._sub; }
      const h2 = $(".ttl h2", s);
      const title = s.classList.contains("title-slide") ? "Title" : (h2 ? h2.innerHTML : "(untitled)");
      items.push(`<a href="#" data-go-slide="${i + 1}" data-text="${(h2 ? h2.textContent : "").toLowerCase().replace(/"/g, "")}"><span class="n">${i + 1}</span><span>${title}</span></a>`);
    });
    outline.innerHTML = `<header><div class="ph"><span>Part ${D.cfg.part} &ndash; ${D.cfg.partTitle}</span><button class="x" aria-label="Close">&times;</button></div>
      <input type="search" placeholder="Filter slides&hellip;" aria-label="Filter slides"></header><div class="list">${items.join("")}</div>`;
    document.body.appendChild(outline);
    renderMath(outline);
    $(".x", outline).onclick = () => toggleOutline(false);
    const inp = $("input", outline);
    inp.addEventListener("input", () => {
      const q = inp.value.trim().toLowerCase();
      $$(".list a", outline).forEach((a) => { a.style.display = !q || a.dataset.text.includes(q) || a.textContent.toLowerCase().includes(q) ? "" : "none"; });
      $$(".list .s, .list .ss", outline).forEach((h) => { h.style.display = q ? "none" : ""; });
    });

    help = el("div", { class: "help" });
    help.innerHTML = `<div class="card"><h3>Keyboard shortcuts</h3><table>
      <tr><td><kbd>&rarr;</kbd> <kbd>space</kbd> <kbd>PgDn</kbd></td><td>next slide</td></tr>
      <tr><td><kbd>&larr;</kbd> <kbd>PgUp</kbd></td><td>previous slide</td></tr>
      <tr><td><kbd>Home</kbd> / <kbd>End</kbd></td><td>first / last slide</td></tr>
      <tr><td><kbd>12</kbd> <kbd>Enter</kbd></td><td>go to slide 12</td></tr>
      <tr><td><kbd>m</kbd></td><td>outline with search</td></tr>
      <tr><td><kbd>b</kbd></td><td>back (after following a link)</td></tr>
      <tr><td><kbd>d</kbd></td><td>dark / light mode</td></tr>
      <tr><td><kbd>f</kbd></td><td>fullscreen</td></tr>
      <tr><td><kbd>n</kbd></td><td>speaker notes (on this screen)</td></tr>
      <tr><td><kbd>s</kbd></td><td>speaker view in a second window: next slide, notes, timer</td></tr>
      <tr><td><kbd>p</kbd></td><td>print / save as PDF (one slide per page)</td></tr>
      <tr><td><kbd>?</kbd> <kbd>Esc</kbd></td><td>this help / close</td></tr></table>
      <p style="margin:12px 0 0;color:var(--ink-muted)">Interactive figures: drag points and lines, move sliders, hover for values.</p></div>`;
    help.onclick = () => help.classList.remove("open");
    document.body.appendChild(help);

    notes = el("div", { class: "notes-pane" });
    document.body.appendChild(notes);

    const tb = el("div", { class: "toolbar" });
    tb.innerHTML = `<button data-act="outline" title="Outline (m)">&#9776; Outline</button><button data-act="theme" title="Dark mode (d)">&#9681; Theme</button><button data-act="fs" title="Fullscreen (f)">&#9974; Fullscreen</button><button data-act="speaker" title="Speaker view in a second window (s)">&#128483; Speaker</button><button data-act="help" title="Keys (?)">?</button>`;
    tb.addEventListener("click", (e) => {
      const a = e.target.closest("button"); if (!a) return;
      ({ outline: () => toggleOutline(), theme: toggleTheme, fs: toggleFS, speaker: openSpeaker, help: () => help.classList.toggle("open") })[a.dataset.act]();
      a.blur();
    });
    document.body.appendChild(tb);
  }
  function toggleOutline(force) {
    const open = force === undefined ? !outline.classList.contains("open") : force;
    outline.classList.toggle("open", open);
    if (open) { updateOutlineCurrent(true); $("input", outline).focus({ preventScroll: true }); }
    else $("input", outline).blur();
  }
  function updateOutlineCurrent(scroll) {
    if (!outline) return;
    $$(".list a.cur", outline).forEach((a) => a.classList.remove("cur"));
    const a = $(`.list a[data-go-slide="${D.idx + 1}"]`, outline);
    if (a) { a.classList.add("cur"); if (scroll) a.scrollIntoView({ block: "center" }); }
  }
  function updateNotes() {
    if (!notes) return;
    const n = $("aside.notes", D.slides[D.idx]);
    notes.innerHTML = `<h5>Speaker notes &middot; slide ${D.idx + 1}</h5>` + (n ? n.innerHTML : "<i>No notes for this slide.</i>");
    if (n && notes.classList.contains("open")) renderMath(notes);
  }
  function toggleTheme() {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    store.set("qrm-theme", root.dataset.theme);
    if (window.QV) QV._themeChanged();
  }
  function toggleFS() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
    else document.exitFullscreen && document.exitFullscreen();
  }

  // ---------------------------------------------------------------- events
  function onKey(e) {
    const t = e.target;
    if (t && (t.tagName === "INPUT" && t.type !== "range" || t.tagName === "TEXTAREA" || t.tagName === "SELECT" || t.isContentEditable)) {
      if (e.key === "Escape") { toggleOutline(false); t.blur(); }
      return;
    }
    if (t && t.tagName === "INPUT" && t.type === "range" && ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(e.key)) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (/^\d$/.test(k)) { D.typed += k; return; }
    if (k === "Enter" && D.typed) { go(+D.typed - 1, { remember: true }); D.typed = ""; e.preventDefault(); return; }
    D.typed = "";
    switch (k) {
      case "ArrowRight": case "ArrowDown": case "PageDown": case " ": case "Enter": D.next(); break;
      case "ArrowLeft": case "ArrowUp": case "PageUp": case "Backspace": D.prev(); break;
      case "Home": go(0); break;
      case "End": go(D.slides.length - 1); break;
      case "m": case "o": toggleOutline(); break;
      case "b": D.back(); break;
      case "d": toggleTheme(); break;
      case "f": toggleFS(); break;
      case "n": notes.classList.toggle("open"); updateNotes(); renderMath(notes); break;
      case "s": openSpeaker(); break;
      case "p": window.print(); break;
      case "?": help.classList.toggle("open"); break;
      case "Escape": help.classList.remove("open"); toggleOutline(false); notes.classList.remove("open"); break;
      default: return;
    }
    e.preventDefault();
  }

  function onClick(e) {
    const g = e.target.closest("[data-go-slide]");
    if (g) { e.preventDefault(); go(+g.dataset.goSlide - 1, { remember: !g.closest(".panel") && !g.closest(".hdr") }); if (g.closest(".panel")) toggleOutline(false); return; }
    const b = e.target.closest(".ftr .back");
    if (b) { e.preventDefault(); D.back(); return; }
    const a = e.target.closest('a[href^="#"]');
    if (a && a.getAttribute("href").length > 1) {
      const i = slideIndexForHash(a.getAttribute("href"));
      if (i !== null) { e.preventDefault(); go(i, { remember: true }); }
    }
    // release focus from buttons / sliders inside slides so the keys keep navigating
    const f = e.target.closest(".slide button, .slide input[type=range], .slide select");
    if (f && f.tagName !== "SELECT") setTimeout(() => f.blur(), 0);
  }

  let touch = null;
  function onTouchStart(e) { if (e.target.closest(".viz, .viz-ctrl, a, button, input")) { touch = null; return; } touch = [e.touches[0].clientX, e.touches[0].clientY]; }
  function onTouchEnd(e) {
    if (!touch) return;
    const dx = e.changedTouches[0].clientX - touch[0], dy = e.changedTouches[0].clientY - touch[1];
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) (dx < 0 ? D.next : D.prev)();
    touch = null;
  }

  // ---------------------------------------------------------------- init
  function init() {
    const b = document.body;
    D.cfg = {
      part: +b.dataset.part || 0,
      partTitle: b.dataset.partTitle || "",
      subtitle: b.dataset.subtitle || "",
      revision: b.hasAttribute("data-revision"),
      notebook: b.dataset.notebook || "",
      tocSplit: b.dataset.tocSplit ? +b.dataset.tocSplit : null,
    };
    D.speaker = /(^|[?&])speaker\b/.test(location.search);
    const saved = store.get("qrm-theme");
    if (saved) document.documentElement.dataset.theme = saved;

    const deck = $("#deck");
    D.slides = $$(":scope > section.slide", deck);
    scanSections();
    insertSectionOverviews();
    D.slides = $$(":scope > section.slide", deck);
    scanSections();
    buildChrome();
    prepCode(deck);
    // titles contain math: render them now (outline needs them)
    $$(".ttl h2", deck).forEach(renderMath);
    buildPanels();
    if (D.speaker) buildSpeaker();
    window.addEventListener("message", onMessage);

    fit();
    window.addEventListener("resize", fit);
    document.addEventListener("keydown", onKey);
    document.addEventListener("click", onClick);
    document.addEventListener("touchstart", onTouchStart, { passive: true });
    document.addEventListener("touchend", onTouchEnd, { passive: true });
    window.addEventListener("hashchange", () => { const i = slideIndexForHash(location.hash); if (i !== null && i !== D.idx) go(i); });
    window.addEventListener("beforeprint", () => D.renderAll());
    if (document.fonts) document.fonts.addEventListener("loadingdone", () => fitSlide(D.slides[D.idx]));

    const start = slideIndexForHash(location.hash);
    D.idx = 0;
    go(start === null ? 0 : start);
    document.body.classList.add("ready");
    D.ready = true;
    if (D.speaker && window.opener) send(window.opener, { type: "hello" });
    document.dispatchEvent(new CustomEvent("deck:ready"));
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
