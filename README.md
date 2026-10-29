# STAR Lab paper and letter templates

Reusable templates are kept separate from concrete documents.

| Directory | Contents | Git |
|---|---|---|
| `templates/paper/` | Single- and double-column paper templates, class, sections, and lab assets | Tracked |
| `templates/letter/` | Recommendation letter template, style, and logo | Tracked |
| `projects/papers/` | Concrete papers, imported archives, references, and demos | Ignored |
| `projects/letters/` | Concrete letters, original documents, and PDFs | Ignored |
| `output/` | Reusable template previews and Overleaf ZIPs | Tracked |
| `scripts/` | Project creation, builds, checks, and packaging | Tracked |
| `build/` | Template compilation logs and scratch files | Ignored |

## Create a paper or letter

Run from the repository root:

```sh
python3 scripts/new-project.py paper my-paper
python3 scripts/new-project.py letter my-letter
```

Each command creates an independent, self-contained copy under `projects/`.
It refuses to overwrite an existing project. Edit that copy so personal
content stays out of the reusable templates and Git.

For a paper, edit `paper-info-single.tex` and `sections/single/`, or their
double-column equivalents. Compile `main.tex` or `main-double.tex` from its
project directory with Tectonic or pdfLaTeX.

For a letter, edit `main.tex`. Sender details and the logo are configurable
in `starletter.sty` or through overrides in the letter preamble. Compile
`main.tex` from the project directory with Tectonic or pdfLaTeX.

Youwei Bao's current NTU letter is in `projects/letters/youwei-bao/`.
Its entry point remains `Recommendation_Youwei_Bao.tex`.
Original paper ZIPs are in `projects/papers/archives/`, reference PDFs in
`projects/papers/references/`, adapted sources in `projects/papers/working/`,
and their preview PDFs in `projects/papers/demos/`.

## Build and export templates

```sh
python3 scripts/build.py --engine tectonic
python3 scripts/package.py
python3 scripts/check-modes.py --engine tectonic
```

The paper builder accepts `--offline` and `--bundle PATH`. To preview the
letter template, compile `recommendation-template.tex` from `templates/letter/`
and use an output directory under `build/`.

Packaging includes reusable templates only. Upload a ZIP from `output/` to
Overleaf. Paper ZIPs use `main.tex`; the letter ZIP uses
`recommendation-template.tex`. Select pdfLaTeX.

To rebuild the concrete paper demos from the original archives:

```sh
python3 scripts/build-demos.py --engine tectonic
```

See [paper documentation](templates/paper/README.md) for paper metadata,
modes, and writing components, and [letter documentation](templates/letter/README.txt)
for letter fields. Everything under `/projects/` is ignored, including its
sources, PDFs, and build files. Ignoring a directory does not remove files
already committed to Git history.
