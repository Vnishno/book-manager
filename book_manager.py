# book_manager.py - წიგნების სიის მართვა: დამატება, ნახვა, ძებნა, წაშლა


# BookManager - ინახავს წიგნების სიას და ყოველ ცვლილებას ფაილში წერს (storage-ით)
# print() აქ არ არის - კლასი მხოლოდ მონაცემებს აბრუნებს, ეკრანზე გამოტანა main.py-ის საქმეა
class BookManager:
    # storage - BookStorage ობიექტი, რომლითაც ფაილთან ვმუშაობთ (კომპოზიცია)
    def __init__(self, storage):
        self.__storage = storage
        # __books - დამალული სია (ინკაფსულაცია), გარედან მხოლოდ ამ კლასის მეთოდებით იცვლება
        # გაშვებისას წიგნები ფაილიდან იტვირთება
        self.__books = storage.load()

    # add_book - ახალი წიგნის დამატება სიაში და ფაილის განახლება
    def add_book(self, book):
        self.__books.append(book)
        self.__storage.save(self.__books)

    # get_all_books - ყველა წიგნის სია
    # .copy() - ვაბრუნებთ ასლს, რომ გარედან ორიგინალი სია ვერ შეცვალონ
    def get_all_books(self):
        return self.__books.copy()

    # search_by_title - ძებნა სათაურის ნაწილით; აბრუნებს ნაპოვნი წიგნების სიას
    # .lower() - დიდი/პატარა ასოები არ აქვს მნიშვნელობა ("harry" იპოვის "Harry Potter"-ს)
    def search_by_title(self, title):
        results = []
        for book in self.__books:
            if title.lower() in book.title.lower():
                results.append(book)
        return results

    # delete_book - წაშლა ზუსტი სათაურით და ფაილის განახლება
    # აბრუნებს True თუ წაიშალა, False თუ ასეთი წიგნი ვერ მოიძებნა
    def delete_book(self, title):
        for book in self.__books:
            if book.title.lower() == title.lower():
                self.__books.remove(book)
                self.__storage.save(self.__books)
                # return - ციკლს მაშინვე ვამთავრებთ, ამიტომ სიის შეცვლა ციკლში უსაფრთხოა
                return True
        return False

    # clear_all - ყველა წიგნის წაშლა სიიდან და თავად ფაილის წაშლა
    # აბრუნებს True თუ ფაილი წაიშალა, False თუ ფაილი არ არსებობდა
    def clear_all(self):
        self.__books = []
        return self.__storage.delete()
