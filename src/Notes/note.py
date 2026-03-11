from datetime import datetime

class Note:
    id = 0

    @staticmethod
    def parse_tags(tags: str, separator=","):
        return [t.strip().lower() for t in tags.split(separator)]

    def __init__(self, note = "", tags=""):
        Note.id += 1
        self.id = Note.id
        self._note = ""
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
            self._tags = []
        else:
            self._tags = Note.parse_tags(value)
        self.date_modified = datetime.now()

    def get_tags(self):
        return ", ".join(self._tags)

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, note: str):
        self._note = note
        self.date_modified = datetime.now()

    def has(self, terms: str):
        parsed_terms = Note.parse_tags(terms, " ")
        return any(term in self.note.lower() for term in parsed_terms) or any(term in self.tags for term in parsed_terms)