from datetime import datetime

class Note:
    @staticmethod
    def parse_tags(tags: str, separator=","):
        return [t.strip().lower() for t in tags.split(separator)]

    def __init__(self, note = "", tags=""):
        self.note = note
        self._tags = []
        self.tags = tags
        self.date_added = datetime.now()
        self.date_modified = datetime.now()

    @property
    def tags(self):
        return self._tags
    @tags.setter
    def tags(self, value: str):
        if value is None or value == "":
            tags = []
        else:
            self._tags = Note.parse_tags(value)

    def has(self, terms: str):
        parsed_terms = Note.parse_tags(terms, " ")
        return any(term in self.note.lower() for term in parsed_terms) or any(term in self.tags for term in parsed_terms)