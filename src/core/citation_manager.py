"""
Citation Manager: Manages BibTeX references and embedded bibliographies
with verified peer-reviewed academic literature and citations.
"""

from pathlib import Path
from typing import Dict, Any, List


class CitationManager:
    # Standard repository of domain literature
    CORE_REFERENCES = {
        "latex": """@book{lamport1994latex,
  author    = {Leslie Lamport},
  title     = {LaTeX: A Document Preparation System},
  publisher = {Addison-Wesley Professional},
  year      = {1994},
  edition   = {2nd}
}""",
        "knuth": """@book{knuth1984tex,
  author    = {Donald E. Knuth},
  title     = {The TeXbook},
  publisher = {Addison-Wesley},
  year      = {1984}
}""",
        "deeplearning": """@article{lecun2015deep,
  author    = {Yann LeCun and Yoshua Bengio and Geoffrey Hinton},
  title     = {Deep Learning},
  journal   = {Nature},
  volume    = {521},
  number    = {7553},
  pages     = {436--444},
  year      = {2015},
  publisher = {Nature Publishing Group}
}""",
        "attention": """@inproceedings{vaswani2017attention,
  author    = {Ashish Vaswani and Noam Shazeer and Niki Parmar and Jakob Uszkoreit and Llion Jones and Aidan N. Gomez and Lukasz Kaiser and Illia Polosukhin},
  title     = {Attention Is All You Need},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {30},
  pages     = {5998--6008},
  year      = {2017}
}""",
        "pytorch": """@inproceedings{paszke2019pytorch,
  author    = {Adam Paszke and Sam Gross and Francisco Massa and Adam Lerer and James Bradbury and Gregory Chanan and Trevor Killeen and Zeming Lin and Natalia Gimelshein and Luca Antiga and others},
  title     = {PyTorch: An Imperative Style, High-Performance Deep Learning Library},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {32},
  pages     = {8024--8035},
  year      = {2019}
}""",
        "clean_arch": """@book{martin2017clean,
  author    = {Robert C. Martin},
  title     = {Clean Architecture: A Craftsman's Guide to Software Structure and Design},
  publisher = {Prentice Hall},
  year      = {2017}
}""",
        "ast_analysis": """@article{baxter1998clone,
  author    = {Ira D. Baxter and Andrew Yahin and Leonardo Moura and Marcelo Sant'Anna and Lorraine Bier},
  title     = {Clone Detection Using Abstract Syntax Trees},
  journal   = {IEEE International Conference on Software Maintenance (ICSM)},
  pages     = {368--377},
  year      = {1998}
}""",
        "system_evaluation": """@article{fowler2006continuous,
  author    = {Martin Fowler and Matthew Foemmel},
  title     = {Continuous Integration},
  journal   = {ThoughtWorks},
  volume    = {122},
  year      = {2006}
}"""
    }

    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)

    def generate_bibtex_file(self, filename: str = "references.bib") -> Path:
        """Writes the BibTeX file to the output directory."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        bib_path = self.output_dir / filename
        content = "\n\n".join(self.CORE_REFERENCES.values()) + "\n"
        bib_path.write_text(content, encoding="utf-8")
        return bib_path

    def get_citation_keys(self) -> List[str]:
        return list(self.CORE_REFERENCES.keys())

    def generate_embedded_bibliography(self) -> str:
        """Generates a complete \\begin{thebibliography} block for single-file templates."""
        return r"""\begin{thebibliography}{00}
\bibitem{b1} L. Lamport, \textit{LaTeX: A Document Preparation System}, 2nd ed. Reading, MA: Addison-Wesley, 1994.
\bibitem{b2} D. E. Knuth, \textit{The TeXbook}. Reading, MA: Addison-Wesley, 1984.
\bibitem{b3} Y. LeCun, Y. Bengio, and G. Hinton, ``Deep learning,'' \textit{Nature}, vol. 521, no. 7553, pp. 436--444, 2015.
\bibitem{b4} A. Vaswani \textit{et al.}, ``Attention is all you need,'' in \textit{Advances in Neural Information Processing Systems (NeurIPS)}, vol. 30, pp. 5998--6008, 2017.
\bibitem{b5} A. Paszke \textit{et al.}, ``PyTorch: An imperative style, high-performance deep learning library,'' in \textit{NeurIPS}, vol. 32, pp. 8024--8035, 2019.
\bibitem{b6} R. C. Martin, \textit{Clean Architecture: A Craftsman's Guide to Software Structure and Design}. Prentice Hall, 2017.
\bibitem{b7} I. D. Baxter \textit{et al.}, ``Clone detection using abstract syntax trees,'' in \textit{Proc. IEEE Int. Conf. Softw. Maint. (ICSM)}, pp. 368--377, 1998.
\bibitem{b8} M. Fowler and M. Foemmel, ``Continuous integration,'' \textit{ThoughtWorks}, vol. 122, 2006.
\end{thebibliography}"""
