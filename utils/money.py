import re


class Money:

    @staticmethod
    def parse(value: str | None) -> float | None:

        if value is None:
            return None

        value = value.replace("R$", "")
        value = value.replace("\n", "")
        value = value.replace(" ", "")
        value = value.replace(".", "")
        value = value.replace(",", ".")

        match = re.search(r"\d+(\.\d+)?", value)

        if not match:
            return None

        return float(match.group())