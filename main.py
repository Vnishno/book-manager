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

    @year.setter
    def year(self, value):
        current_year = datetime.now().year
        # isinstance - ვამოწმებთ, არის თუ არა value მთელი რიცხვი
        if not isinstance(value, int):
            raise TypeError("წელი უნდა იყოს მთელი რიცხვი")
        if value < 1 or value > current_year:
            raise ValueError(f"წელი უნდა იყოს 1-დან {current_year}-მდე")
        # მხოლოდ შემოწმების შემდეგ ვწერთ დამალულ ველში
        self.__year = value

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

#ტესტი
manager = BookManager()
manager.add_book(PrintedBook("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1712, 320))
manager.add_book(EBook("დათა თუთაშხია", "ჭაბუა ამირეჯიბი", 1975, "PDF"))
manager.add_book(PrintedBook("ჯაყოს ხიზნები", "მიხეილ ჯავახიშვილი", 1925, 250))

print("--- ყველა წიგნი ---")
for book in manager.get_all_books():
    print(book)

print("--- ძებნა: 'დათა' ---")
for book in manager.search_by_title("დათა"):
    print(book)

print("--- წაშლა ---")
print(manager.delete_book("ჯაყოს ხიზნები"))
print(manager.delete_book("არარსებული წიგნი"))

print("--- ყველა წიგნი წაშლის შემდეგ ---")
for book in manager.get_all_books():
    print(book)