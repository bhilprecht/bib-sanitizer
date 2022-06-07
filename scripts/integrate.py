import argparse

from pybtex.database import parse_file

from bib_sanitizer.integrator import Integrator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--original_bibtex')
    parser.add_argument('--original_latex')
    parser.add_argument('--target_bibtex')
    parser.add_argument('--target_latex')

    args = parser.parse_args()

    # parse the original bibtex file
    original_bibtex = parse_file(args.original_bibtex)
    target_bibtex = parse_file(args.target_bibtex)

    # match old entry keys with new ones
    integrator = Integrator(target_bibtex)
    replacement = integrator.match_all(original_bibtex)

    # replace in latex file
    with open(args.original_latex) as f:
        latex = f.read()
    for oldkey, newkey in replacement.items():
        # only replace if the citation key appears before comma or closing bracket as in \cite{a,b}
        for sep_char in [',', '}']:
            latex = latex.replace(oldkey + sep_char, newkey + sep_char)

    with open(args.target_latex, 'w') as f:
        f.write(latex)
