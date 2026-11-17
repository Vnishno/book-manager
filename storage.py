# storage.py - JSON ფაილთან მუშაობა
# ფაილის შექმნა, რედაქტირება (თავიდან ჩაწერა), წაკითხვა და წაშლა
import json
import os

from book import PrintedBook, EBook


# BookStorage - მხოლოდ ფაილთან მუშაობს: წაკითხვა, ჩაწერა, წაშლა
# წიგნების სიას თვითონ არ მართავს - ეს BookManager-ის საქმეა
class BookStorage:
    # file_path - ფაილის სახელი/მისამართი, მაგ. "books.json"
    def __init__(self, file_path):
        self.file_path = file_path

    # load - ფაილიდან წიგნების წაკითხვა; აბრუნებს წიგნების (ობიექტების) სიას
    def load(self):
        # os.path.exists - თუ ფაილი ჯერ არ არსებობს (პირველი გაშვება), ცარიელ სიას ვაბრუნებთ
        if not os.path.exists(self.file_path):
            return []
        try:
            # with open - ფაილს ხსნის და ბოლოს თვითონ ხურავს; "r" - მხოლოდ წასაკითხად
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        # JSONDecodeError - ფაილი დაზიანებულია (არასწორი JSON), ცარიელი სიით ვიწყებთ
        except json.JSONDecodeError:
            return []

        # ლექსიკონების სიას ვაქცევთ წიგნების (ობიექტების) სიად
        books = []
        for item in data:
            # თუ ერთი ჩანაწერი დაზიანებულია (აკლია ველი, არასწორი წელი ან ტიპი),
            # პროგრამა არ ითიშება - ამ ჩანაწერს უბრალოდ გამოვტოვებთ
            try:
                books.append(BookStorage.book_from_dict(item))
            except (KeyError, ValueError, TypeError):
                continue
        return books

    # book_from_dict - ფაილიდან წაკითხულ ლექსიკონში "type"-ს უყურებს
    # და წყვეტს, PrintedBook შექმნას თუ EBook
    # @staticmethod - ობიექტი არ სჭირდება, კლასზე იძახება: BookStorage.book_from_dict(data)
    @staticmethod
    def book_from_dict(data):
        if data["type"] == "printed":
            return PrintedBook.from_dict(data)
        if data["type"] == "ebook":
            return EBook.from_dict(data)
        raise ValueError(f"უცნობი ტიპი: {data['type']}")

    # save - წიგნების სიის ჩაწერა ფაილში
    # "w" - ძველ შიგთავსს შლის და თავიდან წერს; თუ ფაილი არ არსებობს, თვითონ ქმნის
    def save(self, books):
        # ობიექტებს ვაქცევთ ლექსიკონებად, რადგან JSON-ს ობიექტის შენახვა არ შეუძლია
        data = []
        for book in books:
            data.append(book.to_dict())
        with open(self.file_path, "w", encoding="utf-8") as file:
            # ensure_ascii=False - ქართული ასოები ნორმალურად ინახება
            # indent=4 - ფაილი ლამაზად, ხაზებად იწერება
            json.dump(data, file, ensure_ascii=False, indent=4)

    # delete - ფაილის წაშლა; აბრუნებს True თუ წაიშალა, False თუ ფაილი არ არსებობდა
    def delete(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            return True
        return False
