# book.py - წიგნის კლასები: აბსტრაქტული Book და მისი შვილობილები PrintedBook, EBook
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

    # to_dict - საერთო ველები ლექსიკონად (შვილობილი კლასები ამას თავის ველებს დაუმატებენ)
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
        }
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
    # to_dict - მშობლის ლექსიკონს ვუმატებთ ტიპს და გვერდებს
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "printed"
        data["pages"] = self.pages
        return data

    # from_dict - ლექსიკონიდან PrintedBook ობიექტის შექმნა
    # @classmethod - ობიექტი ჯერ არ არსებობს, ამიტომ კლასზე იძახება, cls = PrintedBook
    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["year"], data["pages"])

# EBook - ელექტრონული წიგნი, გვერდების ნაცვლად აქვს ფაილის ფორმატი
class EBook(Book):
    def __init__(self, title, author, year, file_format):
        super().__init__(title, author, year)
        self.file_format = file_format

    def get_info(self):
        return f"ელექტრონული, {self.file_format}"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "ebook"
        data["file_format"] = self.file_format
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["year"], data["file_format"])

# book_from_dict - "type"-ის მიხედვით წყვეტს, რომელი კლასის ობიექტი შეიქმნას
def book_from_dict(data):
    if data["type"] == "printed":
        return PrintedBook.from_dict(data)
    if data["type"] == "ebook":
        return EBook.from_dict(data)
    raise ValueError(f"უცნობი ტიპი: {data['type']}")
