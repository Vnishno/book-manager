# Book Manager - წიგნების მართვის კონსოლ აპლიკაცია
from book import  PrintedBook, EBook
from storage import BookStorage
from book_manager import BookManager
from validators import input_text, input_positive_int, input_year

# ===== მენიუს ფუნქციები =====

# მენიუს 1-ლი პუნქტი - ახალი წიგნის დამატება
def add_book_menu(manager):
    title = input_text("სათაური: ")
    author = input_text("ავტორი: ")
    year = input_year("გამოცემის წელი: ")

    # ტიპს ვითხოვთ მანამ, სანამ 1-ს ან 2-ს არ აირჩევს
    while True:
        book_type = input("ტიპი (1 - ნაბეჭდი, 2 - ელექტრონული): ").strip()
        if book_type in ("1", "2"):
            break
        print("აირჩიე 1 ან 2")

    # try - წლის setter-მა შეიძლება ValueError ააგდოს (მაგ. 3000 წელი)
    try:
        if book_type == "1":
            pages = input_positive_int("გვერდების რაოდენობა: ")
            book = PrintedBook(title, author, year, pages)
        else:
            file_format = input_text("ფაილის ფორმატი (მაგ. PDF, EPUB): ").upper()
            book = EBook(title, author, year, file_format)
    except ValueError as e:
        print(f"შეცდომა: {e}")
        return

    manager.add_book(book)
    print("წიგნი დაემატა")


# მენიუს მე-2 პუნქტი - ყველა წიგნის ჩვენება
def show_books_menu(manager):
    books = manager.get_all_books()
    if not books:
        print("სია ცარიელია")
        return
    # enumerate - თითო წიგნს ნომერს აძლევს, start=1 - დათვლა 1-დან იწყება
    for number, book in enumerate(books, start=1):
        print(f"{number}. {book}")


# მენიუს მე-3 პუნქტი - ძებნა სათაურით
def search_menu(manager):
    title = input_text("საძიებო სათაური: ")
    results = manager.search_by_title(title)
    if not results:
        print("ვერაფერი მოიძებნა")
        return
    for book in results:
        print(book)


# მენიუს მე-4 პუნქტი - წიგნის წაშლა
def delete_menu(manager):
    title = input_text("წასაშლელი წიგნის ზუსტი სათაური: ")
    # delete_book აბრუნებს True/False - ამის მიხედვით ვწერთ შეტყობინებას
    if manager.delete_book(title):
        print("წიგნი წაიშალა")
    else:
        print("ასეთი წიგნი ვერ მოიძებნა")

# მენიუს მე-5 პუნქტი - ყველა წიგნის და ფაილის წაშლა (დადასტურებით)
def clear_all_menu(manager):
    answer = input("ნამდვილად გინდა ყველა წიგნის წაშლა? (კი/არა): ").strip().lower()
    if answer != "კი":
        print("გაუქმდა")
        return
    if manager.clear_all():
        print("ყველა წიგნი და ფაილი წაიშალა")
    else:
        print("ფაილი არ არსებობდა, სია გასუფთავდა")

# ===== მთავარი მენიუ =====
def main():
    # storage იქმნება პირველი და გადაეცემა manager-ს
    storage = BookStorage("books.json")
    manager = BookManager(storage)

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
            add_book_menu(manager)
        elif choice == "2":
            show_books_menu(manager)
        elif choice == "3":
            search_menu(manager)
        elif choice == "4":
            delete_menu(manager)
        elif choice == "5":
            clear_all_menu(manager)
        elif choice == "0":
            print("თქვენ გახვედით მენიუდან!")
            break
        else:
            print("არასწორი არჩევანი, სცადე თავიდან")


# პროგრამა მხოლოდ მაშინ ეშვება, როცა ეს ფაილი პირდაპირ გავუშვით (python main.py)
if __name__ == "__main__":
    main()