

def validate_name(name: str | None) -> str | None:
    if name is None:
        return name



    if not all(sign.isalpha() for sign in name):
        raise ValueError(
            "Поле может содержать только буквы"
        )

    return name


def validate_phone(phone: str | None) -> str | None:
    if phone is None:
        return phone

    if not all(sign in '01234567689' for sign in phone):
        raise ValueError(
            "Телефон должен содержать только цифры"
        )
    return phone