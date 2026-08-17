class Text:

    @staticmethod
    def clean(text: str | None) -> str | None:

        if text is None:
            return None

        text = text.replace("\n", " ")

        text = text.replace("\t", " ")

        while "  " in text:
            text = text.replace("  ", " ")

        return text.strip()