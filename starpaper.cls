% STAR Lab publication class. Original design; not a conference style file.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{starpaper}[2026/10/18 v1.5 STAR Lab research papers]

\newif\ifstartwocolumn
\newif\ifstaranonymous
\newif\ifstarmonochrome
\DeclareOption{singlecolumn}{\startwocolumnfalse}
\DeclareOption{twocolumn}{\startwocolumntrue}
\DeclareOption{anonymous}{\staranonymoustrue}
\DeclareOption{monochrome}{\starmonochrometrue}
\DeclareOption*{\ClassWarning{starpaper}{Unknown option `\CurrentOption'}}
\ExecuteOptions{singlecolumn}
\ProcessOptions\relax
\ifstartwocolumn
  \LoadClass[10pt,letterpaper,twocolumn]{article}
\else
  \LoadClass[11pt,letterpaper]{article}
\fi

\RequirePackage{iftex}
\ifPDFTeX
  \pdfminorversion=7
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8]{inputenc}
  \ifstartwocolumn
    \RequirePackage{newtxtext}
  \else
    \RequirePackage{mathpazo}
  \fi
  \RequirePackage[scaled=0.92]{helvet}
  \RequirePackage[noupquote]{zi4}
\else
  \AtBeginDvi{\special{pdf:minorversion 7}}
  \RequirePackage[no-math]{fontspec}
  \ifstartwocolumn
    \setmainfont{TeXGyreTermesX}
  \else
    \IfFontExistsTF{TeX Gyre Pagella}{\setmainfont{TeX Gyre Pagella}}
      {\setmainfont{Palatino}}
  \fi
  \IfFontExistsTF{TeX Gyre Heros}{\setsansfont{TeX Gyre Heros}[Scale=0.92]}
    {\setsansfont{Helvetica}[Scale=0.92]}
  \setmonofont{Inconsolatazi4}[Extension=.otf,
    UprightFont=*-Regular,BoldFont=*-Bold,
    ItalicFont=*-Regular,ItalicFeatures={FakeSlant=0.2},
    BoldItalicFont=*-Bold,BoldItalicFeatures={FakeSlant=0.2}]
\fi
\RequirePackage{microtype}
\RequirePackage{geometry}
\ifstartwocolumn
  \geometry{left=0.7in,right=0.7in,top=0.68in,bottom=0.78in,
    headheight=20pt,headsep=16pt,footskip=27pt}
  \setlength{\columnsep}{0.28in}
\else
  \geometry{left=1.1in,right=1.1in,top=0.78in,bottom=0.85in,
    headheight=20pt,headsep=18pt,footskip=29pt}
\fi

\RequirePackage{xcolor}
\definecolor{STARPrimary}{HTML}{1A1650}
\definecolor{STARAccent}{HTML}{0A8FE6}
\definecolor{STARInk}{HTML}{222A3A}
\definecolor{STARMuted}{HTML}{5C6577}
\definecolor{STARLight}{HTML}{F1F5FA}
\definecolor{STARLine}{HTML}{D3DBE7}
\ifstarmonochrome
  \colorlet{STARPrimary}{black}
  \colorlet{STARAccent}{black!60}
  \colorlet{STARInk}{black}
  \colorlet{STARMuted}{black!65}
  \colorlet{STARLight}{black!4}
  \colorlet{STARLine}{black!25}
\fi
% Backward-compatible aliases for existing figures and papers.
\colorlet{STARForest}{STARPrimary}
\colorlet{STARGold}{STARAccent}
\RequirePackage{graphicx}
\RequirePackage{amsmath,amssymb,amsthm}
\ifstartwocolumn
  \ifPDFTeX\RequirePackage{newtxmath}\else\RequirePackage[noOT1]{newtxmath}\fi
\fi
\RequirePackage{booktabs,array,tabularx,multirow}
\RequirePackage{enumitem}
\RequirePackage{caption}
\RequirePackage{algorithm}
\RequirePackage{algpseudocode}
\RequirePackage{listings}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc,fit,backgrounds}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{etoolbox}
\RequirePackage{url}
\ifstartwocolumn
  \RequirePackage[numbers,sort&compress]{natbib}
\else
  \RequirePackage[authoryear,round]{natbib}
\fi
\RequirePackage{hyperref}
\hypersetup{colorlinks=true,allcolors=STARForest,bookmarksnumbered=true,
  pdfdisplaydoctitle=true,pdfborder={0 0 0}}
\urlstyle{tt}
\pdfstringdefDisableCommands{\def\\{ }\def\texttt#1{#1}\def\thanks#1{}%
  \def\textsuperscript#1{}\def\quad{ }\def\qquad{ }\def\and{, }}

% All identifying metadata is controlled here so anonymous mode is consistent.
\newcommand{\starlabname}{System Trustworthiness and AI Reliability}
\newcommand{\star@affiliation}{STAR Lab, George Mason University}
\newcommand{\star@emails}{}
\newcommand{\star@shorttitle}{Research paper}
\newcommand{\star@track}{AI / SOFTWARE / SECURITY / SYSTEMS}
\newcommand{\star@status}{RESEARCH PREPRINT}
\newcommand{\star@paperid}{}
\newcommand{\star@keywords}{}
\newcommand{\star@version}{}
\newcommand{\staraffiliation}[1]{\gdef\star@affiliation{#1}}
\newcommand{\staremails}[1]{\gdef\star@emails{#1}}
\newcommand{\starshorttitle}[1]{\gdef\star@shorttitle{#1}}
\newcommand{\startrack}[1]{\gdef\star@track{#1}}
\newcommand{\starstatus}[1]{\gdef\star@status{#1}}
\newcommand{\starpaperid}[1]{\gdef\star@paperid{#1}}
\newcommand{\starkeywords}[1]{\gdef\star@keywords{#1}}
\newcommand{\starversion}[1]{\gdef\star@version{#1}}
% Optional paper resources, printed after the abstract. Empty URLs display
% placeholders; omitting a setter omits its row. Anonymous mode hides all rows.
\newif\ifstarproject
\newif\ifstargithub
\newif\ifstardataset
\newcommand{\star@projecturl}{}
\newcommand{\star@projectlabel}{}
\newcommand{\star@githuburl}{}
\newcommand{\star@githublabel}{}
\newcommand{\star@dataseturl}{}
\newcommand{\star@datasetlabel}{}
\newcommand{\starproject}[2][]{\starprojecttrue
  \gdef\star@projectlabel{#1}\gdef\star@projecturl{#2}}
\newcommand{\stargithub}[2][]{\stargithubtrue
  \gdef\star@githublabel{#1}\gdef\star@githuburl{#2}}
\newcommand{\stardataset}[2][]{\stardatasettrue
  \gdef\star@datasetlabel{#1}\gdef\star@dataseturl{#2}}
\newcommand{\starhideresources}{\starprojectfalse\stargithubfalse\stardatasetfalse}
% Small native vector icons avoid an external icon font dependency.
\newcommand{\star@resourceicon}[1]{%
  \tikz[x=1pt,y=1pt,baseline=2pt,draw=STARPrimary,line width=.45pt,
    line cap=round,line join=round]{%
    \useasboundingbox (0,0) rectangle (9,9);
    \ifcase#1
      \draw (4.5,4.5) circle (4);
      \draw (4.5,4.5) ellipse (1.7 and 4);
      \draw (.5,4.5)--(8.5,4.5);
    \or
      \draw (3,1.5)--(.5,4.5)--(3,7.5);
      \draw (6,1.5)--(8.5,4.5)--(6,7.5);
      \draw (4,1)--(5,8);
    \or
      \draw (4.5,7) ellipse (3.7 and 1.4);
      \draw (.8,7)--(.8,1.7) arc (180:360:3.7 and 1.4)--(8.2,7);
      \draw (.8,4.4) arc (180:360:3.7 and 1.4);
    \fi}}
\newcommand{\star@resourcelink}[3]{%
  \ifdefempty{#1}{{\color{STARMuted}\itshape #3}}{%
    \ifdefempty{#2}{\href{#1}{\expandafter\nolinkurl\expandafter{#1}}}%
      {\href{#1}{#2}}}}
\newcommand{\star@resourcerow}[5]{%
  \noindent\star@resourceicon{#1}\hspace{4pt}\textbf{#2:}\hspace{4pt}%
  \star@resourcelink{#3}{#4}{#5}\par}
\newcommand{\starresources}{\ifstaranonymous\else
  \ifboolexpr{bool {starproject} or bool {stargithub} or bool {stardataset}}{%
    \par\vspace{6pt}\noindent\begin{minipage}{\linewidth}\centering
    \sffamily\fontsize{10}{13.5}\selectfont\color{STARPrimary}
      \ifstarproject
        \star@resourcerow{0}{Project page}{\star@projecturl}{\star@projectlabel}{[project-page-url]}%
      \fi
      \ifstargithub
        \star@resourcerow{1}{GitHub}{\star@githuburl}{\star@githublabel}{[github-repository-url]}%
      \fi
      \ifstardataset
        \star@resourcerow{2}{Dataset}{\star@dataseturl}{\star@datasetlabel}{[dataset-url]}%
      \fi
    \end{minipage}\par
  }{}\fi}
% Third masthead slot: a placeholder until a collaborator's artwork is supplied.
\newif\ifstarpartner
\starpartnertrue
\newcommand{\star@partnername}{Partner Institution}
\newcommand{\star@partnerlogo}{}
\newcommand{\star@partnermono}{}
\newcommand{\starpartner}[3][]{\starpartnertrue
  \gdef\star@partnermono{#1}\gdef\star@partnername{#2}\gdef\star@partnerlogo{#3}}
\newcommand{\starhidepartner}{\starpartnerfalse}
% A typographic university name coordinates with the STAR lettering by default.
% The original official logo remains available through \stargmulogo.
\newcommand{\star@universitylogo}{}
\newcommand{\star@universitymono}{}
\newcommand{\stargmulogo}[2][]{\gdef\star@universitymono{#1}\gdef\star@universitylogo{#2}}
\newcommand{\stargmutext}{\gdef\star@universitylogo{}\gdef\star@universitymono{}}
\newcommand{\staracknowledgments}[1]{\ifstaranonymous\else
  \section*{Acknowledgments}#1\fi}
\newcommand{\starlogo}[1][32pt]{%
  \ifstaranonymous\else
    \ifstarmonochrome
      \includegraphics[height=#1]{assets/star-mark-mono.pdf}%
    \else
      \includegraphics[height=#1]{assets/star-mark.pdf}%
    \fi
  \fi}
\newcommand{\starwordmark}{%
  \ifstaranonymous\else
      \ifstarmonochrome
        \includegraphics[height=64pt,width=\linewidth,keepaspectratio]{assets/star-lockup-mono.pdf}%
      \else
        \includegraphics[height=64pt,width=\linewidth,keepaspectratio]{assets/star-lockup.pdf}%
      \fi
  \fi}
\newcommand{\star@externalgraphic}[3]{%
  \ifstarmonochrome
    \ifdefempty{#2}{\includegraphics[height=#3,width=\linewidth,keepaspectratio]{#1}}%
      {\includegraphics[height=#3,width=\linewidth,keepaspectratio]{#2}}%
  \else\includegraphics[height=#3,width=\linewidth,keepaspectratio]{#1}\fi}
\newcommand{\stargmumark}{\ifstaranonymous\else
  \ifdefempty{\star@universitylogo}{%
    {\sffamily\bfseries\fontsize{11}{12.5}\selectfont\color{STARInk}%
      \shortstack[l]{GEORGE MASON\\UNIVERSITY}}%
  }{\star@externalgraphic{\star@universitylogo}{\star@universitymono}{40pt}}\fi}
\newcommand{\starpartnermark}{\ifstaranonymous\else\ifstarpartner
  \ifdefempty{\star@partnerlogo}{%
    \begin{tikzpicture}
      \node[draw=STARLine,dashed,rounded corners=2pt,inner sep=4pt,
        text width=\dimexpr\linewidth-10pt\relax,minimum height=30pt,align=center]
        {{\sffamily\fontsize{7}{9}\selectfont\color{STARMuted}\star@partnername}\\[-1pt]
         {\sffamily\fontsize{5.5}{7}\selectfont\color{STARMuted}LOGO PLACEHOLDER}};
    \end{tikzpicture}%
  }{\star@externalgraphic{\star@partnerlogo}{\star@partnermono}{30pt}}%
  \fi\fi}
\newcommand{\star@brandrow}{%
  \noindent\begin{minipage}[c]{.47\textwidth}\starwordmark\end{minipage}%
  \hfill{\color{STARLine}\raisebox{-22pt}{\rule{.4pt}{48pt}}}\hfill
  \begin{minipage}[c]{.25\textwidth}\centering\stargmumark\end{minipage}%
  \ifstarpartner
    \hfill{\color{STARLine}\raisebox{-22pt}{\rule{.4pt}{48pt}}}\hfill
    \begin{minipage}[c]{.22\textwidth}\centering\starpartnermark\end{minipage}%
  \fi\par}

\setlength{\parindent}{1em}
\setlength{\parskip}{0pt}
\setlength{\emergencystretch}{1em}
\linespread{1.035}
\raggedbottom
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\setlist{nosep,leftmargin=1.4em,topsep=4pt}
\setlist[itemize]{label=\textcolor{STARForest}{\small\textbullet}}
\setlength{\textfloatsep}{12pt plus 3pt minus 2pt}
\setlength{\floatsep}{10pt plus 2pt minus 2pt}
\setlength{\intextsep}{10pt plus 2pt minus 2pt}
\renewcommand{\topfraction}{0.92}
\renewcommand{\bottomfraction}{0.85}
\renewcommand{\textfraction}{0.08}
\renewcommand{\floatpagefraction}{0.75}
\setcounter{topnumber}{3}
\setcounter{bottomnumber}{2}
\setcounter{totalnumber}{5}
\captionsetup{font=small,labelfont={bf,sf,color=STARForest},
  labelsep=period,skip=6pt,singlelinecheck=false}
\captionsetup[table]{position=top}
\titleformat{\section}{\sffamily\bfseries\large\color{STARForest}}
  {\thesection}{0.65em}{}
\titleformat{\subsection}{\sffamily\bfseries\normalsize\color{STARInk}}
  {\thesubsection}{0.6em}{}
\titleformat{\subsubsection}{\sffamily\bfseries\normalsize}
  {\thesubsubsection}{0.6em}{}
\titleformat{\paragraph}[runin]{\bfseries}{\theparagraph}{0.5em}{}[.]
\titlespacing*{\section}{0pt}{2.2ex plus 0.5ex minus 0.3ex}{0.8ex}
\titlespacing*{\subsection}{0pt}{1.7ex plus 0.3ex}{0.6ex}
\titlespacing*{\subsubsection}{0pt}{1.4ex plus 0.2ex}{0.5ex}
\titlespacing*{\paragraph}{0pt}{1ex}{0.7em}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\theoremstyle{definition}
\newtheorem{definition}{Definition}[section]
\newtheorem{assumption}{Assumption}[section]
\theoremstyle{remark}
\newtheorem{remark}{Remark}[section]
\def\sectionautorefname{Section}
\def\subsectionautorefname{Section}
\def\subsubsectionautorefname{Section}
\def\equationautorefname{Equation}
\def\figureautorefname{Figure}
\def\tableautorefname{Table}
\def\algorithmautorefname{Algorithm}
\def\assumptionautorefname{Assumption}
\def\lstlistingautorefname{Listing}
\floatname{algorithm}{Algorithm}
\algrenewcommand\algorithmiccomment[1]{\hfill{\color{STARMuted}\(\triangleright\) #1}}
\lstdefinestyle{star}{basicstyle=\ttfamily\footnotesize,
  keywordstyle=\bfseries\color{STARForest},
  commentstyle=\itshape\color{STARMuted},
  stringstyle=\color{STARForest},
  backgroundcolor=\color{STARLight},
  frame=single,rulecolor=\color{STARLine},framerule=0.4pt,
  framesep=5pt,xleftmargin=6pt,xrightmargin=6pt,
  breaklines=true,columns=fullflexible,keepspaces=true,
  showstringspaces=false,tabsize=2,captionpos=b}
\lstset{style=star}
% A self-contained Python lexer keeps the sample independent of lstlang*.sty.
\lstdefinelanguage{STARPython}{
  morekeywords={and,as,assert,async,await,break,class,continue,def,del,elif,
    else,except,False,finally,for,from,global,if,import,in,is,lambda,None,
    nonlocal,not,or,pass,raise,return,True,try,while,with,yield},
  sensitive=true,morecomment=[l]{\#},morestring=[b]",morestring=[b]'}
\newcommand{\starcallout}[2]{%
  \par\addvspace{8pt}\begingroup
  \setlength{\fboxsep}{8pt}\noindent
  \colorbox{STARLight}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%
    {\sffamily\bfseries\small\color{STARForest}#1\par}\smallskip
    \small #2}}\par\endgroup\addvspace{8pt}}

% Short, quiet running furniture. Page one has only the footer.
\newcommand{\star@footerleft}{%
  \ifstaranonymous
    ANONYMOUS MANUSCRIPT\ifdefempty{\star@paperid}{}{\ / \star@paperid}
  \else
    STAR LAB\ / \star@status
  \fi}
\newcommand{\star@headerleft}{%
  \ifstaranonymous RESEARCH MANUSCRIPT\else STAR LAB\fi}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\sffamily\fontsize{7.3}{9}\selectfont\color{STARMuted}\star@headerleft}
\fancyhead[R]{\sffamily\fontsize{7.3}{9}\selectfont\color{STARMuted}\star@shorttitle}
\fancyfoot[L]{\sffamily\fontsize{7}{9}\selectfont\color{STARMuted}\star@footerleft}
\fancyfoot[R]{\sffamily\small\color{STARForest}\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{STARLine}\leaders\hrule height\headrulewidth\hfill}}
\renewcommand{\footrulewidth}{0pt}
\fancypagestyle{starfirst}{\fancyhf{}
  \fancyfoot[L]{\sffamily\fontsize{7}{9}\selectfont\color{STARMuted}\star@footerleft}
  \fancyfoot[R]{\sffamily\small\color{STARForest}\thepage}
  \renewcommand{\headrulewidth}{0pt}}
\fancypagestyle{plain}{\fancyhf{}
  \fancyfoot[L]{\sffamily\fontsize{7}{9}\selectfont\color{STARMuted}\star@footerleft}
  \fancyfoot[R]{\sffamily\small\color{STARForest}\thepage}
  \renewcommand{\headrulewidth}{0pt}}

\newcommand{\star@titleblock}{%
  \begingroup\setlength{\parindent}{0pt}
  \ifstaranonymous
    {\sffamily\small\color{STARMuted}ANONYMOUS RESEARCH MANUSCRIPT
      \ifdefempty{\star@paperid}{}{\hfill PAPER \star@paperid}\par}
  \else
    \star@brandrow\vspace{4pt}
    {\sffamily\fontsize{6.5}{8}\selectfont\color{STARMuted}%
      \MakeUppercase{\starlabname}\hfill\star@status
      \ifdefempty{\star@version}{}{\ / \star@version}\par}
  \fi
  \vspace{6pt}
  {\color{STARForest}\hrule height 1.1pt}\vspace{2pt}
  {\color{STARGold}\hrule width 36pt height 2pt}\vspace{10pt}
  {\raggedright\bfseries\color{STARInk}%
    \ifstartwocolumn\fontsize{23}{26}\else\fontsize{25}{29}\fi
    \selectfont\@title\par}
  \vspace{8pt}
  \ifstaranonymous
    {\sffamily\normalsize Anonymous authors\par}
    \vspace{3pt}{\small Author information withheld for review\par}
  \else
    {\sffamily\bfseries\normalsize\@author\par}
    \vspace{4pt}{\small\star@affiliation\par}
    \ifdefempty{\star@emails}{}{%
      \vspace{2pt}{\ttfamily\footnotesize\star@emails\par}
    }
  \fi
  \vspace{10pt}
  \endgroup}
\renewcommand{\maketitle}{%
  \ifstaranonymous
    \hypersetup{pdftitle={\@title},pdfauthor={Anonymous authors},
      pdfsubject={},pdfkeywords={}}
  \else
    \hypersetup{pdftitle={\@title},pdfauthor={\@author},
      pdfsubject={STAR Lab: \starlabname; \star@track},pdfkeywords={\star@keywords}}
  \fi
  \ifstartwocolumn\twocolumn[\star@titleblock]\else\star@titleblock\fi
  \thispagestyle{starfirst}}
\renewenvironment{abstract}{%
  \par\begingroup\setlength{\parindent}{0pt}
  {\sffamily\bfseries\small\color{STARForest}ABSTRACT\par}\vspace{4pt}
  \small\ignorespaces
}{%
  \par\starresources\ifdefempty{\star@keywords}{}{%
    \vspace{6pt}{\sffamily\fontsize{8}{10}\selectfont
      \textbf{Keywords}\quad\star@keywords\par}
  }\endgroup\vspace{8pt}}
\newcommand{\starbibliography}[1]{\bibliographystyle{unsrtnat}\bibliography{#1}}
\setlength{\bibsep}{4pt}
\renewcommand{\bibfont}{\small}
\endinput
