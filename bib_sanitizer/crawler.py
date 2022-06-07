import urllib.parse

from tqdm import tqdm
from pybtex.database import parse_string

import requests as requests

DBLP_PUBLICATION_URL = 'https://dblp.org/search/publ/api?q={urlpt}&h=100&format=bib1&rd=1a'
BIBTEX_FORMAT = 'bibtex'

TITLE_FIELD = 'title'
AUTHOR_FIELD = 'author'
JOURNAL_FIELD = 'journal'
LATEX_CMD_REGEX = '(\\\w+)?\{'


class DBLPReplacer:

    @staticmethod
    def _normalize_bib_field(bibstr):
        """
        Removes any latex commands and curly brackets from a bib field
        :param bibstr:
        :type bibstr:
        :return:
        :rtype:
        """
        bibstr = bibstr.replace('}', '')
        bibstr = bibstr.replace('{', '')
        bibstr = bibstr.lower()

        return bibstr

    @staticmethod
    def publication_key(bibentry):
        """
        Generates normalized string representation of a bibentry
        :param bibentry:
        :type bibentry:
        :return:
        :rtype:
        """
        st = []

        # add title and first author
        if TITLE_FIELD in bibentry.fields:
            st.append(DBLPReplacer._normalize_bib_field(bibentry.fields[TITLE_FIELD]))

        authors_included = 0
        if AUTHOR_FIELD in bibentry.persons and len(bibentry.persons[AUTHOR_FIELD]) > 0:
            first_author = bibentry.persons[AUTHOR_FIELD][0]
            st.append(DBLPReplacer._normalize_bib_field(first_author.last_names[-1]))
            authors_included += 1

        st = ' '.join(st)

        # remove special characters
        st = ''.join(e for e in st if e.isalnum() or e == ' ' or e == '-')

        # remove double -
        st = st.replace('--', '-')

        return st

    def find_match(self, key, bibentry):
        """
        Searches on DBLP and tries to find a cleaner version of the current bibtex entry. If available, it will replace
        it.

        :param key: key in the bibtex
        :param bibentry: old bib entry
        :type bibentry:
        :return: old bib entry if no replacement was found or DBLP entry
        :rtype:
        """
        pub_key = DBLPReplacer.publication_key(bibentry)
        pub_url_param = urllib.parse.quote(pub_key)
        dblp_entries = requests.get(DBLP_PUBLICATION_URL.format(urlpt=pub_url_param)).text
        dblp_bib_entries = parse_string(dblp_entries, BIBTEX_FORMAT)

        return_entry = None

        # find best match
        for dblp_entry in dblp_bib_entries.entries.values():
            dblp_pub_key = DBLPReplacer.publication_key(dblp_entry)
            if dblp_pub_key != pub_key:
                continue

            # prefer publications in conferences instead of arxiv preprints
            if return_entry is None or \
                    (JOURNAL_FIELD in return_entry.fields and return_entry.fields[JOURNAL_FIELD] == 'CoRR'):
                return_entry = dblp_entry

        if return_entry is None:
            print(f"Warning: No DBLP match for {key}")
            return_entry = bibentry

        return return_entry

    def replace_refs(self, bib_data):
        """
        Replaces references in a bib file by DBLP references
        :param bib_data: original bib data
        :type bib_data: BibliographyData
        :return: cleaned bib data
        :rtype: BibliographyData
        """

        for key, bibentry in tqdm(bib_data.entries.items()):
            bib_data.entries[key] = self.find_match(key, bibentry)

        return bib_data
