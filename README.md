# STAR Lab publication templates

**STAR = System Trustworthiness and AI Reliability.**

An original publication identity for STAR Lab at George Mason University,
covering AI, software engineering, system security, and ML systems.

| Layout | Main document | Intended use | Citations |
|---|---|---|---|
| Single column | `main.tex` | AI, ML, and ML systems manuscripts | Author–year |
| Double column | `main-double.tex` | Systems, security, and software engineering manuscripts | Numeric |

The single-column design uses Palatino with generous line length and spacing.
The double-column design uses a compact Times-style face. Both share a
midnight-blue and cyan palette, a left-aligned title, an S-and-star
monogram, coordinated sans-serif wordmarks, restrained section headings, and quiet running
headers and footers.
Both use US Letter paper. The full lab name appears beneath the logo row
and in the identifying PDF metadata. The compact logo reads STAR LAB.
Project page, GitHub, and dataset placeholders appear after the abstract.

## Open in Overleaf

1. Select **New Project → Upload Project** and upload one of the ZIPs in `output/`.
2. The single-column ZIP opens with `main.tex`. The double-column ZIP also has
   its correct entry point named `main.tex` for immediate compilation.
3. In the complete kit, choose `main.tex` or `main-double.tex` as the main document.
4. Select **pdfLaTeX** as the compiler and recompile. Bibliography processing
   uses BibTeX and is automatic in Overleaf. No shell escape, downloaded font,
   Python script, or external service is required to build the supplied project.
5. Edit the appropriate `paper-info-*.tex`, then replace the sample sections.

The compiled PDFs are in `output/STAR-single-column.pdf` and
`output/STAR-double-column.pdf`. The manuscript prose is instructional;
unfilled result tables deliberately contain dashes rather than invented data.
Author names, email addresses, and the paper ID are placeholders.

## Project organization

```text
main.tex                     Single-column manuscript
main-double.tex              Double-column manuscript
starpaper.cls                Shared layout, fonts, colors, and modes
paper-info-single.tex        Single-column title and author metadata
paper-info-double.tex        Double-column title and author metadata
macros.tex                   Paper-specific notation
references.bib               Shared bibliography with two real sample entries
sections/single/             Single-column example manuscript
sections/double/             Double-column example manuscript
figures/pipeline.tex          Editable vector architecture figure
assets/star-mark.*           Color vector logo and transparent PNG
assets/star-mark-mono.*      Grayscale vector logo and transparent PNG
assets/star-lockup.*         Custom-drawn STAR LAB wordmark and emblem
assets/star-mark-small.*     Small-use emblem with more open channels
assets/star-signature.*      Full-name signature for larger uses
assets/star-icon-*.png       Transparent icons from 16 to 256 pixels
assets/star-favicon.ico      Multi-resolution favicon
assets/institutions/         Optional official GMU artwork and provenance
assets/*-reverse.*           White-and-cyan versions for dark backgrounds
scripts/build.py             Local compilation helper
scripts/build-demos.py       Compile copies of the supplied example drafts
scripts/make-logo.py         Rebuild the vector and raster logo assets
scripts/package.py           Rebuild Overleaf upload ZIPs
output/                      Compiled previews and upload ZIPs
demo/                        Full example drafts typeset with STAR
build/                       Retained compilation logs and intermediate files
example/                     User's original demonstration archives, unchanged
```

The reusable template and upload ZIPs contain instructional sample prose.
The supplied manuscripts are separately typeset in `demo/`; their adapted
working copies and logs are under `build/demos/`. Their paper text, result
figures, venue styles, and author information are not in the upload ZIPs.

To rebuild those full-paper demonstrations from the untouched archives:

```sh
python3 scripts/build-demos.py --engine tectonic
```

This helper requires Python 3.9 or later and the two supplied archives in
`example/`. It applies the single-column layout to SWExploit and the
double-column layout to DLFloating, preserving the original author
affiliations and included appendices. See `demo/BUILD-REPORT.txt` for local
compiler details and presentation adaptations.

The separate single- and double-column ZIPs contain only the selected
manuscript and its metadata. Their entry point is always `main.tex`.
The complete kit contains both layouts and the ZIP-packaging helper.

## Paper metadata

Use the metadata file for the selected layout:

```tex
\title{Your Paper Title}
\author{First Author\quad Second Author}
\staraffiliation{STAR Lab, George Mason University}
\staremails{first@gmu.edu\quad second@gmu.edu}
\starshorttitle{A Short Running Title}
\startrack{ARTIFICIAL INTELLIGENCE / MACHINE LEARNING}
\starstatus{RESEARCH PREPRINT}
\starversion{October 2026}
\starpaperid{1234}
\starkeywords{keyword one; keyword two; keyword three}
```

The defaults label the output **RESEARCH TEMPLATE**, not an accepted or
published paper. Change that status to reflect the actual manuscript.
Keep running titles short enough to fit the page header. Use superscripts
to map multiple authors to affiliations, as shown in the examples.
`\startrack` records the paper's research area in PDF metadata; the masthead
shows **System Trustworthiness and AI Reliability**. `\starlabname` provides
the full lab name for reuse in the source. Anonymous mode omits the lab name
from the masthead and PDF metadata.
The title block supports explicit line breaks. Author-footnote commands
such as `\thanks` are not part of this class's author interface; put equal
contribution notes in `\staraffiliation` or below the author information.

## Project page, GitHub, and dataset

Three compact, centered resource rows follow the abstract, inspired by the first-page
resource block in [3DCodeVerse](https://arxiv.org/pdf/2610.22341).
Both `paper-info-*.tex` files contain editable placeholders:

```tex
\starproject{}
\stargithub{}
\stardataset{}
```

Fill in a URL to make the row clickable. The URL is shown by default;
an optional short label keeps long addresses compact in two-column papers:

```tex
\starproject{https://example.org/project}
\stargithub{https://github.com/your-org/your-repository}
\stardataset[Dataset on Hugging Face]{https://huggingface.co/datasets/your-org/your-dataset}
```

Empty arguments show gray placeholder text without creating dead hyperlinks.
Delete an unused setter to omit that row, or use `\starhideresources` after
the setters to hide the entire block. Resources are inserted automatically
after the abstract; no command is needed in the paper body. Anonymous mode
hides the block and its PDF hyperlink annotations. Native vector icons and
the template palette work in both color and monochrome modes.

## Modes

```tex
\documentclass[singlecolumn]{starpaper}
\documentclass[twocolumn]{starpaper}
\documentclass[singlecolumn,anonymous]{starpaper}
\documentclass[twocolumn,anonymous,monochrome]{starpaper}
```

Use exactly one of `singlecolumn` and `twocolumn`. Supported options are
limited to those shown; page geometry and type sizes are controlled by the
class rather than forwarded to `article`.

**Anonymous mode** removes all three logo slots, author names,
affiliations, emails, identifying headers and footers, acknowledgments
inserted with `\staracknowledgments`, the resource block, and identifying PDF metadata managed
by this class. It substitutes neutral text and the optional paper ID. It
does not rewrite titles, keywords, prose, self-citations, links in the body, image
metadata, or artifacts: review those yourself. The supplied example prose
discusses STAR by name and must be replaced for an actual blind submission.

**Monochrome mode** changes the built-in palette and emblem to grayscale.
Figures drawn with STAR color names adapt automatically. Imported color
graphics are not converted. The default typographic GMU name follows the
class palette. If you enable the optional official GMU image, it retains its
original colors unless a monochrome image is explicitly supplied.

## Writing components

- Figures: `figure` for one column; `figure*` for both columns. Use
  `\linewidth` inside figures and tables. Wide floats usually move to the
  top of a following page in a two-column paper.
- Tables: `booktabs`, `tabularx`, and `multirow` are already loaded. Put
  table captions above the table, include units, and define missing values.
- Mathematics: AMS math, `theorem`, `lemma`, `proposition`, `definition`,
  `assumption`, and `remark` are provided.
- Algorithms: use `algorithm` with `algpseudocode`; do not also load
  `algorithm2e` or the old `algorithmic` package.
- Code: `listings` is configured for readable shaded code blocks without
  shell escape or a syntax-highlighting service.
- Cross-references: `\autoref{fig:name}` and `\autoref{eq:name}` generate linked,
  typed references. Put `\label` after a figure or table caption.
- Citations: `\citet{key}`, `\citep{key}`, and `\cite{key}` are available
  through `natbib`; `\starbibliography{references}` prints the bibliography.
- Acknowledgments: `\staracknowledgments{...}` hides its contents in
  anonymous mode. An ordinary `\section*{Acknowledgments}` will not.
- Optional callouts: `\starcallout{Heading}{Text}` creates a small tinted
  box. Keep boxes short; they do not break across pages.

## Logo and identity

The STAR mark is a tall, faceted **Polaris** (the North Star, a fixed point
people trust to navigate by), split down the middle. The **navy half** carries
a program graph of square modules with right-angle wiring (software systems);
the **sky-blue half** carries a neural network of round neurons (AI). The
**STAR LAB lettering is drawn as custom vector paths**, and the A has a
star-shaped counter.

The lab palette is `#0A2463` (royal navy) and `#82C3F0` (sky blue).
`STARPrimary` and `STARAccent` are the LaTeX color names; `STARForest` and
`STARGold` remain aliases so older figures still work. Sky blue is used for
rules and accents, not body text.

The master copy of every logo file lives in the lab's `logo/` folder; this
template keeps identical copies in `assets/` so it stays self-contained.
Use the PDF assets in LaTeX, SVG for editing, and transparent PNG for slides
or the web. `star-mark.*` is the emblem, `star-lockup.*` adds the STAR LAB
wordmark, and `star-signature.*` adds the full lab name. `star-mark-small.*`
drops the symbols for 16–32 pixel icons; PNG icons and a favicon are
included. Every form has color, `-mono`, and `-reverse` (dark background)
variants. `\starlogo[32pt]` inserts the emblem; `\starwordmark` inserts the
wordmark. Both respect anonymous and monochrome modes.

To regenerate the logo files, run `python3 scripts/make-logo.py assets`
(requires `rsvg-convert` and `pdftocairo`).

### University and partner institution logos

Both layouts display three separate positions: **STAR Lab | George Mason
University | Partner Institution**. The GMU position defaults to a clean,
two-line typographic university name. It is a text treatment made for this
lab template, not a cropped or altered official university logo. Its sans-serif
type, restrained ink color, and optical size coordinate with the STAR wordmark.

The complete official GMU image is retained as an optional asset, with
provenance in `assets/institutions/README.txt`. To enable it, add
`\stargmulogo{assets/institutions/gmu-logo.png}` to your metadata file.
Use `\stargmutext` to restore the default text treatment.

Configure the third slot in `paper-info-single.tex` or `paper-info-double.tex`:

```tex
% Show a named placeholder (the template default).
\starpartner{Partner Institution}{}

% Replace the placeholder with your collaborator's logo.
% Upload that file to the project before enabling this line.
% \starpartner{Institution Name}{assets/institutions/partner-logo.pdf}

% Optional approved monochrome artwork goes in square brackets.
% \starpartner[assets/institutions/partner-mono.pdf]
%   {Institution Name}{assets/institutions/partner-logo.pdf}

% Hide the third slot for papers without a partner institution.
% \starhidepartner
```

Uploaded PDF, PNG, or JPEG logos are fitted proportionally within the slot.
A logo file is displayed as supplied; its institution name belongs in the
affiliation line as well. To use another official GMU artwork file, use
`\stargmulogo[approved-mono.pdf]{approved-color.pdf}`. With no optional
monochrome file, the original institution logo is retained in monochrome
mode. Anonymous mode hides all logo slots, including custom partner art.


## Compile locally

With a complete TeX distribution containing `latexmk` and pdfLaTeX:

```sh
python3 scripts/build.py
```

With Tectonic:

```sh
python3 scripts/build.py --engine tectonic
# Use --offline when the required TeX resources are already cached.
```

The default pdfLaTeX path uses the standard TeX-distribution fonts.
XeLaTeX/Tectonic uses TeX Gyre Pagella and Heros when available, with
Palatino and Helvetica fallbacks on macOS. Minor font-metric differences
can change line and page breaks between engines; use pdfLaTeX consistently
for Overleaf editing.

The helper retains `compile.log`, TeX logs, and bibliography intermediates
under `build/`, and copies final PDFs into `output/`. To regenerate the
logo, run `python3 scripts/make-logo.py assets` with `rsvg-convert`,
`pdftocairo`, and Arial installed. The final SVGs and PDFs contain vector outlines, so
their use does not require those tools or fonts.
Ordinary manuscript builds use the included PDFs and do not run that script.
To regenerate the upload packages, run `python3 scripts/package.py`.

An optional mode check is available with
`python3 scripts/check-modes.py --engine tectonic`. It compiles neutral
fixtures in both layouts and verifies anonymous text and PDF metadata,
hidden branding and acknowledgments, grayscale-logo selection, clickable
resource URLs, and the absence of resource URL annotations in anonymous mode.
It requires Poppler's `pdfinfo` and `pdftotext`.

## Move to a conference or journal style

This is an original **lab manuscript/preprint style**, not an official COLM,
IEEE, ACM, USENIX, or other venue submission template. A two-column format
alone does not make a manuscript compliant with a venue's requirements.
Use the current official style and instructions for the chosen submission.

1. Start from the venue's official main file, class, and bibliography style.
2. Move `sections/`, `figures/`, `references.bib`, and the needed notation
   from `macros.tex` into that project.
3. Load only the packages the content needs and that the venue allows.
   The examples use AMS math, `booktabs`, `tabularx`, `algorithm`,
   `algpseudocode`, `listings`, `tikz`, `natbib`, and `hyperref`.
4. Replace `\starbibliography` with the venue's bibliography commands,
   `\staracknowledgments` with its acknowledgment mechanism, and
   `\starcallout` with normal prose. Replace the title and author block.
   Port the STAR color definitions only if needed for existing figures.
5. Follow the venue's anonymity, page limits, font, margin, and artifact
   requirements. Keep lab branding off blind-review submissions.

The example ZIPs remain untouched and are not dependencies of these builds.

## Sample reference sources

The sample bibliography was checked against the authors' sources for
[Deep Learning](https://www.deeplearningbook.org/) and
[The Protection of Information in Computer Systems](https://web.mit.edu/saltzer/www/publications/protection/).
