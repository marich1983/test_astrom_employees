import enum


class Gender(str, enum.Enum):
    male = "male"
    female = "female"

    def label(self):
        return {
            "male": "мужской",
            "female": "женский"
        }[self.value]