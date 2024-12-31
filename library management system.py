class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False

    def borrow_book(self):
        self.is_borrowed = True

    def return_book(self):
        self.is_borrowed = False

    def __str__(self):
        return f"Book ID: {self.book_id}, Title: '{self.title}', Author: '{self.author}', Borrowed: {self.is_borrowed}"


# Library Management System
books = []


def add_book():
    book_id = int(input("Enter Book ID: "))
    title = input("Enter Book Title: ")
    author = input("Enter Book Author: ")
    book = Book(book_id, title, author)
    books.append(book)
    print("Book added successfully!")


def display_books():
    if not books:
        print("No books in the library.")
    else:
        for book in books:
            print(book)


def borrow_book():
    book_id = int(input("Enter Book ID to borrow: "))
    for book in books:
        if book.book_id == book_id:
            if book.is_borrowed:
                print("Book is already borrowed.")
            else:
                book.borrow_book()
                print("Book borrowed successfully!")
            return
    print("Book not found.")


def return_book():
    book_id = int(input("Enter Book ID to return: "))
    for book in books:
        if book.book_id == book_id:
            if not book.is_borrowed:
                print("Book is not borrowed.")
            else:
                book.return_book()
                print("Book returned successfully!")
            return
    print("Book not found.")


def update_book_details():
    book_id = int(input("Enter Book ID to update: "))
    for book in books:
        if book.book_id == book_id:
            new_title = input("Enter new Title: ")
            book.title = new_title
            new_author = input("Enter new Author: ")
            book.author = new_author
            print("Book details updated successfully!")
            return
    print("Book not found.")


def main():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Update Book Details")
        print("6. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            add_book()
        elif choice == 2:
            display_books()
        elif choice == 3:
            borrow_book()
        elif choice == 4:
            return_book()
        elif choice == 5:
            update_book_details()
        elif choice == 6:
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
