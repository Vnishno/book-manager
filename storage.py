# storage.py - JSON ფაილთან მუშაობა: წიგნების წაკითხვა, ჩაწერა, ფაილის წაშლა
import json
import os

from book import book_from_dict

# BookStorage - მხოლოდ ფაილთან მუშაობა: წაკითხვა, ჩაწერა, წაშლა
class BookStorage:
    def __init__(self, file_path):
        self.file_path = file_path

    # load - ფაილიდან წიგნების სიის წაკითხვა
    def load(self):
        # os.path.exists - თუ ფაილი ჯერ არ არსებობს (პირველი გაშვება), ცარიელ სიას ვაბრუნებთ
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        # JSONDecodeError - ფაილი დაზიანებულია (არასწორი JSON), ცარიელი სიით ვიწყებთ
        except json.JSONDecodeError:
            return []

        books = []
        for item in data:
            books.append(book_from_dict(item))
        return books

    # save - წიგნების სიის ჩაწერა ფაილში (თუ ფაილი არ არსებობს, "w" რეჟიმი თვითონ შექმნის)
    def save(self, books):
        data = []
        for book in books:
            data.append(book.to_dict())
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    # delete - ფაილის წაშლა; აბრუნებს True თუ წაიშალა, False თუ ფაილი არ არსებობდა
    def delete(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            return True
        return False
