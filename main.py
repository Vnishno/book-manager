# main.py - Book Manager-ის მთავარი ფაილი (აქედან ეშვება პროგრამა)
# მენიუ და მომხმარებელთან ურთიერთობა (input / print)
from book import PrintedBook, EBook
from storage import BookStorage
from book_manager import BookManager
from validators import InputValidator


# BookApp - კონსოლის აპლიკაცია: აჩვენებს მენიუს და მომხმარებლის არჩევანს
# შესაბამის მეთოდს გადასცემს; წიგნებთან სამუშაოდ იყენებს BookManager-ს
class BookApp:
    # file_path - ფაილის სახელი, სადაც წიგნები ინახება
    def __init__(self, file_path):
        # ჯერ storage (ფაილთან სამუშაოდ), მერე manager, რომელიც ამ storage-ს იყენებს
        storage = BookStorage(file_path)
        # __manager - დამალული ველი; აპლიკაციის ყველა მეთოდი ერთსა და იმავე manager-ს იყენებს
        self.__manager = BookManager(storage)

    # მენიუს 1-ლი პუნქტი - ახალი წიგნის დამატება
    # ითხოვს მონაცემებს, ქმნის PrintedBook-ს ან EBook-ს და გადასცემს manager-ს
    def add_book(self):
        title = InputValidator.input_text("სათაური: ")
        author = InputValidator.input_text("ავტორი: ")
        year = InputValidator.input_year("გამოცემის წელი: ")
        book_type = InputValidator.input_choice("ტიპი (1 - ნაბეჭდი, 2 - ელექტრონული): ", ("1", "2"))

        # try - სარეზერვო დაცვა: წელი უკვე შემოწმებულია, მაგრამ თუ კლასი მაინც
        # ააგდებს შეცდომას, პროგრამა არ გაითიშება და შეტყობინებას გამოიტანს
        try:
            if book_type == "1":
                pages = InputValidator.input_positive_int("გვერდების რაოდენობა: ")
                book = PrintedBook(title, author, year, pages)
            else:
                # .upper() - "pdf" გახდება "PDF", რომ სიაში ფორმატები ერთნაირად ჩანდეს
                file_format = InputValidator.input_text("ფაილის ფორმატი (მაგ. PDF, EPUB): ").upper()
                book = EBook(title, author, year, file_format)
        except ValueError as e:
            print(f"შეცდომა: {e}")
            return

        self.__manager.add_book(book)
        print("წიგნი დაემატა")

    # მენიუს მე-2 პუნქტი - ყველა წიგნის ჩვენება დანომრილი სიით
    def show_books(self):
        books = self.__manager.get_all_books()
        if not books:
            print("სია ცარიელია")
            return
        # enumerate - თითო წიგნს ნომერს აძლევს, start=1 - დათვლა 1-დან იწყება
        for number, book in enumerate(books, start=1):
            print(f"{number}. {book}")

    # მენიუს მე-3 პუნქტი - ძებნა სათაურით (საკმარისია სათაურის ნაწილი)
    def search_book(self):
        title = InputValidator.input_text("საძიებო სათაური: ")
        results = self.__manager.search_by_title(title)
        if not results:
            print("ვერაფერი მოიძებნა")
            return
        # print(book) - ავტომატურად იძახებს Book-ის __str__ მეთოდს
        for book in results:
            print(book)

    # მენიუს მე-4 პუნქტი - წიგნის წაშლა
    def delete_book(self):
        title = InputValidator.input_text("წასაშლელი წიგნის ზუსტი სათაური: ")
        # delete_book აბრუნებს True/False - ამის მიხედვით ვწერთ შეტყობინებას
        if self.__manager.delete_book(title):
            print("წიგნი წაიშალა")
        else:
            print("ასეთი წიგნი ვერ მოიძებნა")

    # მენიუს მე-5 პუნქტი - ყველა წიგნის და ფაილის წაშლა (დადასტურებით)
    def clear_all(self):
        answer = input("ნამდვილად გინდა ყველა წიგნის წაშლა? (კი/არა): ").strip().lower()
        if answer != "კი":
            print("გაუქმდა")
            return
        if self.__manager.clear_all():
            print("ყველა წიგნი და ფაილი წაიშალა")
        else:
            print("ფაილი არ არსებობდა, სია გასუფთავდა")

    # run - მთავარი მენიუ
    # while True - მენიუ მეორდება მანამ, სანამ მომხმარებელი 0-ს არ აირჩევს (break)
    def run(self):
        while True:
            print("\n===== წიგნების მენეჯერი =====")
            print("1. წიგნის დამატება")
            print("2. ყველა წიგნის ნახვა")
            print("3. ძებნა სათაურით")
            print("4. წიგნის წაშლა")
            print("5. ყველა წიგნის წაშლა (ფაილის წაშლა)")
            print("0. გასვლა")
            choice = input("აირჩიე: ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.show_books()
            elif choice == "3":
                self.search_book()
            elif choice == "4":
                self.delete_book()
            elif choice == "5":
                self.clear_all()
            elif choice == "0":
                print("თქვენ გახვედით მენიუდან!")
                break
            else:
                print("არასწორი არჩევანი, სცადე თავიდან")


if __name__ == "__main__":
    app = BookApp("books.json")
    app.run()
