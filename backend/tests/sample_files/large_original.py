def normalize_title(title):
    return title.strip().lower()


def add_book(catalog, title, author, category, copies):
    book_key = normalize_title(title)
    if book_key not in catalog:
        catalog[book_key] = {
            "title": title.strip(),
            "author": author.strip(),
            "category": category.strip(),
            "copies": 0,
            "borrowed": 0,
            "borrowers": [],
        }
    catalog[book_key]["copies"] += copies


def borrow_book(catalog, title, student_name, borrow_day):
    book_key = normalize_title(title)
    if book_key not in catalog:
        return False, "Book not found."

    book = catalog[book_key]
    available = book["copies"] - book["borrowed"]
    if available <= 0:
        return False, "No copies available."

    book["borrowed"] += 1
    book["borrowers"].append({"student": student_name, "day": borrow_day})
    return True, "Book borrowed successfully."


def return_book(catalog, title, student_name):
    book_key = normalize_title(title)
    if book_key not in catalog:
        return False, "Book not found."

    book = catalog[book_key]
    for borrower in book["borrowers"]:
        if borrower["student"].lower() == student_name.lower():
            book["borrowers"].remove(borrower)
            book["borrowed"] -= 1
            return True, "Book returned successfully."

    return False, "Borrow record not found."


def get_overdue_books(catalog, current_day, max_days):
    overdue = []
    for book in catalog.values():
        for borrower in book["borrowers"]:
            borrowed_for = current_day - borrower["day"]
            if borrowed_for > max_days:
                overdue.append({
                    "title": book["title"],
                    "student": borrower["student"],
                    "days": borrowed_for,
                })
    return overdue


def build_category_report(catalog):
    report = {}
    for book in catalog.values():
        category = book["category"]
        if category not in report:
            report[category] = {
                "total_books": 0,
                "borrowed_books": 0,
                "available_books": 0,
            }
        report[category]["total_books"] += book["copies"]
        report[category]["borrowed_books"] += book["borrowed"]
        report[category]["available_books"] += book["copies"] - book["borrowed"]
    return report


def search_books(catalog, keyword):
    keyword = keyword.lower()
    matches = []
    for book in catalog.values():
        title_match = keyword in book["title"].lower()
        author_match = keyword in book["author"].lower()
        category_match = keyword in book["category"].lower()
        if title_match or author_match or category_match:
            matches.append(book)
    return matches


def print_inventory(catalog):
    print("LIBRARY INVENTORY")
    print("-" * 40)
    for book in catalog.values():
        available = book["copies"] - book["borrowed"]
        print(f"{book['title']} by {book['author']}")
        print(f"Category: {book['category']}")
        print(f"Total: {book['copies']} | Borrowed: {book['borrowed']} | Available: {available}")
        print()


def print_overdue(overdue_books):
    print("OVERDUE BOOKS")
    print("-" * 40)
    if not overdue_books:
        print("No overdue books.")
        return
    for item in overdue_books:
        print(f"{item['student']} has '{item['title']}' for {item['days']} days.")


def main():
    library_catalog = {}

    add_book(library_catalog, "Python Basics", "Anne Smith", "Programming", 4)
    add_book(library_catalog, "Data Structures", "Mark Brown", "Computer Science", 3)
    add_book(library_catalog, "Modern History", "Laura White", "History", 2)
    add_book(library_catalog, "Python Basics", "Anne Smith", "Programming", 1)

    borrow_book(library_catalog, "Python Basics", "Daniel", 3)
    borrow_book(library_catalog, "Data Structures", "Maria", 5)
    borrow_book(library_catalog, "Modern History", "John", 1)
    borrow_book(library_catalog, "Python Basics", "Sofia", 7)

    return_book(library_catalog, "Modern History", "John")
    print_inventory(library_catalog)

    category_report = build_category_report(library_catalog)
    print("CATEGORY REPORT")
    print("-" * 40)
    for category, data in category_report.items():
        print(category)
        print(f"Total: {data['total_books']}")
        print(f"Borrowed: {data['borrowed_books']}")
        print(f"Available: {data['available_books']}")
        print()

    overdue_books = get_overdue_books(library_catalog, current_day=12, max_days=6)
    print_overdue(overdue_books)

    print()
    print("SEARCH RESULTS FOR 'python'")
    print("-" * 40)
    results = search_books(library_catalog, "python")
    for result in results:
        print(result["title"])


if __name__ == "__main__":
    main()
