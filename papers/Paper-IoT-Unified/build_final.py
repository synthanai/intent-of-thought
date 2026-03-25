#!/usr/bin/env python3
"""Build polished PDF v11: Force word-wrap in table headers."""
import os, re, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(BASE, "1-drafts")

sections = [
    "section0_abstract.md",
    "section1_introduction.md",
    "section2_background.md",
    "section3_framework.md",
    "section4_lifecycle.md",
    "section5_experiments.md",
    "section6_case_study_spar.md",
    "section7_discussion.md",
    "section8_conclusion.md",
    "section9_references.md",
    "section10_appendix.md",
]

abstract_text = ""
body_md = ""

for s in sections:
    path = os.path.join(DRAFTS, s)
    with open(path, 'r') as f:
        content = f.read()
    if s == "section0_abstract.md":
        abstract_text = content.replace("# Abstract\n", "").strip()
        abstract_text = abstract_text.replace('%', r'\%')
        # Force paragraph breaks in abstract environment which may suppress parskip
        abstract_text = re.sub(r'\n\s*\n', '\n\n\\\\par\\\\medskip\n\n', abstract_text)
        continue
    content = re.sub(r'^# Section \d+:\s*', '# ', content, flags=re.MULTILINE)
    content = re.sub(r'^(#{2,})\s*\d+\.\d+\s+', r'\1 ', content, flags=re.MULTILINE)
    body_md += content + "\n\n"

with open("/tmp/iot_body.md", 'w') as f:
    f.write(body_md)

# Use DEFAULT columns so pandoc generates p{} columns with wrapping
subprocess.run([
    "pandoc", "/tmp/iot_body.md",
    "-o", "/tmp/iot_body.tex",
    "--number-sections",
    "--syntax-highlighting=tango",
], check=True)

with open("/tmp/iot_body.tex", 'r') as f:
    body_tex = f.read()

# ===== POST-PROCESSING =====

# 1. Remove minipage wrappers from longtable headers
body_tex = re.sub(
    r'\\begin\{minipage\}\[b\]\{[^}]+\}\\(?:raggedright|centering)\n',
    '',
    body_tex
)
body_tex = body_tex.replace('\\end{minipage}', '')

# 3. Remove LTcaptype blocks
body_tex = re.sub(r'\{\\def\\LTcaptype\{none\}[^\n]*\n', '', body_tex)
body_tex = re.sub(r'(\\end\{longtable\})\n\}', r'\1', body_tex)

# 1b. Make all longtables use small font to prevent column overflow
body_tex = body_tex.replace(
    r'\begin{longtable}',
    r'{\small\begin{longtable}'
)
body_tex = body_tex.replace(
    r'\end{longtable}',
    r'\end{longtable}}'
)

# 2. Removed overly aggressive \newline header wrapping

# 4. Make code blocks smaller
body_tex = body_tex.replace(r'\begin{Shaded}', r'{\small\begin{Shaded}')
body_tex = body_tex.replace(r'\end{Shaded}', r'\end{Shaded}}')

# 5. Keep longtable intact (previous tabular conversion regex was broken)
# Tables render correctly as native longtable environments

# 6. Global Em-Dash Eradication (User Rules Compliance)
body_tex = body_tex.replace('---', ', ')
body_tex = body_tex.replace('—', ', ')
# 7. Indian/UK English Localisation
uk_dict = {
    r'\banalyze\b': 'analyse', r'\bAnalyze\b': 'Analyse',
    r'\banalyzing\b': 'analysing', r'\bAnalyzing\b': 'Analysing',
    r'\boptimize\b': 'optimise', r'\bOptimize\b': 'Optimise',
    r'\boptimization\b': 'optimisation', r'\bOptimization\b': 'Optimisation',
    r'\butilize\b': 'utilise', r'\bUtilize\b': 'Utilise',
    r'\butilization\b': 'utilisation', r'\bUtilization\b': 'Utilisation',
    r'\bgeneralize\b': 'generalise', r'\bGeneralize\b': 'Generalise',
    r'\bgeneralization\b': 'generalisation', r'\bGeneralization\b': 'Generalisation',
    r'\bbehavior\b': 'behaviour', r'\bBehavior\b': 'Behaviour',
    r'\bmodeling\b': 'modelling', r'\bModeling\b': 'Modelling',
    r'\bmodeled\b': 'modelled', r'\bModeled\b': 'Modelled',
    r'\bprioritize\b': 'prioritise', r'\bPrioritize\b': 'Prioritise',
    r'\bcategorize\b': 'categorise', r'\bCategorize\b': 'Categorise',
    r'\brealize\b': 'realise', r'\bRealize\b': 'Realise',
    r'\bidealize\b': 'idealise', r'\bIdealize\b': 'Idealise',
    r'\bformalize\b': 'formalise', r'\bFormalize\b': 'Formalise',
    r'\binternalize\b': 'internalise', r'\bInternalize\b': 'Internalise'
}
for us_word, uk_word in uk_dict.items():
    body_tex = re.sub(us_word, uk_word, body_tex)
    abstract_text = re.sub(us_word, uk_word, abstract_text)

# ===== BUILD MAIN.TEX =====
main_tex = r"""\documentclass[11pt,a4paper]{article}

% Encoding and fonts
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\exhyphenpenalty=50
\tolerance=2000
\emergencystretch=1.5em
\sloppy
\setlength{\parskip}{0.6em}
\setlength{\parindent}{1.5em}

% Page geometry
\usepackage[margin=1.8cm]{geometry}

% URL line breaking
\usepackage[hyphens]{url}

% Links
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue!60!black,
  citecolor=blue!60!black,
  urlcolor=blue!60!black
}

% Math
\usepackage{amsmath,amssymb}

% Tables
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{calc}  % CRITICAL: defines \real{} for pandoc columns
\usepackage{float}
\renewcommand{\arraystretch}{1.3}

% Graphics
\usepackage{graphicx}
\usepackage{xcolor}

% Pandoc compatibility: define \tightlist
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

\title{\textbf{Intent of Thought (IoT): A Governance Lifecycle for LLM Reasoning Topology Selection}}

\author{
  Naveen Riaz Mohamed Kani \\
  Independent Researcher, Melbourne, Australia \\
  ORCID: \href{https://orcid.org/0009-0003-9173-2425}{0009-0003-9173-2425} \\
  \texttt{naveenriaz@synthai.biz}
}

\date{March 2026}

\begin{document}
\maketitle

\begin{abstract}
""" + abstract_text + r"""

\par\medskip\noindent\textbf{Keywords:} Large Language Models, Chain-of-Thought Reasoning, Reasoning Topology, Intent Governance, Failure Modes, Multi-Agent Debate
\end{abstract}

\newpage
\tableofcontents
\newpage

""" + body_tex + r"""

\end{document}
"""

with open("/tmp/iot_final.tex", 'w') as f:
    f.write(main_tex)

# ===== COMPILE =====
env = os.environ.copy()
env["TEXMFVAR"] = "/tmp/texmf-var"
os.makedirs("/tmp/texmf-var", exist_ok=True)

for p in [1, 2]:
    print(f"XeLaTeX pass {p}...")
    r = subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory=/tmp", "/tmp/iot_final.tex"],
        capture_output=True, text=True, env=env
    )
    for line in r.stdout.split('\n'):
        if 'Output written' in line:
            print(f"  {line.strip()}")
    errors = [l for l in r.stdout.split('\n') if l.startswith('!')]
    if errors:
        unique_errors = set(errors)
        print(f"  Errors: {len(unique_errors)} unique")

pdf = "/tmp/iot_final.pdf"
if os.path.exists(pdf):
    os.system('cp /tmp/iot_final.pdf "Intent_of_Thought.pdf"')
    print(f"\n✅ Build successful: Exported to Intent_of_Thought.pdf")
