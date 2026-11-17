# validators.py - მომხმარებლის შეყვანის შემოწმება
# თითო მეთოდი მანამ ეკითხება მომხმარებელს, სანამ სწორ მნიშვნელობას არ შეიყვანს
from book import Book


# InputValidator - შეყვანის შემოწმების მეთოდები ერთ კლასში
# ყველა მეთოდი @staticmethod-ია: ობიექტი არ სჭირდება, კლასზე იძახება:
# InputValidator.input_text("სათაური: ")
class InputValidator:
    # input_text - ითხოვს ტექსტს; ცარიელს არ იღებს
    @staticmethod
    def input_text(prompt):
        while True:
            # strip - შლის ზედმეტ ჰარებს თავში და ბოლოში ("   " ცარიელად ჩაითვლება)
            text = input(prompt).strip()
            if text:
                return text
            print("ველი ცარიელი არ შეიძლება იყოს")

    # input_positive_int - ითხოვს მთელ რიცხვს, რომელიც 0-ზე მეტია
    @staticmethod
    def input_positive_int(prompt):
        while True:
            value = input(prompt).strip()
            # int("abc") აგდებს ValueError-ს - ვიჭერთ, რომ პროგრამა არ გაითიშოს
            try:
                number = int(value)
            except ValueError:
                print("შეიყვანე მთელი რიცხვი")
                # continue - ციკლის თავში ბრუნდება და თავიდან ეკითხება
                continue
            if number > 0:
                return number
            print("რიცხვი 0-ზე მეტი უნდა იყოს")

    # input_year - ითხოვს გამოცემის წელს
    # ჯერ input_positive_int ამოწმებს რომ რიცხვია, მერე Book.validate_year - რომ მიმდინარე წელზე მეტი არ არის
    @staticmethod
    def input_year(prompt):
        while True:
            year = InputValidator.input_positive_int(prompt)
            try:
                Book.validate_year(year)
                return year
            # e - შეცდომა, რომელიც validate_year-მა ააგდო; print(e) მის ტექსტს გამოიტანს
            except ValueError as e:
                print(e)

    # input_choice - ითხოვს მნიშვნელობას მხოლოდ დაშვებული ვარიანტებიდან (მაგ. "1" ან "2")
    @staticmethod
    def input_choice(prompt, options):
        while True:
            choice = input(prompt).strip()
            if choice in options:
                return choice
            print(f"აირჩიე ერთ-ერთი: {', '.join(options)}")
