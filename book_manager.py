# book_manager.py - წიგნების სიის მართვა: დამატება, ნახვა, ძებნა, წაშლა
class BookManager:
    def __init__(self, storage):
        # ახალი: storage - BookStorage ობიექტი, რომლითაც ფაილთან ვმუშაობთ
        self.__storage = storage
        # ახალი: სია ცარიელი აღარაა - გაშვებისას ფაილიდან იტვირთება
        self.__books = storage.load()

    # add_book - ახალი წიგნის დამატება სიაში და ფაილის განახლება
    def add_book(self, book):
        self.__books.append(book)
        self.__storage.save(self.__books)  # ახალი

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

    # delete_book - წაშლა ზუსტი სათაურით და ფაილის განახლება
    def delete_book(self, title):
        for book in self.__books:
            if book.title.lower() == title.lower():
                self.__books.remove(book)
                self.__storage.save(self.__books)  # ახალი
                return True
        return False

    # ახალი: clear_all - ყველა წიგნის წაშლა სიიდან და თავად ფაილის წაშლა
    def clear_all(self):
        self.__books = []
        return self.__storage.delete()
