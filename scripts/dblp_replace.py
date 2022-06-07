import argparse

from pybtex.database import parse_file

from bib_sanitizer.crawler import DBLPReplacer, BIBTEX_FORMAT

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--original_bibtex')
    parser.add_argument('--target_bibtex')

    args = parser.parse_args()

    # parse the original bibtex file
    bib_db = parse_file(args.original_bibtex)

    # crawl DBLP for potential matches
    crawler = DBLPReplacer()
    bib_db = crawler.replace_refs(bib_db)

    # save new bib file
    bib_db.to_file(args.target_bibtex, BIBTEX_FORMAT)
