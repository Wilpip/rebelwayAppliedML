from MyLibrary import Book
from MyLibrary import Selection

if __name__ == "__main__":
    database = "./database.json"
    my_selection = Selection(database)

    #search for an book
    print("Searching book")
    results = my_selection.get_all_books(verbose=1)
    print("_________________")


    #select a book
    # Demander à l'utilisateur de sélectionner un ou plusieurs livres
    results = my_selection.menu_book_selection()
    print("_________________")

