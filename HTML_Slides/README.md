# HTML slides with interactive figures

Browser versions of the five Beamer decks: the same content, frame by frame,
with the static figures replaced by **interactive figures**. You can drag
points and lines, move sliders, run simulations and hover for exact values.

| Part | Deck | Slides | Interactive figures |
|------|------|-------:|-------:|
| 1 | [`Part_1_Descriptive_Statistics.html`](Part_1_Descriptive_Statistics.html) (revision) | 114 | 13 |
| 2 | [`Part_2_Graphical_Representations.html`](Part_2_Graphical_Representations.html) (revision) | 110 | 22 |
| 3 | [`Part_3_Statistical_Inference.html`](Part_3_Statistical_Inference.html) | 198 | 26 |
| 4 | [`Part_4_Regression.html`](Part_4_Regression.html) | 250 | 60 |
| 5 | [`Part_5_Classification.html`](Part_5_Classification.html) | 127 | 15 |

Each deck follows its Beamer deck frame by frame, so the slide counts are the same as the PDF page counts.

Open `index.html` or any deck in a browser by double-clicking it. You need no
server and no internet connection, because the fonts, KaTeX and D3 are bundled
in `assets/`.

## Presenting

| Key | Action |
|-----|--------|
| `→` `space` `PgDn` / `←` `PgUp` | next / previous slide |
| `Home` / `End` | first / last slide |
| `12` `Enter` | go to slide 12 |
| `m` | outline with search |
| `b` | back, after following an internal link |
| `d` | dark / light mode |
| `f` | fullscreen |
| `n` | speaker notes |
| `p` | print, or save as PDF (one slide per page; use "Save as PDF", margins "None") |
| `?` | all keys |

Every slide has its own address (`…/Part_3_Statistical_Inference.html#42`), so
you can link to it directly.

## Authoring

Each slide is a fixed 1280 × 720 canvas that is scaled to the window, so a
slide that fits on one screen fits on every screen. The content area is about
1184 × 590 px.

The engine fits every slide when it is shown:

- **Text-only slides** (no `.viz`) are enlarged up to 135 %, as far as everything
  still fits.
- **Every slide** is then placed optically centred, as Beamer centres frames
  vertically.
- **Opt-outs:** `class="no-fit"` on the `<section>` turns both off. `class="top"`
  keeps the zoom but not the centring, and `class="no-zoom"` on an element stops
  the zoom on its slide.
- **Figure slides** get no zoom, so size their figures to use the space.
- **Line breaks:** inline maths is never separated from the characters that touch
  it, e.g. "$p$-value" or "$250$&nbsp;g".

```html
<section class="slide" data-section="Histogram" data-short="Histogram" data-subsection="Exercises">
  <h2>Slide title</h2>
  … content …
</section>
```

- **Generated slides:** the title page, "About the Lecturer" and "The lecture at
  a glance" are generated (`data-auto="title" | "lecturer" | "course"`). An
  "Overview" slide is inserted automatically before every section, as
  `\AtBeginSection` does in Beamer. A contents slide uses `<div class="toc"
  data-mode="sections"></div>`.
- **Sections:** `data-section` (+ `data-short`), `data-subsection` and
  `data-appendix` go on the first slide of a section or subsection. Main
  sections are numbered 1, 2, …; appendix sections are lettered A, B, ….
- **Blocks:** `.block` (blue), `.block.alert` (red), `.block.example` (green),
  `.block.orange`, `.block.grey`, each with an `<h4>` title. Some blocks get
  their title automatically: `.block.key` ("Key takeaway"), `.block.guiding`
  ("Guiding question") and `.block.problem` ("Problem statement").
  `<p class="inwords">` gives the "In words:" line.
- **Layout:** `<div class="cols" style="--cols: 55fr 45fr">`, with one child per
  column. A `<div>` column is a flex column with a 12 px gap. Font steps are
  `.fs-s`, `.fs-xs`, `.fs-xxs` and `.fs-tiny`.
- **Tables:** `<table class="bt">` gives booktabs rules at 21 px. Set another size
  with `style="font-size:…px"`. Cell highlights are `.hl` (orange), `.hlb`
  (blue), `.hlg` (green) and `.hlr` (red).
- **Maths:** KaTeX with `$…$`, `$$…$$`, `\[…\]` and `\begin{align*}`. Colour
  macros `\blue{}`, `\orange{}`, `\green{}`, `\red{}`, `\violet{}`, `\grey{}` and
  `\hl{}` follow dark mode.
- **Code:** use `<pre class="py">` for code and `<pre class="out">` for its
  output (`data-label="…"` replaces the "Output" label). Python is highlighted
  automatically, and `<`, `>`, `&` must be escaped.
- **Pointers:** `<a class="trynb" data-sec="section 1.2"></a>` (the notebook in
  Colab), `<a class="pycourse" data-what="…"></a>`, `<div class="apxnote">…</div>`,
  `<div class="srcnote">…</div>`.
- **Exercise and solution slides:** a title that starts with "Exercise" or
  "Solution" gets a badge automatically.
- **Speaker notes:** `<aside class="notes">…</aside>` inside a slide.
- **Interactive figures:** `<div class="viz" id="…" style="height:…px"></div>`
  plus `QV.mount("#id", el => { … })`. The API is documented at the top of
  `assets/viz.js`. `QV.stats` follows the course definitions: quantile
  x_(⌈n·p⌉), median x_(⌈n/2⌉), variance with n − 1.

- **Deck-specific code:** each deck keeps its own CSS and helper functions at
  the top of its slide region: a `<style>` block plus a script that defines one
  global: `P2`, `P3A`/`P3B`, `P4A`/`P4B` or `P5X` (Part 1 has none). Ids carry the
  deck prefix (`p1-` … `p5-`).
  Every inline script is wrapped in `(() => { … })();`.

`_template.html` shows every building block once.

## Files

```
HTML_Slides/
├── index.html                 landing page
├── Part_k_<Topic>.html        the decks (one file each)
├── _template.html             building blocks / style guide
└── assets/
    ├── deck.css, deck.js      layout, navigation, generated slides
    ├── viz.js                 chart library (QV) on top of D3
    ├── fonts/                 Source Sans 3, JetBrains Mono (SIL OFL)
    └── vendor/                KaTeX 0.16 (MIT), D3 7.9 (ISC)
```

The PDF decks (LaTeX Beamer) remain the reference version. The numbers on
these slides come from the same data and the same course definitions.
