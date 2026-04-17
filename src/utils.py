from anki.utils import strip_html

class FieldUtil:
    EXPRESSION_FIELDS = ["Expressions", "Expression"]
    READING_FIELDS = ["Kana Reading", "Kana", "Reading"]

    @classmethod
    def get_clean_field(cls, note, field_names):
        for fld in field_names:
            if fld in note:
                return strip_html(note[fld]).strip()
        return None

    @classmethod
    def get_word(cls, note):
        return cls.get_clean_field(note, cls.EXPRESSION_FIELDS)

    @classmethod
    def get_reading(cls, note):
        return cls.get_clean_field(note, cls.READING_FIELDS)