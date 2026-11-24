/* ==========================================================================
   QV -- interactive figures for the QRM HTML slides (built on D3 v7)

   Charts are drawn lazily: QV.mount() only registers a function, the engine
   calls it the first time the slide is shown (so sizes are known), and again
   calls show()/hide() on the returned object when the slide is entered/left.

     <div class="viz" id="p1-mean" style="height:330px"></div>
     <script>
     QV.mount("#p1-mean", (el) => {
       const ch = QV.chart(el, { x: { domain: [36, 46], label: "Shoe size" },
                                 y: { domain: [0, 4], label: "Players", ticks: 4 } });
       QV.bars(ch, [{ x: 40, y: 3 }], { width: 0.7 });
       const s = QV.slider(QV.controls(el), { label: "n", min: 5, max: 50, value: 10, onInput: v => {...} });
       return { show() {...}, hide() {...} };      // optional (animations)
     });
     </script>

   Everything is in "slide pixels" (the slide is 1280 x 720). Colours are
   CSS tokens (QV.C.blue = "var(--c-blue)"), so dark mode works for free --
   always set colours with .style("fill", ...) / .style("stroke", ...),
   never with .attr("fill", ...), because attributes do not resolve var().

   Contents: mount | C, series | chart + marks | labels (text, tex) |
   controls (slider, select, segmented, button, readout, tiles, legend) |
   tooltip, drag, animation | stats (course rules) | distributions | rng |
   components: histogram, boxplot, ecdf, density, scatter, freqBars
   ========================================================================== */
(function () {
  "use strict";
  const d3 = window.d3;

  // ---------------------------------------------------------------- registry
  const REG = [];
  function mount(target, fn) {
    const sel = typeof target === "string" ? target : null;
    const find = () => (sel ? Array.from(document.querySelectorAll(sel)) : [target]);
    const add = (els) => els.forEach((el) => {
      if (REG.some((x) => x.el === el && x.fn === fn)) return;
      const r = { el, fn, sel, inst: null, done: false };
      REG.push(r);
      // the slide may already be on screen (engine initialised before this script ran)
      const s = el.closest && el.closest(".slide.active");
      if (s && window.Deck && Deck.ready) _show(s);
    });
    const els = find();
    if (els.length || document.readyState !== "loading") add(els);
    else document.addEventListener("DOMContentLoaded", () => { add(find()); const s = document.querySelector(".slide.active"); if (s && window.Deck && Deck.ready) _show(s); }, { once: true });
  }
  function _mountAll(slide) {
    REG.forEach((r) => {
      if (!r.done && slide.contains(r.el)) {
        r.done = true;
        if (!r.el.hasAttribute("role")) {            // screen readers: name the figure after its slide
          const name = (slide.getAttribute("aria-label") || "").replace(/^Slide \d+ of \d+:?\s*/, "");
          r.el.setAttribute("role", "figure");
          r.el.setAttribute("aria-label", "Interactive figure" + (name ? ": " + name : ""));
        }
        try { r.inst = r.fn(r.el) || null; } catch (e) { console.error("QV chart failed:", r.el.id || r.el, e); r.el.dataset.vizError = String(e); }
      }
    });
  }
  function _show(slide) {
    _mountAll(slide);
    REG.forEach((r) => { if (r.inst && r.inst.show && slide.contains(r.el)) try { r.inst.show(); } catch (e) { console.error(e); } });
  }
  function _hide(slide) {
    REG.forEach((r) => { if (r.inst && r.inst.hide && slide.contains(r.el)) try { r.inst.hide(); } catch (e) { console.error(e); } });
  }
  /** Remove the figures of a slide from the registry (the engine then restores the slide's original HTML). */
  function _detach(slide) {
    const out = [];
    for (let i = REG.length - 1; i >= 0; i--) {
      const r = REG[i];
      if (!slide.contains(r.el)) continue;
      try { if (r.inst && r.inst.hide) r.inst.hide(); if (r.inst && r.inst.destroy) r.inst.destroy(); } catch (e) { console.error(e); }
      out.unshift(r);
      REG.splice(i, 1);
    }
    return out;
  }
  /** Register detached figures again on the restored elements (unless the slide's own script has just done so). */
  function _reattach(slide, stale) {
    stale.forEach((r) => {
      let els = [];
      try {
        if (r.sel) els = Array.from(slide.querySelectorAll(r.sel));
        else if (r.el.id) { const e = slide.querySelector("#" + CSS.escape(r.el.id)); if (e) els = [e]; }
      } catch (e) { els = []; }
      els.forEach((el) => { if (!REG.some((x) => x.el === el)) REG.push({ el, fn: r.fn, sel: r.sel, inst: null, done: false }); });
    });
  }
  function _themeChanged() {
    REG.forEach((r) => { if (r.inst && r.inst.theme) try { r.inst.theme(); } catch (e) { console.error(e); } });
  }

  // ---------------------------------------------------------------- colours
  const C = {
    blue: "var(--c-blue)", orange: "var(--c-orange)", green: "var(--c-green)",
    violet: "var(--c-violet)", red: "var(--c-red)", grey: "var(--c-grey)",
    blueT: "var(--c-blue-tint)", orangeT: "var(--c-orange-tint)", greenT: "var(--c-green-tint)",
    violetT: "var(--c-violet-tint)", redT: "var(--c-red-tint)", greyT: "var(--c-grey-tint)",
    ink: "var(--ink)", ink2: "var(--ink-2)", muted: "var(--ink-muted)",
    surface: "var(--surface)", surface2: "var(--surface-2)", grid: "var(--grid)", axis: "var(--axis)", rule: "var(--rule)",
    // text versions (for labels in a series colour, if you must)
    tBlue: "var(--t-blue)", tOrange: "var(--t-orange)", tGreen: "var(--t-green)",
    tViolet: "var(--t-violet)", tRed: "var(--t-red)", tGrey: "var(--t-grey)",
  };
  /** Categorical order (validated for colour-vision deficiencies): use in this order. */
  const series = [C.blue, C.orange, C.green, C.violet, C.red];
  /** Text token matching a series colour. */
  const textOf = (c) => ({ [C.blue]: C.tBlue, [C.orange]: C.tOrange, [C.green]: C.tGreen, [C.violet]: C.tViolet, [C.red]: C.tRed, [C.grey]: C.tGrey }[c] || C.ink);

  // ---------------------------------------------------------------- number formatting
  /** fmt(3.14159, 2) -> "3.14"; fmt(0.5) -> "0.5"; trims nothing unless trim=true. */
  function fmt(x, digits = 2, trim = false) {
    if (x === null || x === undefined || Number.isNaN(x)) return "–";
    let s = (+x).toFixed(digits);
    if (trim && s.includes(".")) s = s.replace(/0+$/, "").replace(/\.$/, "");
    if (s === "-0" || /^-0\.0*$/.test(s)) s = s.slice(1);
    return s.replace("-", "−");
  }
  const pct = (x, digits = 1) => fmt(100 * x, digits) + " %";

  // ---------------------------------------------------------------- chart scaffold
  /**
   * QV.chart(el, opts) -> ch
   *  opts.width/height (default: element size), opts.margin {top,right,bottom,left}
   *  opts.x / opts.y: { domain:[a,b], type:"linear"|"band"|"point"|"log", label, ticks, tickValues,
   *                     format (d3 format string or fn), grid (bool), padding (band), nice (bool), hide (bool) }
   *  ch: { svg, g, x, y, w, h, el, overlay, layer(name), axes(), toData(event) -> [x, y] }
   */
  function chart(el, opts = {}) {
    const W = opts.width || el.clientWidth || 560;
    const H = opts.height || el.clientHeight || 320;
    const m = Object.assign({ top: 14, right: 18, bottom: opts.x && opts.x.label === "" ? 30 : 50, left: 62 }, opts.margin || {});
    if (opts.y && opts.y.hide && !(opts.margin && opts.margin.left !== undefined)) m.left = Math.min(m.left, 16);
    const w = W - m.left - m.right, h = H - m.top - m.bottom;
    el.style.position = el.style.position || "relative";
    const svg = d3.select(el).append("svg").attr("width", W).attr("height", H).attr("viewBox", `0 0 ${W} ${H}`);
    const id = "qv" + Math.random().toString(36).slice(2, 9);
    svg.append("defs").append("clipPath").attr("id", id + "c").append("rect").attr("x", -2).attr("y", -6).attr("width", w + 4).attr("height", h + 8);
    const g = svg.append("g").attr("transform", `translate(${m.left},${m.top})`);
    const overlay = d3.select(el).append("div").style("position", "absolute").style("left", 0).style("top", 0)
      .style("width", W + "px").style("height", H + "px").style("pointer-events", "none").node();

    const mkScale = (o, range) => {
      if (!o) return d3.scaleLinear().domain([0, 1]).range(range);
      let s;
      if (o.type === "band") s = d3.scaleBand().domain(o.domain).range(range).padding(o.padding ?? 0.3);
      else if (o.type === "point") s = d3.scalePoint().domain(o.domain).range(range).padding(o.padding ?? 0.5);
      else if (o.type === "log") s = d3.scaleLog().domain(o.domain).range(range);
      else { s = d3.scaleLinear().domain(o.domain || [0, 1]).range(range); if (o.nice) s.nice(); }
      return s;
    };
    const x = mkScale(opts.x, [0, w]);
    const y = mkScale(opts.y, [h, 0]);
    const layers = {};
    ["back", "grid", "axes", "data", "annot", "front"].forEach((n) => { layers[n] = g.append("g").attr("class", "l-" + n); });
    layers.data.attr("clip-path", opts.clip === false ? null : `url(#${id}c)`);
    layers.clipped = layers.data;
    const ch = { svg, g, x, y, w, h, W, H, m, el, overlay, opts, id, layers };
    ch.layer = (n) => layers[n] || (layers[n] = g.append("g").attr("class", "l-" + n));
    ch.axes = () => drawAxes(ch);
    ch.toData = (event) => {
      const [px, py] = pointOf(event, g.node());   // mouse, pen or touch; also accepts a d3-drag event
      return [x.invert ? x.invert(px) : px, y.invert ? y.invert(py) : py];
    };
    ch.px = (xv) => (x.bandwidth ? x(xv) + x.bandwidth() / 2 : x(xv));
    drawAxes(ch);
    return ch;
  }

  function drawAxes(ch) {
    const { x, y, w, h, opts, layers } = ch;
    const fmtOf = (o) => (o && o.format ? (typeof o.format === "function" ? o.format : d3.format(o.format)) : null);
    layers.grid.selectAll("*").remove();
    layers.axes.selectAll("*").remove();
    const xo = opts.x || {}, yo = opts.y || {};
    // grid (recessive, solid hairlines)
    if (yo.grid !== false && !yo.hide && y.ticks) {
      layers.grid.append("g").attr("class", "grid").call(d3.axisLeft(y).tickSize(-w).tickFormat("").tickValues(yo.tickValues || null).ticks(yo.ticks || 5));
    }
    if (xo.grid && x.ticks) {
      layers.grid.append("g").attr("class", "grid").attr("transform", `translate(0,${h})`).call(d3.axisBottom(x).tickSize(-h).tickFormat("").tickValues(xo.tickValues || null).ticks(xo.ticks || 6));
    }
    if (!xo.hide) {
      const ax = d3.axisBottom(x).tickSizeOuter(0).tickPadding(6);
      if (x.ticks) ax.ticks(xo.ticks || 6);
      if (xo.tickValues) ax.tickValues(xo.tickValues);
      if (fmtOf(xo)) ax.tickFormat(fmtOf(xo));
      const ga = layers.axes.append("g").attr("class", "axis x").attr("transform", `translate(0,${h})`).call(ax);
      fixMinus(ga);
      if (xo.label) layers.axes.append("text").attr("class", "axis-label").attr("x", w / 2).attr("y", h + 42).attr("text-anchor", "middle").text(xo.label);
    }
    if (!yo.hide) {
      const ay = d3.axisLeft(y).tickSizeOuter(0).tickPadding(6);
      if (y.ticks) ay.ticks(yo.ticks || 5);
      if (yo.tickValues) ay.tickValues(yo.tickValues);
      if (fmtOf(yo)) ay.tickFormat(fmtOf(yo));
      const ga = layers.axes.append("g").attr("class", "axis y").call(ay);
      fixMinus(ga);
      ga.select(".domain").style("display", yo.domainLine ? null : "none");
      ga.selectAll(".tick line").style("display", "none");
      if (yo.label) layers.axes.append("text").attr("class", "axis-label").attr("transform", `translate(${-ch.m.left + 16},${h / 2}) rotate(-90)`).attr("text-anchor", "middle").text(yo.label);
    }
  }
  function fixMinus(sel) { sel.selectAll(".tick text").each(function () { this.textContent = this.textContent.replace("-", "−"); }); }
  /** Typographic minus for negative numbers in plain text ("-0.5" -> "−0.5"). */
  const minusText = (s) => String(s).replace(/(^|[\s(\[=:,;\/])-(?=\d|\.\d)/g, "$1−");
  /** Same for the text nodes of an HTML element (maths rendered by KaTeX is left alone). */
  function fixMinusDom(el) {
    const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.parentElement && n.parentElement.closest(".katex") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT) });
    for (let n = w.nextNode(); n; n = w.nextNode()) { const v = minusText(n.nodeValue); if (v !== n.nodeValue) n.nodeValue = v; }
  }

  // ---------------------------------------------------------------- marks (data coordinates)
  const layerOf = (ch, o) => ch.layer(o.layer || "data");
  const curveOf = (c) => ({ linear: d3.curveLinear, monotone: d3.curveMonotoneX, step: d3.curveStepAfter, stepBefore: d3.curveStepBefore, basis: d3.curveBasis }[c || "linear"]);

  /** Polyline through [[x,y],...]. o: {color, width, dash, curve, opacity, layer, cls} */
  function line(ch, pts, o = {}) {
    const gen = d3.line().x((d) => ch.x(d[0])).y((d) => ch.y(d[1])).curve(curveOf(o.curve)).defined((d) => Number.isFinite(d[1]));
    return layerOf(ch, o).append("path").datum(pts).attr("class", o.cls || null).attr("d", gen)
      .style("fill", "none").style("stroke", o.color || C.blue).style("stroke-width", o.width || 2.5)
      .style("stroke-linejoin", "round").style("stroke-linecap", "round")
      .style("stroke-dasharray", o.dash === true ? "7 5" : o.dash || null).style("opacity", o.opacity ?? 1);
  }
  /** Update a path created by line() with new points. */
  function setLine(ch, path, pts, curve) {
    const gen = d3.line().x((d) => ch.x(d[0])).y((d) => ch.y(d[1])).curve(curveOf(curve)).defined((d) => Number.isFinite(d[1]));
    path.datum(pts).attr("d", gen);
  }
  /** Filled area between y0 (default 0) and the points. o: {color, opacity, y0, layer} */
  function area(ch, pts, o = {}) {
    const y0 = o.y0 ?? 0;
    const gen = d3.area().x((d) => ch.x(d[0])).y0((d) => ch.y(d.length > 2 ? d[2] : y0)).y1((d) => ch.y(d[1])).curve(curveOf(o.curve));
    return layerOf(ch, o).append("path").datum(pts).attr("d", gen).attr("class", o.cls || null)
      .style("fill", o.color || C.blue).style("fill-opacity", o.opacity ?? 0.16).style("stroke", "none");
  }
  function setArea(ch, path, pts, y0 = 0, curve) {
    const gen = d3.area().x((d) => ch.x(d[0])).y0((d) => ch.y(d.length > 2 ? d[2] : y0)).y1((d) => ch.y(d[1])).curve(curveOf(curve));
    path.datum(pts).attr("d", gen);
  }
  /** Sample f on [from, to]: returns [[x, f(x)], ...]. */
  function sample(f, from, to, n = 240) { const out = []; for (let i = 0; i <= n; i++) { const x = from + (to - from) * i / n; out.push([x, f(x)]); } return out; }
  function fnLine(ch, f, o = {}) { const [a, b] = ch.x.domain(); return line(ch, sample(f, o.from ?? a, o.to ?? b, o.n), o); }
  function fnArea(ch, f, o = {}) { const [a, b] = ch.x.domain(); return area(ch, sample(f, o.from ?? a, o.to ?? b, o.n), o); }

  /** Dots with a surface ring. pts: [[x,y],...] or objects with o.x/o.y accessors. o: {r, color, ring, opacity, tip(d,i)->html, cls, layer} */
  function dots(ch, pts, o = {}) {
    const gx = o.x || ((d) => d[0]), gy = o.y || ((d) => d[1]);
    const sel = layerOf(ch, Object.assign({ layer: "annot" }, o)).append("g").attr("class", o.cls || null).selectAll("circle").data(pts).join("circle")
      .attr("cx", (d) => ch.x(gx(d))).attr("cy", (d) => ch.y(gy(d))).attr("r", o.r || 5.5)
      .style("fill", typeof o.color === "function" ? o.color : () => o.color || C.blue)
      .style("stroke", o.ring === false ? "none" : C.surface).style("stroke-width", o.ring === false ? 0 : 2)
      .style("opacity", o.opacity ?? 1);
    if (o.tip) attachTip(ch, sel, o.tip);
    return sel;
  }
  /**
   * Bars from a baseline. data: [{x, y, color?, label?}] (x is a category for band scales, a number otherwise).
   * o: {width (data units, numeric x), color, base (0), tip(d)->html, labels(d)->string, horizontal}
   */
  function bars(ch, data, o = {}) {
    const base = o.base ?? 0;
    const band = !!ch.x.bandwidth;
    const bw = band ? Math.min(ch.x.bandwidth(), o.maxWidth || 64) : Math.abs(ch.x(o.width ?? 0.8) - ch.x(0));
    const xs = (d) => (band ? ch.x(d.x) + (ch.x.bandwidth() - bw) / 2 : ch.x(d.x) - bw / 2);
    const gsel = layerOf(ch, o).append("g").attr("class", o.cls || null);
    const sel = gsel.selectAll("path").data(data).join("path")
      .attr("d", (d) => barPath(xs(d), ch.y(Math.max(d.y, base)), bw, Math.abs(ch.y(d.y) - ch.y(base)), d.y >= base, o.radius ?? 4))
      .style("fill", (d) => d.color || o.color || C.blue).style("opacity", o.opacity ?? 1);
    if (o.tip) attachTip(ch, sel, o.tip);
    if (o.labels) {
      ch.layer("annot").append("g").selectAll("text").data(data).join("text").attr("class", "lbl")
        .attr("x", (d) => xs(d) + bw / 2).attr("y", (d) => ch.y(Math.max(d.y, base)) - 6).attr("text-anchor", "middle").text(o.labels);
    }
    sel.update = (nd) => {
      sel.data(nd).attr("d", (d) => barPath(xs(d), ch.y(Math.max(d.y, base)), bw, Math.abs(ch.y(d.y) - ch.y(base)), d.y >= base, o.radius ?? 4))
        .style("fill", (d) => d.color || o.color || C.blue);
      return sel;
    };
    return sel;
  }
  /** Rectangle with 4px rounded data end, square at the baseline. */
  function barPath(x, y, w, h, up = true, r = 4) {
    r = Math.max(0, Math.min(r, w / 2, h));
    if (h <= 0) return `M${x},${y}h${w}`;
    if (up) return `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`;
    return `M${x},${y}V${y + h - r}Q${x},${y + h} ${x + r},${y + h}H${x + w - r}Q${x + w},${y + h} ${x + w},${y + h - r}V${y}Z`;
  }
  /** Rectangle in data coordinates (x0..x1, y0..y1). o: {fill, opacity, stroke, width, rx, layer} */
  function rect(ch, x0, x1, y0, y1, o = {}) {
    const r = layerOf(ch, o).append("rect");
    const set = (a, b, c, d) => r.attr("x", Math.min(ch.x(a), ch.x(b))).attr("width", Math.abs(ch.x(b) - ch.x(a)))
      .attr("y", Math.min(ch.y(c), ch.y(d))).attr("height", Math.abs(ch.y(d) - ch.y(c)));
    set(x0, x1, y0, y1);
    r.attr("rx", o.rx || 0).style("fill", o.fill || C.blueT).style("fill-opacity", o.opacity ?? 1)
      .style("stroke", o.stroke || "none").style("stroke-width", o.width || 1.5).style("stroke-dasharray", o.dash || null);
    r.set = set;
    return r;
  }
  /** Vertical reference line at x. o: {color, dash, width, label, labelPos:"top"|"bottom", y0, y1} */
  function vline(ch, xv, o = {}) {
    const gg = layerOf(ch, Object.assign({ layer: "annot" }, o)).append("g");
    const ln = gg.append("line").style("stroke", o.color || C.ink2).style("stroke-width", o.width || 2).style("stroke-dasharray", o.dash === true ? "6 4" : o.dash || null);
    const tx = gg.append("text").attr("class", o.labelCls || "lbl").attr("text-anchor", o.anchor || "middle");
    gg.set = (v, label) => {
      const ya = o.y0 ?? ch.y.domain()[0], yb = o.y1 ?? ch.y.domain()[ch.y.domain().length - 1];   // current domain
      const px = ch.px(v);
      ln.attr("x1", px).attr("x2", px).attr("y1", ch.y(ya)).attr("y2", ch.y(yb));
      if (label !== undefined) tx.text(label);
      tx.attr("x", px + (o.dx || 0)).attr("y", o.labelPos === "bottom" ? ch.y(ya) - 6 : ch.y(yb) - 6 + (o.dy || 0));
      return gg;
    };
    gg.set(xv, o.label || "");
    return gg;
  }
  function hline(ch, yv, o = {}) {
    const gg = layerOf(ch, Object.assign({ layer: "annot" }, o)).append("g");
    const ln = gg.append("line").style("stroke", o.color || C.ink2).style("stroke-width", o.width || 2).style("stroke-dasharray", o.dash === true ? "6 4" : o.dash || null);
    const tx = gg.append("text").attr("class", o.labelCls || "lbl").attr("text-anchor", o.anchor || "end");
    gg.set = (v, label) => {
      const xa = o.x0 ?? ch.x.domain()[0], xb = o.x1 ?? ch.x.domain()[ch.x.domain().length - 1];   // current domain
      ln.attr("x1", ch.px(xa)).attr("x2", ch.px(xb)).attr("y1", ch.y(v)).attr("y2", ch.y(v));
      if (label !== undefined) tx.text(label);
      tx.attr("x", ch.px(xb) + (o.dx || 0)).attr("y", ch.y(v) - 6 + (o.dy || 0));
      return gg;
    };
    gg.set(yv, o.label || "");
    return gg;
  }
  /** Segment between two data points. o: {color, width, dash, arrow (bool), layer} */
  function segment(ch, x1, y1, x2, y2, o = {}) {
    const s = layerOf(ch, Object.assign({ layer: "annot" }, o)).append("line")
      .style("stroke", o.color || C.ink2).style("stroke-width", o.width || 2).style("stroke-dasharray", o.dash === true ? "6 4" : o.dash || null);
    if (o.arrow) s.attr("marker-end", `url(#${arrowMarker(ch, o.color || C.ink2)})`);
    s.set = (a, b, c, d) => s.attr("x1", ch.x(a)).attr("y1", ch.y(b)).attr("x2", ch.x(c)).attr("y2", ch.y(d));
    s.set(x1, y1, x2, y2);
    return s;
  }
  const _markers = {};
  function arrowMarker(ch, color) {
    const key = ch.id + color;
    if (_markers[key]) return _markers[key];
    const id = ch.id + "a" + Object.keys(_markers).length;
    ch.svg.select("defs").append("marker").attr("id", id).attr("viewBox", "0 0 10 10").attr("refX", 9).attr("refY", 5)
      .attr("markerWidth", 7).attr("markerHeight", 7).attr("orient", "auto-start-reverse")
      .append("path").attr("d", "M0,0L10,5L0,10z").style("fill", color);
    _markers[key] = id;
    return id;
  }
  /** SVG text at data coordinates. o: {anchor, dx, dy, cls ("lbl"|"lbl-muted"|"lbl-strong"), color (text token), size, weight, layer} */
  function text(ch, xv, yv, str, o = {}) {
    const t = layerOf(ch, Object.assign({ layer: "front" }, o)).append("text").attr("class", o.cls || "lbl")
      .attr("text-anchor", o.anchor || "middle").attr("dominant-baseline", o.baseline || null);
    if (o.color) t.style("fill", o.color);
    if (o.size) t.style("font-size", o.size + "px");
    if (o.weight) t.style("font-weight", o.weight);
    t.set = (a, b, s) => { t.attr("x", ch.px(a) + (o.dx || 0)).attr("y", ch.y(b) + (o.dy || 0)); if (s !== undefined) t.text(minusText(s)); return t; };
    t.set(xv, yv, str);
    return t;
  }
  /**
   * KaTeX label in an HTML overlay at data coordinates.
   * o: {anchor:"middle"|"start"|"end", baseline:"middle"|"top"|"bottom", dx, dy, size (px), color (text token), bg (bool)}
   * returns the element with .set(x, y, latex?) and .anchor(anchor, baseline) to change the alignment later
   */
  function tex(ch, xv, yv, latex, o = {}) {
    const d = document.createElement("div");
    d.className = "fo-tex";
    d.style.position = "absolute";
    d.style.fontSize = (o.size || 17) + "px";
    if (o.color) d.style.color = o.color;
    if (o.bg) { d.style.background = "var(--surface)"; d.style.padding = "1px 4px"; d.style.borderRadius = "4px"; }
    d.anchor = (anchor = "middle", baseline = "middle") => {
      const tx = { start: "0%", middle: "-50%", end: "-100%" }[anchor];
      const ty = { top: "0%", middle: "-50%", bottom: "-100%" }[baseline];
      d.style.transform = `translate(${tx},${ty})`;
      return d;
    };
    d.anchor(o.anchor || "middle", o.baseline || "middle");
    ch.overlay.appendChild(d);
    d.set = (a, b, l) => {
      if (l !== undefined) d.innerHTML = window.Deck && Deck.tex ? Deck.tex(l) : l;
      d.style.left = (ch.m.left + ch.px(a) + (o.dx || 0)) + "px";
      d.style.top = (ch.m.top + ch.y(b) + (o.dy || 0)) + "px";
      return d;
    };
    d.set(xv, yv, latex);
    return d;
  }

  // ---------------------------------------------------------------- tooltip, drag, animation
  function tooltipFor(ch) {
    if (ch._tip) return ch._tip;
    const t = document.createElement("div");
    t.className = "qv-tip";
    ch.el.appendChild(t);
    // On touch screens there is no hover: a tap shows the tooltip and the finger lifts at once.
    // So after a touch the tooltip stays for a moment instead of vanishing with the "leave" event.
    let lastType = "mouse", timer = null;
    ch.el.addEventListener("pointerover", (e) => { lastType = e.pointerType || "mouse"; }, true);
    ch.el.addEventListener("pointerdown", (e) => { lastType = e.pointerType || "mouse"; }, true);
    const TOUCH_MS = 2800;
    ch._tip = {
      show(html, event) {
        clearTimeout(timer); timer = null;
        t.innerHTML = html;
        const r = ch.el.getBoundingClientRect();
        const sc = r.width / ch.el.offsetWidth || 1;          // the slide is CSS-scaled
        let px = (event.clientX - r.left) / sc + 14, py = (event.clientY - r.top) / sc - 10;
        t.classList.add("on");
        const tw = t.offsetWidth, th = t.offsetHeight;
        if (px + tw > ch.el.offsetWidth) px = px - tw - 28;
        // keep the tooltip inside the slide (between title bar and footer)
        const slide = ch.el.closest(".slide");
        if (slide) {
          const sr = slide.getBoundingClientRect();
          px = Math.max((sr.left - r.left) / sc + 4, Math.min((sr.right - r.left) / sc - tw - 4, px));
          py = Math.max((sr.top - r.top) / sc + 34, Math.min((sr.bottom - r.top) / sc - th - 32, py));
        }
        t.style.left = px + "px"; t.style.top = py + "px";
      },
      /** hide the tooltip (after a short delay on touch screens); then() runs when it is really hidden */
      hide(then) {
        clearTimeout(timer); timer = null;
        const off = () => { t.classList.remove("on"); if (typeof then === "function") then(); };
        if (lastType === "touch" && t.classList.contains("on")) timer = setTimeout(off, TOUCH_MS); else off();
      },
      isTouch: () => lastType === "touch",
    };
    return ch._tip;
  }
  function attachTip(ch, sel, fn) {
    const tip = tooltipFor(ch);
    sel.style("cursor", "default")
      .on("pointerenter.tip pointermove.tip", function (event, d) { const i = sel.nodes().indexOf(this); tip.show(fn(d, i), event); d3.select(this).style("filter", "brightness(1.12)"); })
      .on("pointerleave.tip", function () { const me = d3.select(this); tip.hide(() => me.style("filter", null)); if (!tip.isTouch()) me.style("filter", null); });
  }
  /** Crosshair + readout on hover over the plot area. fn(xData, yData) -> html (or null to hide). */
  function hover(ch, fn, o = {}) {
    const tip = tooltipFor(ch);
    const vl = ch.layer("front").append("line").style("stroke", C.axis).style("stroke-width", 1).style("display", "none")
      .attr("y1", 0).attr("y2", ch.h).style("pointer-events", "none");
    ch.layer("front").append("rect").attr("class", "hit").attr("width", ch.w).attr("height", ch.h)
      .style("touch-action", "none")            // a finger moving over the plot reads values, it does not pan
      .on("pointerdown pointermove", (event) => {
        const [xv, yv] = ch.toData(event);
        const html = fn(xv, yv);
        if (html === null || html === undefined) { tip.hide(); vl.style("display", "none"); return; }
        if (o.crosshair !== false) vl.style("display", null).attr("x1", ch.x(xv)).attr("x2", ch.x(xv));
        tip.show(html, event);
      })
      .on("pointerleave", () => { tip.hide(() => vl.style("display", "none")); if (!tip.isTouch()) vl.style("display", "none"); });
  }
  /**
   * Pointer position of a d3-drag (or any pointer / mouse / touch) event in the coordinates of an SVG node.
   * Touch events carry their position in a Touch object, not on the event itself.
   */
  function pointOf(event, node) {
    const src = event.sourceEvent || event;
    let pt = src;
    if (src.changedTouches || src.touches) {
      const all = Array.from(src.changedTouches || []).concat(Array.from(src.touches || []));
      pt = all.find((t) => t.identifier === event.identifier) || all[0] || src;
    }
    // The slide is scaled to the window with a CSS transform (and a figure can be enlarged with "z").
    // d3.pointer relies on getScreenCTM(), which Safari / WebKit computes without such transforms, so
    // handles would jump there. The bounding box of the <svg> is right in every browser: map through it.
    const svg = node && (node.ownerSVGElement || (node.tagName && node.tagName.toLowerCase() === "svg" ? node : null));
    if (svg && pt && pt.clientX !== undefined && svg.createSVGPoint) {
      const r = svg.getBoundingClientRect();
      const vb = svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width ? svg.viewBox.baseVal : null;
      const w = vb ? vb.width : svg.width.baseVal.value, h = vb ? vb.height : svg.height.baseVal.value;
      if (r.width > 0 && r.height > 0 && w > 0 && h > 0) {
        let q = svg.createSVGPoint();
        q.x = (vb ? vb.x : 0) + (pt.clientX - r.left) * w / r.width;
        q.y = (vb ? vb.y : 0) + (pt.clientY - r.top) * h / r.height;
        if (node !== svg && node.getCTM) { const m = node.getCTM(); if (m) q = q.matrixTransform(m.inverse()); }
        return [q.x, q.y];
      }
    }
    return d3.pointer(pt, node);
  }
  /**
   * Make a selection draggable in data coordinates.
   * fn(xData, yData, d, event) is called during the drag; o.end() after.
   */
  function drag(ch, sel, fn, o = {}) {
    sel.classed("drag", true).call(d3.drag()
      .on("start", function () { d3.select(this).raise(); })
      .on("drag", function (event, d) {
        const [px, py] = pointOf(event, ch.g.node());          // works for mouse, pen and touch
        if (!Number.isFinite(px) || !Number.isFinite(py)) return;
        const xv = ch.x.invert ? ch.x.invert(Math.max(0, Math.min(ch.w, px))) : px;
        const yv = ch.y.invert ? ch.y.invert(Math.max(0, Math.min(ch.h, py))) : py;
        fn(xv, yv, d, event);
      })
      .on("end", (event, d) => o.end && o.end(d, event)));
    return sel;
  }
  /** requestAnimationFrame loop. step(dtSeconds, tSeconds) returns false to stop. -> {start, stop, running} */
  function anim(step) {
    let raf = null, last = 0, t0 = 0;
    const a = {
      running: false,
      start() { if (a.running) return; a.running = true; last = t0 = performance.now(); raf = requestAnimationFrame(loop); },
      stop() { a.running = false; if (raf) cancelAnimationFrame(raf); raf = null; },
    };
    function loop(now) { const dt = (now - last) / 1000; last = now; if (step(dt, (now - t0) / 1000) === false) { a.stop(); return; } if (a.running) raf = requestAnimationFrame(loop); }
    return a;
  }

  // ---------------------------------------------------------------- controls
  /** A control row next to a chart. where: "after" (default) | "before" | an element to append to. */
  function controls(el, where = "after") {
    const row = document.createElement("div");
    row.className = "viz-ctrl";
    if (where instanceof Element) where.appendChild(row);
    else if (where === "before") el.parentNode.insertBefore(row, el);
    else el.parentNode.insertBefore(row, el.nextSibling);
    return row;
  }
  const labelHTML = (s) => (window.Deck && /\$/.test(s) ? s.replace(/\$([^$]+)\$/g, (m, t) => Deck.tex(t)) : s);
  /** Range slider. o: {label, min, max, step, value, fmt(v)->string, onInput(v), width} -> {value(), set(v, fire)} */
  function slider(row, o) {
    const lab = document.createElement("label");
    lab.innerHTML = `<span>${labelHTML(o.label || "")}</span>`;
    const inp = document.createElement("input");
    inp.type = "range"; inp.min = o.min; inp.max = o.max; inp.step = o.step ?? (o.max - o.min) / 100; inp.value = o.value;
    if (o.width) inp.style.width = o.width + "px";
    const val = document.createElement("span"); val.className = "val";
    const f = o.fmt || ((v) => String(v));
    lab.appendChild(inp); lab.appendChild(val); row.appendChild(lab);
    const upd = (fire) => {
      const v = +inp.value;
      inp.style.setProperty("--pct", (100 * (v - +inp.min) / ((+inp.max - +inp.min) || 1)).toFixed(2) + "%");   // filled track
      val.innerHTML = labelHTML(f(v)); fixMinusDom(val);
      if (fire && o.onInput) o.onInput(v);
    };
    inp.addEventListener("input", () => upd(true));
    upd(false);
    return { input: inp, value: () => +inp.value, set(v, fire = true) { inp.value = v; upd(fire); } };
  }
  /** Drop-down. o: {label, options:[[value, label], ...], value, onChange(v)} */
  function select(row, o) {
    const lab = document.createElement("label");
    lab.innerHTML = `<span>${labelHTML(o.label || "")}</span>`;
    const s = document.createElement("select");
    o.options.forEach(([v, l]) => { const op = document.createElement("option"); op.value = v; op.textContent = l; s.appendChild(op); });
    s.value = o.value ?? o.options[0][0];
    s.addEventListener("change", () => { o.onChange && o.onChange(s.value); s.blur(); });
    lab.appendChild(s); row.appendChild(lab);
    return { el: s, value: () => s.value, set(v) { s.value = v; o.onChange && o.onChange(v); } };
  }
  /** Segmented buttons. o: {label, options:[[value, labelHTML], ...], value, onChange(v)} */
  function segmented(row, o) {
    const wrap = document.createElement("label");
    if (o.label) wrap.innerHTML = `<span>${labelHTML(o.label)}</span>`;
    const seg = document.createElement("span"); seg.className = "seg";
    let cur = o.value ?? o.options[0][0];
    const btns = o.options.map(([v, l]) => {
      const b = document.createElement("button"); b.type = "button"; b.innerHTML = labelHTML(l); b.dataset.v = v;
      b.addEventListener("click", () => { api.set(v); });
      seg.appendChild(b); return b;
    });
    const api = {
      value: () => cur,
      set(v, fire = true) { cur = v; btns.forEach((b) => b.classList.toggle("on", String(b.dataset.v) === String(v))); if (fire && o.onChange) o.onChange(v); },
    };
    api.set(cur, false);
    wrap.appendChild(seg); row.appendChild(wrap);
    return api;
  }
  function button(row, label, onClick, o = {}) {
    const b = document.createElement("button"); b.type = "button"; b.innerHTML = labelHTML(label);
    if (o.primary) b.className = "primary";
    b.addEventListener("click", onClick); row.appendChild(b);
    b.setLabel = (l) => { b.innerHTML = labelHTML(l); };
    return b;
  }
  /** Live text in a control row. -> {set(html)} (TeX in $...$ is rendered) */
  function readout(row, html = "") {
    const s = document.createElement("span"); s.className = "readout"; row.appendChild(s);
    const api = { el: s, set(h) { s.innerHTML = labelHTML(h); fixMinusDom(s); return api; } };
    api.set(html);
    return api;
  }
  function spacer(row) { const s = document.createElement("span"); s.className = "sp"; row.appendChild(s); return s; }
  /** Stat tiles. labels: ["Mean", "Median", ...] -> {set(i, value)} */
  function tiles(parent, labels, where = "append") {
    const wrap = document.createElement("div"); wrap.className = "tiles"; wrap.style.setProperty("--n", labels.length);
    const vals = labels.map((l) => { const t = document.createElement("div"); t.className = "tile"; t.innerHTML = `<div class="k">${labelHTML(l)}</div><div class="v">–</div>`; wrap.appendChild(t); return t.querySelector(".v"); });
    if (where === "before") parent.parentNode.insertBefore(wrap, parent); else if (where === "after") parent.parentNode.insertBefore(wrap, parent.nextSibling); else parent.appendChild(wrap);
    return { el: wrap, set(i, v) { vals[i].innerHTML = labelHTML(String(v)); fixMinusDom(vals[i]); } };
  }
  /** HTML legend. items: [{label, color, type:"swatch"|"line"|"dash"|"dot"}] */
  function legend(parent, items, where = "append") {
    const wrap = document.createElement("div"); wrap.className = "viz-legend";
    wrap.innerHTML = items.map((it) => {
      const t = it.type || "swatch";
      const mark = t === "line" || t === "dash" ? `<span class="ln${t === "dash" ? " dash" : ""}" style="border-color:${it.color}"></span>`
        : t === "dot" ? `<span class="dt" style="background:${it.color}"></span>` : `<span class="sw" style="background:${it.color}"></span>`;
      return `<span class="key">${mark}<span>${labelHTML(it.label)}</span></span>`;
    }).join("");
    if (where === "before") parent.parentNode.insertBefore(wrap, parent); else if (where === "after") parent.parentNode.insertBefore(wrap, parent.nextSibling); else parent.appendChild(wrap);
    return wrap;
  }

  // ---------------------------------------------------------------- statistics (course definitions)
  const num = (a) => a.map(Number);
  const sortNum = (a) => num(a).slice().sort((p, q) => p - q);
  const sum = (a) => a.reduce((s, v) => s + +v, 0);
  const mean = (a) => sum(a) / a.length;
  /** Course quantile rule: x_p = x_(ceil(n p)) = min{x | F(x) >= p}. */
  function quantile(a, p) {
    const s = sortNum(a), n = s.length;
    let k = Math.ceil(n * p - 1e-12);
    k = Math.max(1, Math.min(n, k));
    return s[k - 1];
  }
  /** Course median: x_(ceil(n/2)). */
  const median = (a) => quantile(a, 0.5);
  /** Sample variance (divide by n - 1); ddof = 0 divides by n. */
  function variance(a, ddof = 1) { const m = mean(a); return sum(a.map((v) => (v - m) ** 2)) / (a.length - ddof); }
  const sd = (a, ddof = 1) => Math.sqrt(variance(a, ddof));
  const range = (a) => Math.max(...a) - Math.min(...a);
  const iqr = (a) => quantile(a, 0.75) - quantile(a, 0.25);
  const geomean = (a) => Math.exp(mean(a.map(Math.log)));
  function trimmedMean(a, alpha) { const s = sortNum(a), n = s.length, k = Math.floor(n * alpha); return mean(s.slice(k, n - k)); }
  /** Frequency table: [{x, h, f, H, F}] sorted by value. */
  function freq(a) {
    const m = new Map(); num(a).forEach((v) => m.set(v, (m.get(v) || 0) + 1));
    const xs = [...m.keys()].sort((p, q) => p - q), n = a.length;
    let H = 0;
    return xs.map((x) => { const h = m.get(x); H += h; return { x, h, f: h / n, H, F: H / n }; });
  }
  /** Empirical CDF as a function F(x). */
  function ecdfFn(a) { const s = sortNum(a), n = s.length; return (x) => d3.bisectRight(s, x) / n; }
  /** Five-number summary for a boxplot with fences k * IQR (course rule quantiles). */
  function fiveNum(a, k = 1.5) {
    const s = sortNum(a);
    const q1 = quantile(s, 0.25), q2 = quantile(s, 0.5), q3 = quantile(s, 0.75), I = q3 - q1;
    const lo = q1 - k * I, hi = q3 + k * I;
    const inside = s.filter((v) => v >= lo && v <= hi);
    return { min: s[0], max: s[s.length - 1], q1, median: q2, q3, iqr: I, fenceLo: lo, fenceHi: hi,
      whiskerLo: inside.length ? inside[0] : q1, whiskerHi: inside.length ? inside[inside.length - 1] : q3,
      outliers: s.filter((v) => v < lo || v > hi) };
  }
  function cov(x, y) { const mx = mean(x), my = mean(y); return sum(x.map((v, i) => (v - mx) * (y[i] - my))) / (x.length - 1); }
  const corr = (x, y) => cov(x, y) / (sd(x) * sd(y));
  /** Simple OLS fit y = b0 + b1 x with the usual inference quantities. */
  function ols(x, y) {
    const n = x.length, mx = mean(x), my = mean(y);
    const sxx = sum(x.map((v) => (v - mx) ** 2)), sxy = sum(x.map((v, i) => (v - mx) * (y[i] - my)));
    const b1 = sxy / sxx, b0 = my - b1 * mx;
    const yhat = x.map((v) => b0 + b1 * v), resid = y.map((v, i) => v - yhat[i]);
    const rss = sum(resid.map((e) => e * e)), tss = sum(y.map((v) => (v - my) ** 2)), ess = tss - rss;
    const s2 = rss / (n - 2), s = Math.sqrt(s2);
    const seB1 = s / Math.sqrt(sxx), seB0 = s * Math.sqrt(1 / n + mx * mx / sxx);
    return { n, b0, b1, yhat, resid, rss, tss, ess, r2: ess / tss, s, s2, seB0, seB1, mx, my, sxx, sxy, predict: (v) => b0 + b1 * v };
  }
  const logistic = (z) => 1 / (1 + Math.exp(-z));

  // ---------------------------------------------------------------- distributions
  const SQ2PI = Math.sqrt(2 * Math.PI);
  const normPdf = (x, mu = 0, s = 1) => Math.exp(-0.5 * ((x - mu) / s) ** 2) / (s * SQ2PI);
  function erf(x) {
    // W. J. Cody-type rational approximation via erfc continued fraction; |error| < 1e-12 for practical x
    const t = 1 / (1 + 0.5 * Math.abs(x));
    const y = 1 - t * Math.exp(-x * x - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 +
      t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
    return x >= 0 ? y : -y;
  }
  function normCdf(x, mu = 0, s = 1) {
    const z = (x - mu) / s;
    if (z < -8) return 0; if (z > 8) return 1;
    // series / continued fraction for high accuracy (4+ decimals exact as in tables)
    if (Math.abs(z) < 3) {
      let sumv = z, term = z;
      for (let i = 1; i < 200; i++) { term *= z * z / (2 * i + 1); sumv += term; if (Math.abs(term) < 1e-16) break; }
      return 0.5 + sumv * Math.exp(-z * z / 2) / SQ2PI;
    }
    return 0.5 * (1 + erf(z / Math.SQRT2));
  }
  /** Inverse standard normal (Acklam), then scaled. */
  function normInv(p, mu = 0, s = 1) {
    if (p <= 0) return -Infinity; if (p >= 1) return Infinity;
    const a = [-3.969683028665376e1, 2.209460984245205e2, -2.759285104469687e2, 1.383577518672690e2, -3.066479806614716e1, 2.506628277459239];
    const b = [-5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2, 6.680131188771972e1, -1.328068155288572e1];
    const c = [-7.784894002430293e-3, -3.223964580411365e-1, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783];
    const d = [7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996, 3.754408661907416];
    const pl = 0.02425; let q, r, x;
    if (p < pl) { q = Math.sqrt(-2 * Math.log(p)); x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
    else if (p <= 1 - pl) { q = p - 0.5; r = q * q; x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1); }
    else { q = Math.sqrt(-2 * Math.log(1 - p)); x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
    // one Newton step for full precision
    const e = normCdf(x) - p; x = x - e * SQ2PI * Math.exp(x * x / 2);
    return mu + s * x;
  }
  function lgamma(x) {
    const g = 7, cf = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
    if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - lgamma(1 - x);
    x -= 1; let a = cf[0]; const t = x + g + 0.5;
    for (let i = 1; i < g + 2; i++) a += cf[i] / (x + i);
    return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
  }
  function betacf(a, b, x) {
    const MAXIT = 300, EPS = 3e-16, FPMIN = 1e-300;
    let qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap;
    if (Math.abs(d) < FPMIN) d = FPMIN; d = 1 / d; let h = d;
    for (let m = 1; m <= MAXIT; m++) {
      const m2 = 2 * m; let aa = m * (b - m) * x / ((qam + m2) * (a + m2));
      d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN; c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN; d = 1 / d; h *= d * c;
      aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
      d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN; c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN; d = 1 / d;
      const del = d * c; h *= del; if (Math.abs(del - 1) < EPS) break;
    }
    return h;
  }
  /** Regularised incomplete beta I_x(a, b). */
  function betaInc(x, a, b) {
    if (x <= 0) return 0; if (x >= 1) return 1;
    const bt = Math.exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * Math.log(x) + b * Math.log(1 - x));
    return x < (a + 1) / (a + b + 2) ? bt * betacf(a, b, x) / a : 1 - bt * betacf(b, a, 1 - x) / b;
  }
  const tPdf = (x, df) => Math.exp(lgamma((df + 1) / 2) - lgamma(df / 2)) / Math.sqrt(df * Math.PI) * (1 + x * x / df) ** (-(df + 1) / 2);
  function tCdf(x, df) { const ib = betaInc(df / (df + x * x), df / 2, 0.5); return x >= 0 ? 1 - 0.5 * ib : 0.5 * ib; }
  function invert(cdf, p, lo, hi) { for (let i = 0; i < 200; i++) { const mid = (lo + hi) / 2; if (cdf(mid) < p) lo = mid; else hi = mid; if (hi - lo < 1e-12) break; } return (lo + hi) / 2; }
  const tInv = (p, df) => invert((x) => tCdf(x, df), p, -1e3, 1e3);
  const fPdf = (x, d1, d2) => (x <= 0 ? 0 : Math.exp(0.5 * d1 * Math.log(d1 * x) + 0.5 * d2 * Math.log(d2) - 0.5 * (d1 + d2) * Math.log(d1 * x + d2) - Math.log(x) - (lgamma(d1 / 2) + lgamma(d2 / 2) - lgamma((d1 + d2) / 2))));
  const fCdf = (x, d1, d2) => (x <= 0 ? 0 : betaInc(d1 * x / (d1 * x + d2), d1 / 2, d2 / 2));
  const fInv = (p, d1, d2) => invert((x) => fCdf(x, d1, d2), p, 0, 1e4);
  function gammaP(a, x) {
    if (x <= 0) return 0;
    if (x < a + 1) { let ap = a, s = 1 / a, del = s; for (let n = 0; n < 500; n++) { ap += 1; del *= x / ap; s += del; if (Math.abs(del) < Math.abs(s) * 1e-15) break; } return s * Math.exp(-x + a * Math.log(x) - lgamma(a)); }
    let b = x + 1 - a, c = 1e300, d = 1 / b, h = d;
    for (let i = 1; i < 500; i++) { const an = -i * (i - a); b += 2; d = an * d + b; if (Math.abs(d) < 1e-300) d = 1e-300; c = b + an / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; const del = d * c; h *= del; if (Math.abs(del - 1) < 1e-15) break; }
    return 1 - Math.exp(-x + a * Math.log(x) - lgamma(a)) * h;
  }
  const chi2Pdf = (x, k) => (x <= 0 ? 0 : Math.exp((k / 2 - 1) * Math.log(x) - x / 2 - (k / 2) * Math.log(2) - lgamma(k / 2)));
  const chi2Cdf = (x, k) => gammaP(k / 2, x / 2);
  const binomPmf = (k, n, p) => Math.exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) + k * Math.log(p) + (n - k) * Math.log(1 - p));

  // ---------------------------------------------------------------- random numbers (seeded, reproducible)
  function rng(seed = 1) {
    let a = seed >>> 0;
    const uniform = () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    let spare = null;
    const normal = (mu = 0, s = 1) => {
      if (spare !== null) { const v = spare; spare = null; return mu + s * v; }
      let u = 0, v = 0; while (u === 0) u = uniform(); v = uniform();
      const r = Math.sqrt(-2 * Math.log(u)); spare = r * Math.sin(2 * Math.PI * v); return mu + s * r * Math.cos(2 * Math.PI * v);
    };
    return {
      uniform, normal,
      int: (lo, hi) => lo + Math.floor(uniform() * (hi - lo + 1)),
      exp: (rate = 1) => -Math.log(1 - uniform()) / rate,
      choice: (arr) => arr[Math.floor(uniform() * arr.length)],
      sample: (arr, n) => Array.from({ length: n }, () => arr[Math.floor(uniform() * arr.length)]),
    };
  }

  // ---------------------------------------------------------------- components
  /**
   * Histogram (density scale by default: area = relative frequency).
   * o: {breaks:[c0..ck], counts:[h1..hk]} or {data, breaks}; density (true), color, xLabel, yLabel,
   *    yMax, highlight:[class indices], tip (default shows class, h, f, density), labels (fn), x/y overrides
   */
  function histogram(el, o) {
    const br = o.breaks;
    const counts = o.counts || br.slice(1).map((b, i) => o.data.filter((v) => (i === 0 ? v >= br[0] : v > br[i]) && v <= b).length);
    const n = sum(counts);
    const cls = counts.map((h, i) => {
      const wdt = br[i + 1] - br[i];
      return { i, a: br[i], b: br[i + 1], h, f: h / n, dens: h / n / wdt };
    });
    const density = o.density !== false;
    const val = (c) => (density ? c.dens : c.h);
    const yMax = o.yMax || d3.max(cls, val) * 1.15;
    const ch = chart(el, Object.assign({
      x: Object.assign({ domain: [br[0], br[br.length - 1]], label: o.xLabel || "", tickValues: br }, o.x || {}),
      y: Object.assign({ domain: [0, yMax], label: o.yLabel || (density ? "Density f / width" : "Absolute frequency"), format: density ? undefined : "d" }, o.y || {}),
    }, o.chart || {}));
    const hl = new Set(o.highlight || []);
    const sel = ch.layer("data").append("g").selectAll("path").data(cls).join("path")
      .attr("d", (c) => {
        const x0 = ch.x(c.a) + 1, x1 = ch.x(c.b) - 1;    // 2px surface gap between adjacent bars
        return barPath(x0, ch.y(val(c)), x1 - x0, ch.y(0) - ch.y(val(c)), true, 4);
      })
      .style("fill", (c) => (hl.has(c.i) ? C.orange : o.color || C.blue));
    attachTip(ch, sel, o.tip || ((c) => `<b>${c.i === 0 && o.closedFirst !== false ? "[" : "("}${fmt(c.a, 2, true)}, ${fmt(c.b, 2, true)}]</b><br>h = ${c.h} &nbsp; f = ${fmt(c.f, 3)}<br>height f/width = ${fmt(c.dens, 4)}`));
    if (o.labels) ch.layer("annot").selectAll("text.hl").data(cls).join("text").attr("class", "lbl").attr("text-anchor", "middle")
      .attr("x", (c) => (ch.x(c.a) + ch.x(c.b)) / 2).attr("y", (c) => ch.y(val(c)) - 6).text(o.labels);
    ch.classes = cls; ch.bars = sel;
    return ch;
  }

  /**
   * Boxplot(s), horizontal by default, with course-rule quartiles and k*IQR fences.
   * o: {groups:[{name, data, color}], k (1.5), vertical (false), points (true: jittered raw data),
   *     annotate (true: label Q1, median, Q3 for a single group), xLabel, domain, fences (false)}
   */
  function boxplot(el, o) {
    const groups = o.groups || [{ name: "", data: o.data }];
    const k = o.k ?? 1.5;
    const stats = groups.map((g) => Object.assign({ g }, fiveNum(g.data, k)));
    const all = groups.flatMap((g) => g.data);
    const pad = (Math.max(...all) - Math.min(...all)) * 0.08 || 1;
    const dom = o.domain || [Math.min(...all) - pad, Math.max(...all) + pad];
    const names = groups.map((g, i) => g.name || String(i));
    const vertical = !!o.vertical;
    const ch = chart(el, Object.assign(vertical
      ? { x: { domain: names, type: "band", padding: 0.45, label: "" }, y: { domain: dom, label: o.xLabel || "" } }
      : { x: { domain: dom, label: o.xLabel || "", grid: true }, y: { domain: names, type: "band", padding: 0.45, hide: groups.length === 1 && !groups[0].name }, margin: { left: groups.some((g) => g.name) ? 110 : 16 } }, o.chart || {}));
    if (!vertical && groups.some((g) => g.name)) {
      ch.layers.axes.selectAll(".axis.y .tick text").style("font-size", "15px").style("fill", C.ink2);
    }
    const tip = tooltipFor(ch);
    const rngJ = rng(7);
    stats.forEach((s, gi) => {
      const col = s.g.color || series[gi % series.length];
      const name = names[gi];
      const bw = (vertical ? ch.x : ch.y).bandwidth();
      const c0 = (vertical ? ch.x : ch.y)(name);
      const P = (v) => (vertical ? ch.y(v) : ch.x(v));
      const gg = ch.layer("data").append("g");
      const mk = (tag) => gg.append(tag);
      const seg = (v1, v2, a, b, st) => {
        const l = mk("line"); if (vertical) l.attr("x1", a).attr("x2", b).attr("y1", P(v1)).attr("y2", P(v2)); else l.attr("y1", a).attr("y2", b).attr("x1", P(v1)).attr("x2", P(v2));
        l.style("stroke", st || C.ink2).style("stroke-width", 2); return l;
      };
      // whiskers
      seg(s.whiskerLo, s.q1, c0 + bw / 2, c0 + bw / 2); seg(s.q3, s.whiskerHi, c0 + bw / 2, c0 + bw / 2);
      seg(s.whiskerLo, s.whiskerLo, c0 + bw * 0.25, c0 + bw * 0.75); seg(s.whiskerHi, s.whiskerHi, c0 + bw * 0.25, c0 + bw * 0.75);
      // box
      const box = mk("rect").attr("rx", 5);
      if (vertical) box.attr("x", c0).attr("width", bw).attr("y", P(s.q3)).attr("height", P(s.q1) - P(s.q3));
      else box.attr("y", c0).attr("height", bw).attr("x", P(s.q1)).attr("width", P(s.q3) - P(s.q1));
      box.style("fill", col).style("fill-opacity", 0.22).style("stroke", col).style("stroke-width", 2.5);
      seg(s.median, s.median, c0, c0 + bw, C.ink).style("stroke-width", 3.5);
      // raw points
      if (o.points !== false) {
        s.g.data.forEach((v) => {
          const j = c0 + bw / 2 + (rngJ.uniform() - 0.5) * bw * 0.5;
          const isOut = v < s.fenceLo || v > s.fenceHi;
          mk("circle").attr(vertical ? "cy" : "cx", P(v)).attr(vertical ? "cx" : "cy", isOut ? c0 + bw / 2 : j).attr("r", isOut ? 6 : 3.6)
            .style("fill", isOut ? C.red : col).style("opacity", isOut ? 1 : 0.55).style("stroke", C.surface).style("stroke-width", isOut ? 2 : 1);
        });
      }
      if (o.fences) {
        [s.fenceLo, s.fenceHi].forEach((v) => seg(v, v, c0 - 8, c0 + bw + 8, C.red).style("stroke-dasharray", "5 4").style("stroke-width", 1.5));
      }
      // hover target
      const hit = mk("rect").attr("class", "hit");
      if (vertical) hit.attr("x", c0).attr("width", bw).attr("y", 0).attr("height", ch.h); else hit.attr("y", c0 - 6).attr("height", bw + 12).attr("x", 0).attr("width", ch.w);
      hit.on("pointermove", (e) => tip.show(`${name ? `<b>${name}</b><br>` : ""}min ${fmt(s.min, 2, true)} · Q1 ${fmt(s.q1, 2, true)} · median <b>${fmt(s.median, 2, true)}</b> · Q3 ${fmt(s.q3, 2, true)} · max ${fmt(s.max, 2, true)}<br>IQR ${fmt(s.iqr, 2, true)} · fences [${fmt(s.fenceLo, 2, true)}, ${fmt(s.fenceHi, 2, true)}]${s.outliers.length ? ` · outliers: ${s.outliers.map((v) => fmt(v, 2, true)).join(", ")}` : ""}`, e))
        .on("pointerleave", () => tip.hide());
      // annotations (single group)
      if (o.annotate && !vertical) {
        // median above the box, quartiles below (no collisions for narrow boxes)
        const lab = (t, v, yy, anchor) => ch.layer("front").append("text").attr("class", "lbl-muted").attr("text-anchor", anchor).attr("x", P(v)).attr("y", yy).text(`${t} = ${fmt(v, 2, true)}`);
        lab("median", s.median, c0 - 10, "middle");
        lab("Q₁", s.q1, c0 + bw + 22, "end");
        lab("Q₃", s.q3, c0 + bw + 22, "start");
      }
    });
    ch.stats = stats;
    return ch;
  }

  /**
   * Empirical CDF as a step function with hover readout F(x) and optional quantile marker.
   * o: {data, xLabel, domain, quantile: p (draws x_p), color, hover (true)}
   */
  function ecdf(el, o) {
    const s = sortNum(o.data), n = s.length, F = ecdfFn(s);
    const fr = freq(s);
    const pad = (s[n - 1] - s[0]) * 0.12 || 1;
    const dom = o.domain || [s[0] - pad, s[n - 1] + pad];
    const ch = chart(el, Object.assign({ x: { domain: dom, label: o.xLabel || "x", ticks: 8 }, y: { domain: [0, 1.05], label: "F(x)", tickValues: [0, 0.25, 0.5, 0.75, 1], format: ".2~f" } }, o.chart || {}));
    const col = o.color || C.blue;
    // horizontal steps
    const steps = [[dom[0], 0]].concat(fr.map((r) => [r.x, r.F]));
    steps.forEach((st, i) => {
      const x1 = i + 1 < steps.length ? steps[i + 1][0] : dom[1];
      segment(ch, st[0], st[1], x1, st[1], { color: col, width: 3, layer: "data" });
    });
    // jumps (dashed) + closed / open dots
    fr.forEach((r, i) => {
      const prevF = i ? fr[i - 1].F : 0;
      segment(ch, r.x, prevF, r.x, r.F, { color: col, width: 1.5, dash: "3 4", layer: "data" });
    });
    dots(ch, fr.map((r, i) => [r.x, i ? fr[i - 1].F : 0]), { r: 4.5, color: C.surface, ring: false, cls: "open" }).style("stroke", col).style("stroke-width", 2);
    dots(ch, fr.map((r) => [r.x, r.F]), { r: 5, color: col, tip: (d) => `F(${fmt(d[0], 2, true)}) = ${fmt(d[1], 3, true)}` });
    if (o.quantile) {
      const p = o.quantile, xp = quantile(s, p);
      hline(ch, p, { color: C.orange, dash: true, x1: xp, label: "" });
      vline(ch, xp, { color: C.orange, dash: true, y1: p, label: "" });
      tex(ch, xp, 0.03, `x_{${p}} = ${fmt(xp, 2, true)}`, { anchor: "start", dx: 8, bg: true });
    }
    if (o.hover !== false) hover(ch, (xv) => `F(${fmt(xv, 2)}) = <b>${fmt(F(xv), 3, true)}</b><br>share of values ≤ ${fmt(xv, 2)}`);
    ch.F = F; ch.freq = fr;
    return ch;
  }

  /**
   * Density curve with shaded regions.
   * o: {pdf(x), domain:[a,b], yMax, xLabel, yLabel, color, regions:[{from, to, color, opacity, label}], ticks, tickValues}
   * returns ch with ch.setRegions(regions) and ch.setPdf(pdf)
   */
  function density(el, o) {
    const [a, b] = o.domain;
    let pdf = o.pdf;
    const yMax = o.yMax || d3.max(sample(pdf, a, b, 200), (d) => d[1]) * 1.12;
    const ch = chart(el, Object.assign({
      x: { domain: [a, b], label: o.xLabel ?? "", ticks: o.ticks, tickValues: o.tickValues, format: o.xFormat },
      y: { domain: [0, yMax], label: o.yLabel || "", hide: o.yLabel === undefined, grid: false },
    }, o.chart || {}));
    const regG = ch.layer("data").append("g");
    const curve = line(ch, sample(pdf, a, b), { color: o.color || C.blue, width: 2.5 });
    const baseline = segment(ch, a, 0, b, 0, { color: C.axis, width: 1, layer: "data" });
    ch.setRegions = (regs = []) => {
      regG.selectAll("*").remove();
      regs.forEach((r) => {
        const lo = Math.max(a, r.from ?? a), hi = Math.min(b, r.to ?? b);
        if (hi <= lo) return;
        area(ch, sample(pdf, lo, hi, 120), { color: r.color || C.orange, opacity: r.opacity ?? 0.45 }).remove().each(function () { regG.node().appendChild(this); });
      });
    };
    ch.setPdf = (f) => { pdf = f; setLine(ch, curve, sample(pdf, a, b)); };
    ch.setRegions(o.regions || []);
    ch.curve = curve; ch.baseline = baseline;
    return ch;
  }

  /**
   * Scatter plot with optional regression line, residual segments and residual squares.
   * o: {x:[...], y:[...], xLabel, yLabel, xDomain, yDomain, line: "ols" | {b0, b1} | null,
   *     residuals (bool), squares (bool), tip, color}
   * returns ch with ch.setLine(b0, b1) -> RSS, ch.fit (OLS result)
   */
  function scatter(el, o) {
    const X = o.x, Y = o.y;
    const padX = (Math.max(...X) - Math.min(...X)) * 0.1 || 1, padY = (Math.max(...Y) - Math.min(...Y)) * 0.15 || 1;
    const ch = chart(el, Object.assign({
      x: { domain: o.xDomain || [Math.min(...X) - padX, Math.max(...X) + padX], label: o.xLabel || "x" },
      y: { domain: o.yDomain || [Math.min(...Y) - padY, Math.max(...Y) + padY], label: o.yLabel || "y" },
    }, o.chart || {}));
    const fit = ols(X, Y);
    const sqG = ch.layer("data").append("g");
    const resG = ch.layer("data").append("g");
    const ln = line(ch, [], { color: o.lineColor || C.orange, width: 3 });
    const pts = X.map((v, i) => [v, Y[i], i]);
    ch.dotsSel = dots(ch, pts, { r: 6, color: o.color || C.blue, tip: o.tip || ((d) => `(${fmt(d[0], 2, true)}, ${fmt(d[1], 2, true)})`) });
    ch.setLine = (b0, b1) => {
      const [xa, xb] = ch.x.domain();
      setLine(ch, ln, [[xa, b0 + b1 * xa], [xb, b0 + b1 * xb]]);
      const res = X.map((v, i) => Y[i] - (b0 + b1 * v));
      if (o.residuals) {
        resG.selectAll("line").data(pts).join("line")
          .attr("x1", (d) => ch.x(d[0])).attr("x2", (d) => ch.x(d[0])).attr("y1", (d) => ch.y(d[1])).attr("y2", (d) => ch.y(b0 + b1 * d[0]))
          .style("stroke", C.red).style("stroke-width", 2);
      }
      if (o.squares) {
        // squares drawn with equal side lengths in pixels (side = |residual| in y-pixels)
        sqG.selectAll("rect").data(pts).join("rect")
          .attr("x", (d, i) => ch.x(d[0]) + (res[i] > 0 ? 0 : 0))
          .attr("y", (d, i) => Math.min(ch.y(d[1]), ch.y(b0 + b1 * d[0])))
          .attr("width", (d, i) => Math.abs(ch.y(d[1]) - ch.y(b0 + b1 * d[0])))
          .attr("height", (d, i) => Math.abs(ch.y(d[1]) - ch.y(b0 + b1 * d[0])))
          .style("fill", C.red).style("fill-opacity", 0.14).style("stroke", C.red).style("stroke-opacity", 0.5);
      }
      return sum(res.map((e) => e * e));
    };
    if (o.line === "ols") ch.setLine(fit.b0, fit.b1);
    else if (o.line) ch.setLine(o.line.b0, o.line.b1);
    ch.fit = fit; ch.lineSel = ln;
    return ch;
  }

  /** Bar chart of a frequency table: o: {data or table [{x, h}], relative (bool), xLabel, yLabel, highlight (x values), labels (bool)} */
  function freqBars(el, o) {
    const tab = o.table || freq(o.data);
    const n = sum(tab.map((r) => r.h));
    const val = (r) => (o.relative ? r.h / n : r.h);
    const cats = tab.map((r) => String(r.x));
    const ch = chart(el, Object.assign({
      x: { domain: cats, type: "band", label: o.xLabel || "", padding: 0.35 },
      y: { domain: [0, (o.yMax || d3.max(tab, val) * 1.2)], label: o.yLabel || (o.relative ? "Relative frequency" : "Absolute frequency"), format: o.relative ? ".2f" : "d", ticks: o.ticks || 4 },
    }, o.chart || {}));
    const hl = new Set((o.highlight || []).map(String));
    const sel = bars(ch, tab.map((r) => ({ x: String(r.x), y: val(r), color: hl.has(String(r.x)) ? C.orange : o.color, r })), {
      tip: (d) => `<b>${o.xLabel || "x"} = ${d.r.x}</b><br>h = ${d.r.h} &nbsp; f = ${fmt(d.r.h / n, 3)}`,
      labels: o.labels ? (d) => (o.relative ? fmt(d.y, 2) : d.y) : null,
    });
    ch.barsSel = sel;
    return ch;
  }

  // ---------------------------------------------------------------- touch screens
  // Hover read-outs listen to "pointermove". A finger that only taps never moves, so on touch screens a tap
  // inside a figure also counts as a move at that spot: every hover read-out then answers to a tap.
  document.addEventListener("pointerdown", (e) => {
    if (e.pointerType !== "touch" || e.qvSynthetic || !e.target || !e.target.closest || !e.target.closest(".viz")) return;
    let ev;
    try {
      ev = new PointerEvent("pointermove", { bubbles: true, cancelable: true, clientX: e.clientX, clientY: e.clientY, screenX: e.screenX, screenY: e.screenY,
        pointerId: e.pointerId, pointerType: "touch", isPrimary: e.isPrimary, view: window });
    } catch (err) { return; }
    ev.qvSynthetic = true;
    e.target.dispatchEvent(ev);
  }, true);

  // ---------------------------------------------------------------- export
  window.QV = {
    mount, _show, _hide, _mountAll, _themeChanged, _detach, _reattach,
    C, series, textOf, fmt, pct, minusText, fixMinusDom,
    chart, line, setLine, area, setArea, sample, fnLine, fnArea, dots, bars, barPath, rect, vline, hline, segment, text, tex,
    tooltip: tooltipFor, attachTip, hover, drag, pointOf, anim,
    controls, slider, select, segmented, button, readout, spacer, tiles, legend,
    stats: { sum, mean, median, quantile, variance, sd, range, iqr, geomean, trimmedMean, freq, ecdf: ecdfFn, fiveNum, cov, corr, ols, sortNum, logistic },
    dist: { normPdf, normCdf, normInv, tPdf, tCdf, tInv, fPdf, fCdf, fInv, chi2Pdf, chi2Cdf, binomPmf, lgamma, betaInc, erf },
    rng,
    histogram, boxplot, ecdf, density, scatter, freqBars,
  };
})();
