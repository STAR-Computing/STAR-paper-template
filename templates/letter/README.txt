STAR Lab recommendation letter template

Copy this directory, or run from the repository root:
  python3 scripts/new-project.py letter NAME

Edit recommendation-template.tex (renamed main.tex in a new project).
Compile from the directory containing the source:
  tectonic recommendation-template.tex
or:
  pdflatex -interaction=nonstopmode -halt-on-error recommendation-template.tex

For Overleaf, upload output/STAR-letter-Overleaf.zip and select pdfLaTeX.

Customize fields with \renewcommand in the letter preamble:
SenderName, SenderTitle, SenderInstitution, SenderEmail, SenderWebsite,
LabLogo, LetterDate, LetterSubject, LetterPosition, LetterSalutation.
The default logo is assets/star-lockup.pdf. Set LabLogo to {} to omit it.
The closing uses a typed name; no handwritten signature is included.

Keep concrete letters in projects/letters/, which is ignored by Git.
