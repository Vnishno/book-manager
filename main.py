# Book Manager - წიგნების მართვის კონსოლ აპლიკაცია


# Book - ერთი წიგნი: სათაური, ავტორი, გამოცემის წელი
class Book:
    # __init__ - ეშვება ობიექტის შექმნისას და ველებს ავსებს
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        # __year - დამალული ველი (encapsulation), გარედან პირდაპირ ვერ მივწვდებით
        self.__year = year

    # @property - წელს ვკითხულობთ ისე, თითქოს ჩვეულებრივი ველი იყოს: book.year
    @property
    def year(self):
        return self.__year

    # __str__ - როგორ გამოჩნდეს წიგნი print()-ის დროს
    def __str__(self):
        return f"{self.title} - {self.author} ({self.year})"


# --- დროებითი ტესტი (მერე წავშლით) ---
book1 = Book("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1712)
print(book1)
print(book1.year)