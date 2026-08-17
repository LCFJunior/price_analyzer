import re
import unicodedata


class ClassifierTextUtils:
    @staticmethod
    def normalize(
        value: str,
    ) -> str:
        value = value.lower().strip()

        normalized = unicodedata.normalize(
            "NFKD",
            value,
        )

        normalized = "".join(
            character
            for character in normalized
            if not unicodedata.combining(
                character
            )
        )

        normalized = re.sub(
            r"[^a-z0-9]+",
            " ",
            normalized,
        )

        return " ".join(
            normalized.split()
        )

    @staticmethod
    def slug(
        value: str,
    ) -> str:
        normalized = (
            ClassifierTextUtils.normalize(
                value
            )
        )

        return normalized.replace(
            " ",
            "_",
        )

    @staticmethod
    def contains_term(
        text: str,
        term: str,
    ) -> bool:
        normalized_text = (
            ClassifierTextUtils.normalize(
                text
            )
        )

        normalized_term = (
            ClassifierTextUtils.normalize(
                term
            )
        )

        return bool(
            re.search(
                rf"\b{re.escape(normalized_term)}\b",
                normalized_text,
            )
        )