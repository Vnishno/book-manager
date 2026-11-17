# book.py - წიგნის კლასები
# აქ არის ოოპ-ის სამივე პრინციპი:
#   ინკაფსულაცია - __year დამალულია, წვდომა მხოლოდ @property-ით
#   მემკვიდრეობა - PrintedBook და EBook იღებენ ყველაფერს Book-ისგან
#   პოლიმორფიზმი - get_info() და to_dict() თითო კლასში თავისებურად მუშაობს
from datetime import datetime
from abc import ABC, abstractmethod


# Book - ზოგადი წიგნი (სათაური, ავტორი, წელი)
# ABC - აბსტრაქტული კლასი: შაბლონია, Book(...)-ით პირდაპირ ობიექტს ვერ შევქმნით
class Book(ABC):
    # __init__ - ეშვება ობიექტის შექმნისას და ველებს ავსებს
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        # self.year (და არა self.__year) - ასე ქვემოთ დაწერილი setter ეშვება და წელს ამოწმებს
        self.year = year

    # @property - წლის წაკითხვა: book.year (ფრჩხილების გარეშე, როგორც ჩვეულებრივი ველი)
    # __year - დამალული ველი (ინკაფსულაცია), გარედან book.__year არ მუშაობს
    @property
    def year(self):
        return self.__year

    # @year.setter - წლის შეცვლა: book.year = 1937
    # ჯერ ამოწმებს, მერე წერს - ასე არასწორი წელი ვერასდროს მოხვდება ობიექტში
    @year.setter
    def year(self, value):
        Book.validate_year(value)
        self.__year = value

    # validate_year - ამოწმებს წელს; თუ არასწორია, შეცდომას აგდებს (raise)
    # @staticmethod - ობიექტი არ სჭირდება, ამიტომ კლასზე იძახება: Book.validate_year(1990)
    # ერთი წესი ორ ადგილას გამოიყენება: setter-ში და მენიუში (validators.py)
    @staticmethod
    def validate_year(value):
        current_year = datetime.now().year
        # TypeError - არასწორი ტიპი (მაგ. ტექსტი რიცხვის ნაცვლად)
        if not isinstance(value, int):
            raise TypeError("წელი უნდა იყოს მთელი რიცხვი")
        # ValueError - ტიპი სწორია, მაგრამ მნიშვნელობა არა (მაგ. 3000)
        if value < 1 or value > current_year:
            raise ValueError(f"წელი უნდა იყოს 1-დან {current_year}-მდე")

    # get_info - წიგნის ტიპის ინფო (ნაბეჭდი/ელექტრონული)
    # @abstractmethod - აქ კოდი არ აქვს, ყველა შვილობილმა კლასმა თავისი ვერსია უნდა დაწეროს
    @abstractmethod
    def get_info(self):
        pass

    # to_dict - საერთო ველები ლექსიკონად, JSON ფაილში შესანახად
    # (შვილობილი კლასები ამას თავის ველებს დაუმატებენ)
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
        }

    # __str__ - როგორ გამოჩნდეს წიგნი print()-ის დროს
    # self.get_info() - გაეშვება იმ კლასის ვერსია, რომლის ობიექტიცაა (პოლიმორფიზმი)
    def __str__(self):
        return f"{self.title} - {self.author} ({self.year}) | {self.get_info()}"


# PrintedBook - ნაბეჭდი წიგნი
# მემკვიდრეობა: Book-ისგან იღებს ყველაფერს და უმატებს გვერდების რაოდენობას
class PrintedBook(Book):
    def __init__(self, title, author, year, pages):
        # super().__init__ - მშობლის __init__ ავსებს title, author, year (წლის შემოწმებით)
        super().__init__(title, author, year)
        self.pages = pages

    # get_info - მშობლის აბსტრაქტული მეთოდის საკუთარი ვერსია (override)
    def get_info(self):
        return f"ნაბეჭდი, {self.pages} გვ."

    # to_dict - მშობლის ლექსიკონს ვუმატებთ ტიპს და გვერდებს
    # "type" საჭიროა, რომ ფაილიდან წაკითხვისას ვიცოდეთ, რომელი კლასი შევქმნათ
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "printed"
        data["pages"] = self.pages
        return data

    # from_dict - ლექსიკონიდან (ფაილიდან წაკითხული) PrintedBook ობიექტის შექმნა
    # @classmethod - ობიექტი ჯერ არ არსებობს, ამიტომ კლასზე იძახება; cls = PrintedBook
    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["year"], data["pages"])


# EBook - ელექტრონული წიგნი
# მემკვიდრეობა: Book-ისგან იღებს ყველაფერს და უმატებს ფაილის ფორმატს (PDF, EPUB...)
class EBook(Book):
    def __init__(self, title, author, year, file_format):
        super().__init__(title, author, year)
        self.file_format = file_format

    # get_info - EBook-ის საკუთარი ვერსია (override)
    def get_info(self):
        return f"ელექტრონული, {self.file_format}"

    # to_dict - მშობლის ლექსიკონს ვუმატებთ ტიპს და ფაილის ფორმატს
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "ebook"
        data["file_format"] = self.file_format
        return data

    # from_dict - ლექსიკონიდან EBook ობიექტის შექმნა
    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["year"], data["file_format"])

