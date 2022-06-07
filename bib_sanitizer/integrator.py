from bib_sanitizer.crawler import DBLPReplacer


class Integrator:

    def __init__(self, target_bib):
        self.target_bib = target_bib

        self.entry_dict = dict()
        for bibkey, entry in self.target_bib.entries.items():
            pub_key = DBLPReplacer.publication_key(entry)
            self.entry_dict[pub_key] = bibkey

    def match(self, bibentry):
        """
        Attempts to find the corresponding bibtex entry in the target_bib for a bibentry
        :param bibentry:
        :type bibentry:
        :return:
        :rtype:
        """

        pub_key = DBLPReplacer.publication_key(bibentry)
        return self.entry_dict.get(pub_key)

    def match_all(self, original_bibtex):
        """
        Repeats the matching for each bibentry in the original bibtex file
        :param original_bibtex:
        :type original_bibtex:
        :return:
        :rtype:
        """
        replacement = dict()
        for original_key, entry in original_bibtex.entries.items():
            target_key = self.match(entry)
            if target_key is None:
                print(f"No match found for bibtex key {original_key}")
            replacement[original_key] = target_key
        return replacement
