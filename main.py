# Book Manager - წიგნების მართვის კონსოლ აპლიკაცია

from datetime import datetime

# Book - ერთი წიგნი: სათაური, ავტორი, გამოცემის წელი
class Book:
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

    # __str__ - როგორ გამოჩნდეს წიგნი print()-ის დროს
    def __str__(self):
        return f"{self.title} - {self.author} ({self.year})"

# --- დროებითი ტესტი (მერე წავშლით) ---
book1 = Book("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1712)
print(book1)

book1.year = 1937
print(book1)

try:
    Book("რაღაც წიგნი", "ავტორი", 3000)
except ValueError as e:
    print("შეცდომა:", e)

try:
    book1.year = "abc"
except TypeError as e:
    print("შეცდომა:", e)