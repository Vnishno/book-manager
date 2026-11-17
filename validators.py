# validators.py - მომხმარებლის შეყვანის შემოწმება (ცარიელი ტექსტი, რიცხვი, წელი)
from book import Book

# input_text - ტექსტს ითხოვს მანამ, სანამ ცარიელი არ იქნება
def input_text(prompt):
    while True:
        # strip - შლის ზედმეტ ჰარებს თავში და ბოლოში
        text = input(prompt).strip()
        if text:
            return text
        print("ველი ცარიელი არ შეიძლება იყოს")


# input_positive_int - დადებით მთელ რიცხვს ითხოვს მანამ, სანამ სწორს არ შეიყვანენ
def input_positive_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("შეიყვანე მთელი რიცხვი")
            continue
        if number > 0:
            return number
        print("რიცხვი 0-ზე მეტი უნდა იყოს")

# input_year - წელს ითხოვს მანამ, სანამ Book.validate_year არ დაადასტურებს
def input_year(prompt):
    while True:
        year = input_positive_int(prompt)
        try:
            Book.validate_year(year)
            return year
        except ValueError as e:
            print(e)
