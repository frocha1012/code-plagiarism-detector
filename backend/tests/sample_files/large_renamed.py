def clean_name(name):
    return name.strip().lower()


def register_item(storage, name, writer, section, amount):
    item_id = clean_name(name)

    if item_id not in storage:
        storage[item_id] = {
            "title": name.strip(),
            "author": writer.strip(),
            "category": section.strip(),
            "copies": 0,
            "borrowed": 0,
            "borrowers": [],
        }

    storage[item_id]["copies"] += amount


def checkout_item(storage, name, pupil, start_day):
    item_id = clean_name(name)
    if item_id not in storage:
        return False, "Book not found."

    record = storage[item_id]
    remaining = record["copies"] - record["borrowed"]
    if remaining <= 0:
        return False, "No copies available."

    record["borrowed"] += 1
    record["borrowers"].append(
        {"student": pupil, "day": start_day}
    )
    return True, "Book borrowed successfully."


def checkin_item(storage, name, pupil):
    item_id = clean_name(name)
    if item_id not in storage:
        return False, "Book not found."

    record = storage[item_id]
    for entry in record["borrowers"]:
        if entry["student"].lower() == pupil.lower():
            record["borrowers"].remove(entry)
            record["borrowed"] -= 1
            return True, "Book returned successfully."

    return False, "Borrow record not found."


def find_late_records(storage, today, limit):
    late_list = []
    for record in storage.values():
        for entry in record["borrowers"]:
            total_days = today - entry["day"]
            if total_days > limit:
                late_list.append(
                    {
                        "title": record["title"],
                        "student": entry["student"],
                        "days": total_days,
                    }
                )
    return late_list


def create_section_summary(storage):
    summary = {}
    for record in storage.values():
        section = record["category"]
        if section not in summary:
            summary[section] = {
                "total_books": 0,
                "borrowed_books": 0,
                "available_books": 0,
            }
        summary[section]["total_books"] += record["copies"]
        summary[section]["borrowed_books"] += record["borrowed"]
        summary[section]["available_books"] += record["copies"] - record["borrowed"]
    return summary


def lookup_items(storage, search_text):
    search_text = search_text.lower()
    found = []
    for record in storage.values():
        has_name = search_text in record["title"].lower()
        has_writer = search_text in record["author"].lower()
        has_section = search_text in record["category"].lower()
        if has_name or has_writer or has_section:
            found.append(record)
    return found


def show_stock(storage):
    print("LIBRARY INVENTORY")
    print("-" * 40)
    for record in storage.values():
        remaining = record["copies"] - record["borrowed"]
        print(f"{record['title']} by {record['author']}")
        print(f"Category: {record['category']}")
        print(f"Total: {record['copies']} | Borrowed: {record['borrowed']} | Available: {remaining}")
        print()


def show_late_items(late_list):
    print("OVERDUE BOOKS")
    print("-" * 40)
    if not late_list:
        print("No overdue books.")
        return
    for entry in late_list:
        print(f"{entry['student']} has '{entry['title']}' for {entry['days']} days.")


def run_program():
    book_storage = {}

    register_item(book_storage, "Python Basics", "Anne Smith", "Programming", 4)
    register_item(book_storage, "Data Structures", "Mark Brown", "Computer Science", 3)
    register_item(book_storage, "Modern History", "Laura White", "History", 2)
    register_item(book_storage, "Python Basics", "Anne Smith", "Programming", 1)

    checkout_item(book_storage, "Python Basics", "Daniel", 3)
    checkout_item(book_storage, "Data Structures", "Maria", 5)
    checkout_item(book_storage, "Modern History", "John", 1)
    checkout_item(book_storage, "Python Basics", "Sofia", 7)

    checkin_item(book_storage, "Modern History", "John")
    show_stock(book_storage)

    section_summary = create_section_summary(book_storage)
    print("CATEGORY REPORT")
    print("-" * 40)
    for section, values in section_summary.items():
        print(section)
        print(f"Total: {values['total_books']}")
        print(f"Borrowed: {values['borrowed_books']}")
        print(f"Available: {values['available_books']}")
        print()

    late_items = find_late_records(book_storage, today=12, limit=6)
    show_late_items(late_items)

    print()
    print("SEARCH RESULTS FOR 'python'")
    print("-" * 40)
    matches = lookup_items(book_storage, "python")
    for match in matches:
        print(match["title"])


if __name__ == "__main__":
    run_program()
