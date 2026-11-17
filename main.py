# Book Manager - წიგნების მართვის კონსოლ აპლიკაცია

from datetime import datetime
from abc import ABC, abstractmethod

# ABC - აბსტრაქტული კლასი: ზოგადი შაბლონია, Book(...)-ით პირდაპირ ობიექტი არ იქმნება
class Book(ABC):
    # __init__ - ეშვება ობიექტის შექმნისას და ველებს ავსებს
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    # @property - წელს ვკითხულობთ ისე, თითქოს ჩვეულებრივი ველი იყოს: book.year
    @property
    def year(self):
        return self.__year

    # @year.setter - ეშვება, როცა წელს მნიშვნელობას ვანიჭებთ: book.year = 1937
    @year.setter
    def year(self, value):
        # შემოწმებას validate_year აკეთებს, არასწორ წელზე შეცდომას აგდებს
        Book.validate_year(value)
        self.__year = value

    # @staticmethod - შემოწმებას ობიექტი არ სჭირდება, ამიტომ კლასზე იძახება: Book.validate_year(1990)
    # ერთი წესი ორ ადგილას გამოიყენება: setter-ში და მენიუში
    @staticmethod
    def validate_year(value):
        current_year = datetime.now().year
        if not isinstance(value, int):
            raise TypeError("წელი უნდა იყოს მთელი რიცხვი")
        if value < 1 or value > current_year:
            raise ValueError(f"წელი უნდა იყოს 1-დან {current_year}-მდე")

    # @abstractmethod - ყველა შვილობილმა კლასმა ეს მეთოდი თავისებურად უნდა დაწეროს
    @abstractmethod
    def get_info(self):
        pass

    # __str__ - როგორ გამოჩნდეს წიგნი print()-ის დროს
    def __str__(self):
        # self.get_info() - გაეშვება იმ კლასის ვერსია, რომლის ობიექტიცაა (პოლიმორფიზმი)
        return f"{self.title} - {self.author} ({self.year}) | {self.get_info()}"

# PrintedBook - ნაბეჭდი წიგნი, Book-ისგან იღებს ყველაფერს და უმატებს გვერდების რაოდენობას
class PrintedBook(Book):
    def __init__(self, title, author, year, pages):
        # super().__init__ - მშობლის __init__ ავსებს title, author, year (ვალიდაციითურთ)
        super().__init__(title, author, year)
        self.pages = pages

    # get_info - მშობლის აბსტრაქტული მეთოდის საკუთარი ვერსია (override)
    def get_info(self):
        return f"ნაბეჭდი, {self.pages} გვ."


# EBook - ელექტრონული წიგნი, გვერდების ნაცვლად აქვს ფაილის ფორმატი
class EBook(Book):
    def __init__(self, title, author, year, file_format):
        super().__init__(title, author, year)
        self.file_format = file_format

    def get_info(self):
        return f"ელექტრონული, {self.file_format}"

# BookManager - წიგნების სიის მართვა: დამატება, ნახვა, ძებნა, წაშლა
class BookManager:
    def __init__(self):
        # __books - დამალული სია, გარედან მხოლოდ ამ კლასის მეთოდებით იცვლება
        self.__books = []

    # add_book - ახალი წიგნის დამატება სიაში
    def add_book(self, book):
        self.__books.append(book)

    # get_all_books - სიის ასლს ვაბრუნებთ, რომ გარედან ორიგინალი ვერ შეცვალონ
    def get_all_books(self):
        return self.__books.copy()

    # search_by_title - ძებნა სათაურის ნაწილით, დიდი/პატარა ასოების მიუხედავად
    def search_by_title(self, title):
        results = []
        for book in self.__books:
            if title.lower() in book.title.lower():
                results.append(book)
        return results

    # delete_book - წაშლა ზუსტი სათაურით; აბრუნებს True თუ წაიშალა, False თუ ვერ მოიძებნა
    def delete_book(self, title):
        for book in self.__books:
            if book.title.lower() == title.lower():
                self.__books.remove(book)
                return True
        return False

# ===== შეყვანის ვალიდაცია =====

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

# ===== მენიუს ფუნქციები =====

# მენიუს 1-ლი პუნქტი - ახალი წიგნის დამატება
def add_book_menu(manager):
    title = input_text("სათაური: ")
    author = input_text("ავტორი: ")
    year = input_year("გამოცემის წელი: ")

    # ტიპს ვითხოვთ მანამ, სანამ 1-ს ან 2-ს არ აირჩევს
    while True:
        book_type = input("ტიპი (1 - ნაბეჭდი, 2 - ელექტრონული): ").strip()
        if book_type in ("1", "2"):
            break
        print("აირჩიე 1 ან 2")

    # try - წლის setter-მა შეიძლება ValueError ააგდოს (მაგ. 3000 წელი)
    try:
        if book_type == "1":
            pages = input_positive_int("გვერდების რაოდენობა: ")
            book = PrintedBook(title, author, year, pages)
        else:
            file_format = input_text("ფაილის ფორმატი (მაგ. PDF, EPUB): ").upper()
            book = EBook(title, author, year, file_format)
    except ValueError as e:
        print(f"შეცდომა: {e}")
        return

    manager.add_book(book)
    print("წიგნი დაემატა")


# მენიუს მე-2 პუნქტი - ყველა წიგნის ჩვენება
def show_books_menu(manager):
    books = manager.get_all_books()
    if not books:
        print("სია ცარიელია")
        return
    # enumerate - თითო წიგნს ნომერს აძლევს, start=1 - დათვლა 1-დან იწყება
    for number, book in enumerate(books, start=1):
        print(f"{number}. {book}")


# მენიუს მე-3 პუნქტი - ძებნა სათაურით
def search_menu(manager):
    title = input_text("საძიებო სათაური: ")
    results = manager.search_by_title(title)
    if not results:
        print("ვერაფერი მოიძებნა")
        return
    for book in results:
        print(book)


# მენიუს მე-4 პუნქტი - წიგნის წაშლა
def delete_menu(manager):
    title = input_text("წასაშლელი წიგნის ზუსტი სათაური: ")
    # delete_book აბრუნებს True/False - ამის მიხედვით ვწერთ შეტყობინებას
    if manager.delete_book(title):
        print("წიგნი წაიშალა")
    else:
        print("ასეთი წიგნი ვერ მოიძებნა")

# ===== მთავარი მენიუ =====
def main():
    manager = BookManager()

    while True:
        print("\n===== წიგნების მენეჯერი =====")
        print("1. წიგნის დამატება")
        print("2. ყველა წიგნის ნახვა")
        print("3. ძებნა სათაურით")
        print("4. წიგნის წაშლა")
        print("0. გასვლა")
        choice = input("აირჩიე: ").strip()

        if choice == "1":
            add_book_menu(manager)
        elif choice == "2":
            show_books_menu(manager)
        elif choice == "3":
            search_menu(manager)
        elif choice == "4":
            delete_menu(manager)
        elif choice == "0":
            print("ნახვამდის!")
            break
        else:
            print("არასწორი არჩევანი, სცადე თავიდან")


# პროგრამა მხოლოდ მაშინ ეშვება, როცა ეს ფაილი პირდაპირ გავუშვით (python main.py)
if __name__ == "__main__":
    main()