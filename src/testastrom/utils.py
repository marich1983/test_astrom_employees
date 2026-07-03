from datetime import date

def age_calculate(birthday: date) -> int:
    return int((date.today() - birthday).days/365)

def birthday_calculate(age: int) -> date:
    today = date.today()
    return date(today.year - age, today.month, today.day)

if __name__ == '__main__':
    print(age_calculate(date(1983, 8, 24)))
    print(birthday_calculate(43))


