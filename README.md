# bib-sanitizer

Convert bibtex entries of latex documents to DBLP references.

Bibtex entries for references in latex documents often stem from various different sources (scholar, conference
websites, ...) and are of varying quality and slightly inconsistent (e.g., inconsistent conference names etc.). In
contrast, DBLP references are often very consistent and of high quality. Hence, this script looks up existing bibtex
entries in DBLP and replaces those in the .bib file. Afterwards, the resulting .bib file can be used as a drop-in
replacement for the old one.

## Replace references with cleaner bibtex references

Simply run the `dblp_replace.py` script.

```
python3 dblp_replace.py 
    --original_bibtex path_to/original.bib
    --target_bibtex path_to/clean_bib.bib
```

## Optional: Integrate into document with existing bibtex files

Sometimes we might want to integrate a latex file (with clean bibtex entries) into another file (also with clean bibtex
entries), e.g., the latex file could be a publication that we want to include in a cumulative dissertation with
consistent references.

The workflow in this example is as follows:

1. We run the `dblp_replace.py` script on the latex file to obtain the `clean_bib.bib` file
2. We integrate the new references (i.e., the delta of new publications) in the .bib file of the target
   document (`target.bib`). To do this, we might use tools like Jabref, which you might anyway use for the larger
   document. Of course, the bibtex keys can change during this process. This is fixed by the next step.
3. Now we run the `integrate.py` script to adapt the citation keys of the smaller document to be consistent with the
   larger one.
4. The smaller document can now be included in the larger one.

```
python3 integrate.py 
    --original_bibtex path_to/clean_bib.bib
    --original_latex path_to/original.tex
    --target_bibtex path_to/target.bib
    --target_latex path_to/target.tex
```

## Dev setup

Clone

```
git clone git@github.com:bhilprecht/bib-sanitizer.git
```

Install requirements

```
python3 -m venv venv 
source venv/bin/activate
pip3 install --upgrade setuptools
pip3 install --upgrade pip
pip3 install -e .
```
