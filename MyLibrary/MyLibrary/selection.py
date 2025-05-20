import json
from dataclasses import dataclass, field
from unittest import result
from MyLibrary.book import Book
from MyLibrary.random_number_utils import RandomNumberUtils
from MyLibrary.file_io import Fstream



@dataclass
class Selection:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(init=False, default_factory=RandomNumberUtils.generate_random_id)

    def get_all_books(self, verbose=0)->dict:
        """
        Reads and returns a has map with all the available books

        Args:
            if verbose is set to 1, it will print all the items.

        Returns:
            dict: a hash map with all the items in the database.
        """
        data_file = Fstream.load_json_files(self.database_path)

        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

        try:
            if verbose == 1:
                Fstream.print_json_structure(data_file)
                return data_file
            else:
                return data_file

        except:
            raise ValueError("The value for the verbose as to be 0 or 1")
         

    def menu_book_selection(self):
        """
        Displays a menu for selecting, searching, or deleting books.
        """
        results = self.get_all_books()
        print("Menu:")
        print("0 - Select one or more books")
        print("1 - Search for a book by name")
        print("2 - Select all books")
        print("3 - Delete one or more books")
        choice = input("Your choice: ")

        if choice == "0":           
            print("List of books:")
            books = results["books"]
            ids_list = list(books.keys())
            for i, book_id in enumerate(ids_list):
                book = books[book_id]
                print(f"{i}: {book['name']} (ID: {book_id})")        
            
            user_input = input("Enter the index(es) of the book(s) to select (separated by commas): ")
            index_list = []
            for part in user_input.split(","):
                if part.strip().isdigit():
                    index_list.append(int(part.strip()))          
            
            selected_books = []
            for index in index_list:
                if 0 <= index < len(ids_list):
                    book_id = ids_list[index]
                    selected_books.append(books[book_id])
            
            print("Selected books:")
            for book in selected_books:
                print(book['name'])

        elif choice == "1":
            search = input("Enter the name of the book to search for: ").lower()
            books = results["books"]
            found_books = []
           
            for book_id, book in books.items():
                if search in book['name'].lower():
                    found_books.append(book)
           
            if found_books:
                print("Books found:")
                for book in found_books:
                    print(book['name'])
            else:
                print("No book found.")

        elif choice == "2":  
            print("All books selected:")
            for book_id, book in results["books"].items():
                print(book['name'])

        elif choice == "3":
            print("List of books:")
            books = results["books"]
            ids_list = list(books.keys())
            for i, book_id in enumerate(ids_list):
                book = books[book_id]
                print(f"{i}: {book['name']} (ID: {book_id})")
            
            user_input = input("Enter the index(es) of the book(s) to delete (separated by commas): ")
            index_list = []
            for part in user_input.split(","):
                if part.strip().isdigit():
                    index_list.append(int(part.strip()))
            
            books_to_delete = []
            for index in index_list:
                if 0 <= index < len(ids_list):
                    book_id = ids_list[index]
                    books_to_delete.append(book_id)

            remaining_books = {}
            for book_id, book in books.items():
                if book_id not in books_to_delete:
                    remaining_books[book_id] = book

            print("Books deleted.")
            print("Remaining books:")
            for book_id, book in remaining_books.items():
                print(book['name'])

        else:
            print("Unknown choice.")