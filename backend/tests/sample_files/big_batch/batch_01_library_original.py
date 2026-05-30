"""Large sample student submission: library management assignment."""

def normalize_title(title):
    return title.strip().lower()

def add_book(catalog, title, author, category, copies):
    book_key = normalize_title(title)
    if book_key not in catalog:
        catalog[book_key] = {
            "title": title.strip(),
            "author": author.strip(),
            "category": category.strip(),
            "copies": copies,
            "borrowed": 0,
            "history": [],
        }
    else:
        catalog[book_key]["copies"] += copies
    catalog[book_key]["history"].append("added")
    return catalog[book_key]

def borrow_book(catalog, title):
    book_key = normalize_title(title)
    if book_key not in catalog:
        return False
    entry = catalog[book_key]
    available = entry["copies"] - entry["borrowed"]
    if available <= 0:
        return False
    entry["borrowed"] += 1
    entry["history"].append("borrowed")
    return True

def return_book(catalog, title):
    book_key = normalize_title(title)
    if book_key not in catalog:
        return False
    entry = catalog[book_key]
    if entry["borrowed"] == 0:
        return False
    entry["borrowed"] -= 1
    entry["history"].append("returned")
    return True

def find_books_by_category(catalog, category):
    results = []
    target = category.strip().lower()
    for key, entry in catalog.items():
        if entry["category"].lower() == target:
            results.append(entry["title"])
    return sorted(results)

def build_catalog_report(catalog):
    report = []
    for key, entry in sorted(catalog.items()):
        available = entry["copies"] - entry["borrowed"]
        status = "available" if available > 0 else "unavailable"
        report.append({
            "title": entry["title"],
            "available": available,
            "status": status,
        })
    return report

def print_overdue_books(records):
    overdue = []
    for record in records:
        days_late = record.get("days_late", 0)
        if days_late > 0:
            fine = days_late * 0.25
            overdue.append((record["student"], record["title"], fine))
    return overdue

def process_library_week_1(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 1, "processed": weekly_total, "alerts": alerts}

def process_library_week_2(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 2, "processed": weekly_total, "alerts": alerts}

def process_library_week_3(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 3, "processed": weekly_total, "alerts": alerts}

def process_library_week_4(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 4, "processed": weekly_total, "alerts": alerts}

def process_library_week_5(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 5, "processed": weekly_total, "alerts": alerts}

def process_library_week_6(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 6, "processed": weekly_total, "alerts": alerts}

def process_library_week_7(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 7, "processed": weekly_total, "alerts": alerts}

def process_library_week_8(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 8, "processed": weekly_total, "alerts": alerts}

def process_library_week_9(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 9, "processed": weekly_total, "alerts": alerts}

def process_library_week_10(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 10, "processed": weekly_total, "alerts": alerts}

def process_library_week_11(catalog, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_book(catalog, title)
        elif action == "return":
            success = return_book(catalog, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 11, "processed": weekly_total, "alerts": alerts}

def library_extra_practice_case_1():
    sample_values = [1, 2, 3, 4]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def library_extra_practice_case_2():
    sample_values = [2, 3, 4, 5]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def library_extra_practice_case_3():
    sample_values = [3, 4, 5, 6]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total
