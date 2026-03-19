import os
import glob
import re

draft_dir = "1-drafts"
output_file = "paper_body.tex"

# Custom sort to ensure we process in correct order
files = sorted(glob.glob(os.path.join(draft_dir, "section*.md")))

print("Assembling the following files:")
for f in files:
    print(f" - {f}")

full_text = ""
for f in files:
    with open(f, 'r') as file:
        full_text += file.read() + "\n\n"

# We must convert the figures markdown to simple latex includes since pandoc 
# inside the sandbox might be tricky to format perfectly for arXiv.
# Actually, it is easier to just run pandoc on the concatenated file:

with open("temp_full.md", 'w') as temp:
    temp.write(full_text)

os.system("pandoc temp_full.md --natbib -o temp_body.tex")

with open("temp_body.tex", 'r') as tb:
    tex_content = tb.read()

# Replace .svg with .pdf in the \includegraphics commands
tex_content = tex_content.replace(".svg}", ".pdf}")
tex_content = tex_content.replace("figures/", "figures/") # ensure path is right

# Standardize section headers for proper latex formatting
# (Pandoc usually handles headers correctly)

with open(output_file, 'w') as out:
    out.write(tex_content)

print(f"Successfully assembled {output_file}")

# Write the main.tex preamble
main_tex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{geometry}
\usepackage{natbib}
\geometry{a4paper, margin=1in}

\title{Intent of Thought (IoT): A Governance Lifecycle for LLM Reasoning Topology Selection}
\author{
  Naveen Riaz Mohamed Kani \\
  SYNTHAI \\
  \texttt{naveen@synthai.org}
}

\date{\today}

\begin{document}

\maketitle

\input{paper_body.tex}

\bibliographystyle{plainnat}
\bibliography{references}

\end{document}
"""

with open("main.tex", 'w') as m:
    m.write(main_tex)
print("Successfully generated main.tex")

# Cleanup
if os.path.exists("temp_full.md"):
    os.remove("temp_full.md")
if os.path.exists("temp_body.tex"):
    os.remove("temp_body.tex")

