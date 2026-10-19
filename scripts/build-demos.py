#!/usr/bin/env python3
"""Apply STAR to copies of both example manuscripts and compile into demo/.

Original ZIPs are read only. Working sources and logs live under build/demos/.
Usage: python3 scripts/build-demos.py --engine tectonic [--bundle PATH]
"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]

COLM_INFO = r"""
\title{When Correct Patches Become Vulnerable: Red Teaming LLM-Based Program Repair Agents}
\author{Simin Chen\textsuperscript{1,*}\quad Yixin He\textsuperscript{2,*}\quad
Suman Jana\textsuperscript{1}\quad Baishakhi Ray\textsuperscript{1}}
\staraffiliation{\textsuperscript{1}Columbia University\quad
\textsuperscript{2}University of Southern California\\
\textsuperscript{*}Equal contribution}
\staremails{sc5687@columbia.edu\quad yixinhe@usc.edu\\
suman@cs.columbia.edu\quad rayb@cs.columbia.edu}
\starshorttitle{SWExploit: Red Teaming Program Repair Agents}
\startrack{ARTIFICIAL INTELLIGENCE / SOFTWARE SECURITY}
\starstatus{TEMPLATE DEMO}
\starproject{}
\stargithub{}
\stardataset{}
"""

SP_INFO = r"""
\title{Your Compiler is Backdooring Your Model: Understanding and Exploiting
Compilation Inconsistency Vulnerabilities in Deep Learning Compilers}
\author{Simin Chen\textsuperscript{1}\quad Jinjun Peng\textsuperscript{1}\quad
Yixin He\textsuperscript{2}\quad Junfeng Yang\textsuperscript{1}\quad
Baishakhi Ray\textsuperscript{1}}
\staraffiliation{\textsuperscript{1}Columbia University\quad
\textsuperscript{2}University of Southern California}
\staremails{\{sc5687,jinjun.peng\}@columbia.edu\quad
\{junfeng,rayb\}@cs.columbia.edu\\HeyixInn00@gmail.com}
\starshorttitle{Compilation Inconsistency in Deep Learning Compilers}
\startrack{SYSTEM SECURITY / MACHINE LEARNING SYSTEMS}
\starstatus{TEMPLATE DEMO}
\starproject{}
\stargithub{}
\stardataset{}
"""

LISTINGS = r"""
% The original verbatim bodies are unchanged. Listings replaces minted
% for a self-contained build without shell escape or executing code.
\lstnewenvironment{pythoncode}[1][]{\lstset{style=star,
  language=STARPython,numbers=left,numberstyle=\tiny\color{STARMuted},
  numbersep=7pt,basicstyle=\ttfamily\footnotesize,
  title={\sffamily\bfseries\small #1},aboveskip=10pt,belowskip=10pt}}{}
\lstnewenvironment{prompt}[1][]{\lstset{style=star,language={},
  title={\sffamily\bfseries\small #1},aboveskip=10pt,belowskip=10pt}}{}
\lstnewenvironment{demo}[1][]{\lstset{style=star,language={},
  title={\sffamily\bfseries\small #1},aboveskip=10pt,belowskip=10pt}}{}
\lstnewenvironment{case}[1][]{\lstset{style=star,language={},
  title={\sffamily\bfseries\small #1},aboveskip=10pt,belowskip=10pt}}{}
"""

def strip_comments(text):
    return re.sub(r"(?<!\\)%[^\n]*", "", text)

def prepare(kind):
    is_colm = kind == "colm"
    archive = ROOT / "example" / ("COLM26_SWExploit_CameraReady (1).zip" if is_colm
                                  else "SP26_DLFloating_CameraReady (6).zip")
    target = ROOT / "build" / "demos" / kind
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            if name.endswith("/"):
                continue
            destination = target / name
            if not destination.resolve().is_relative_to(target.resolve()):
                raise ValueError("Unsafe ZIP member")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(z.read(name))
    # Bundled old packages must not shadow the compiler's matching packages.
    for p in target.rglob("*.sty"):
        if p.name in ["natbib.sty", "fancyhdr.sty", "algorithm.sty", "algorithmic.sty"]:
            p.rename(p.with_suffix(".sty.original"))
    cls = (ROOT / "starpaper.cls").read_text()
    if not is_colm:
        # This manuscript uses algorithm2e rather than algorithm/algpseudocode.
        cls = cls.replace(r"\RequirePackage{algorithm}", "")
        cls = cls.replace(r"\RequirePackage{algpseudocode}", "")
        cls = cls.replace(r"\floatname{algorithm}{Algorithm}", "")
        cls = re.sub(r"(?m)^\\algrenewcommand[^\n]*\n", "", cls)
    (target / "starpaper.cls").write_text(cls)
    (target / "assets").mkdir(exist_ok=True)
    for p in (ROOT / "assets").rglob("*"):
        if p.is_file() and p.suffix.lower() in [".pdf", ".png", ".jpg", ".jpeg"]:
            destination = target / "assets" / p.relative_to(ROOT / "assets")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, destination)

    definitions = strip_comments((target / "Text/definition.tex").read_text())
    if is_colm:
        definitions = definitions.split(r"\newtcblisting")[0]
        definitions = definitions.replace(r"\usepackage[most]{tcolorbox}", r"\usepackage{tcolorbox}")
        definitions = re.sub(r"\\tcbuselibrary\{[^}]*\}", "", definitions)
        for package in ["minted", "cleveref", "todonotes", "subcaption"]:
            definitions = re.sub(r"\\usepackage(?:\[[^]]*\])?\{" + package + r"\}", "", definitions)
        definitions += LISTINGS
        definitions += r"""
% Use the active OpenType bold face for Latin mathematical identifiers.
\ifPDFTeX\else
  \DeclareMathAlphabet{\mathbf}{TU}{\rmdefault}{b}{n}
\fi
"""
        problem = target / "Method/problem.tex"
        text = problem.read_text()
        text = text.replace(r" \mathcal{I}^* =", r"\begin{aligned}" + "\n" + r" \mathcal{I}^* &=")
        text = text.replace(r" \quad" + "\n" + r"\text{s.t.}  \quad", r" \\" + "\n" + r"\text{s.t.}\quad &")
        text = text.replace(r"\; \bigwedge \;", r"\\ &\bigwedge\quad")
        text = text.replace(r"\end{equation}", "\\end{aligned}\n\\end{equation}")
        problem.write_text(text)
        body = (target / "colm_main.tex").read_text().split(r"\begin{document}", 1)[1]
        body = re.sub(r"\\ifcolmsubmission.*?\\fi", "", body, flags=re.S)
        body = body.replace(r"\bibliographystyle{colm2026_conference}", r"\bibliographystyle{unsrtnat}")
        main = "\\documentclass[singlecolumn]{starpaper}\n\\input{Text/definition}\n" + COLM_INFO
    else:
        definitions = definitions.replace(r"\usepackage{algorithmic}", "")
        definitions = definitions.replace(r"\usepackage{wasysym}", r"\usepackage[nointegrals]{wasysym}")
        definitions = definitions.replace(r"\newtheorem{definition}{Definition}",
                                          r"\counterwithout{definition}{section}")
        # The source uses bold math only for table-header emphasis. In this
        # offline XeTeX build the cached NewTX bold math font is unavailable;
        # preserve the expressions at normal math weight, keeping text bold.
        definitions += "\n\\ifPDFTeX\\else\\renewcommand{\\boldmath}{\\mathversion{normal}}\\fi\n"
        definitions += r"""
% Classic math accents require a legacy math-operator font in XeTeX.
\ifPDFTeX\else
  \SetSymbolFont{operators}{normal}{OT1}{cmr}{m}{n}
  \SetSymbolFont{operators}{bold}{OT1}{cmr}{m}{n}
\fi
\providecommand{\appendices}{\clearpage\appendix}
"""
        source = (target / "main.tex").read_text()
        (target / "original-main.tex").write_text(source)
        # Preserve the paper body; replace only venue-specific title machinery.
        body = source.split(r"\maketitle", 1)[1]
        body = r"\maketitle" + body
        body = body.replace(r"\pagestyle{plain}", "")
        body = body.replace(r"\IEEEpeerreviewmaketitle", "")
        body = body.replace(r"\bibliographystyle{IEEEtran}", r"\bibliographystyle{unsrtnat}")
        main = "\\documentclass[twocolumn]{starpaper}\n\\input{Text/definition}\n" + SP_INFO
    definitions += "\n\\renewcommand{\\Checkmark}{\\ensuremath{\\checkmark}}\n"
    (target / "Text/definition.tex").write_text(definitions)
    (target / "main.tex").write_text(main + "\n\\begin{document}\n" + body)
    if is_colm:
        # Venue-tuned wrapping collides at the STAR width. Preserve each
        # object's width and contents while using ordinary, non-wrapping floats.
        pattern = r"\\begin\{wrap(figure|table)\}(?:\[[^]]*\])?\{[^}]+\}\{([^}]+)\}(.*?)\\end\{wrap\1\}"
        def unwrap(match):
            environment, width, contents = match.groups()
            contents = contents.replace(width, r"\linewidth")
            return ("\\begin{" + environment + "}[htbp]\n\\centering\n"
                    + "\\begin{minipage}{" + width + "}\n" + contents
                    + "\\end{minipage}\n\\end{" + environment + "}")
        for p in target.rglob("*.tex"):
            if p.name in ["colm_main.tex", "original-main.tex"]:
                continue
            # Mask comment backslashes so disabled sample floats stay disabled.
            text = re.sub(r"(?<!\\)%[^\n]*",
                          lambda m: m.group().replace("\\", "\x00"), p.read_text())
            text = re.sub(pattern, unwrap, text, flags=re.S)
            text = re.sub(r"(?m)^\s*\\vspace\*?\{-[^}]+\}", "", text)
            text = text.replace("\x00", "\\")
            text = text.replace(r"\texttt{sentence-transformers/all-MiniLM-L6-v2}",
                                r"\texttt{sentence-\allowbreak transformers/\allowbreak all-\allowbreak MiniLM-\allowbreak L6-\allowbreak v2}")
            p.write_text(text)
    else:
        # Move font sizing outside math mode and wrap the long metric
        # definitions without changing any mathematical expression.
        p = target / "Setup/process.tex"
        def metric(match):
            contents = match.group(1).strip()
            label = re.match(r"\\label\{[^}]+\}", contents).group()
            contents = contents[len(label):].strip()
            if contents.startswith(r"{\small"):
                assert contents.endswith("}")
                contents = contents[len(r"{\small"):-1].strip()
            else:
                contents = contents.replace(r"\small", "").strip()
            contents = contents.replace(r"\begin{split}", "").replace(r"\end{split}", "").strip()
            contents = re.sub(r"(?:\\;\s*){2}\\forall|\\quad \\forall",
                              lambda m: r"\\ \forall", contents)
            return ("{\\small\n\\begin{equation}\n" + label
                    + "\n\\begin{gathered}\n" + contents
                    + "\n\\end{gathered}\n\\end{equation}\n}")
        text = re.sub(r"\\begin\{equation\}(.*?)\\end\{equation\}", metric,
                      p.read_text(), flags=re.S)
        p.write_text(text)
        # Single-column objects in IEEE's wider columns must fit STAR's gutter.
        for filename, old in [("Text/introduction.tex", r"0.49\textwidth"),
                              ("Result/rq1.tex", r"0.498\textwidth"),
                              ("Table/ablation.tex", r"0.5\textwidth")]:
            p = target / filename
            p.write_text(p.read_text().replace(old, r"\linewidth"))
    return target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", default=shutil.which("tectonic"))
    parser.add_argument("--bundle")
    parser.add_argument("--paper", choices=["colm", "sp", "both"], default="both")
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    papers = ["colm", "sp"] if args.paper == "both" else [args.paper]
    for kind in papers:
        target = prepare(kind)
        print(f"Prepared {target.relative_to(ROOT)}", flush=True)
        if args.prepare_only:
            continue
        cmd = [args.engine, "--keep-logs", "--keep-intermediates"]
        if args.bundle:
            cmd += ["--bundle", args.bundle]
        cmd += ["main.tex"]
        run = subprocess.run(cmd, cwd=target, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        (target / "compile.log").write_text(run.stdout)
        print(run.stdout[-5000:], flush=True)
        if run.returncode:
            raise SystemExit(run.returncode)
        (ROOT / "demo").mkdir(exist_ok=True)
        name = "STAR-COLM-SWExploit-single-column.pdf" if kind == "colm" else "STAR-SP-DLFloating-double-column.pdf"
        shutil.copy2(target / "main.pdf", ROOT / "demo" / name)
        print(f"Created demo/{name}", flush=True)

if __name__ == "__main__":
    main()
