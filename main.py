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


# ტესტი
book1 = PrintedBook("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1712, 320)
book2 = EBook("დათა თუთაშხია", "ჭაბუა ამირეჯიბი", 1975, "PDF")

# ერთი და იგივე print, მაგრამ თითო წიგნი თავისებურად გამოიტანს თავის ინფოს
books = [book1, book2]
for book in books:
    print(book)

try:
    Book("რაღაც", "ავტორი", 2000)
except TypeError as e:
    print("შეცდომა:", e)