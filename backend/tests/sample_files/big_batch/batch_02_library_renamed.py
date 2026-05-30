"""Large sample student submission: library management assignment."""

def clean_name(name):
    return name.strip().lower()

def register_item(storage, name, writer, section, amount):
    item_id = clean_name(name)
    if item_id not in storage:
        storage[item_id] = {
            "title": name.strip(),
            "author": writer.strip(),
            "category": section.strip(),
            "copies": amount,
            "borrowed": 0,
            "history": [],
        }
    else:
        storage[item_id]["copies"] += amount
    storage[item_id]["history"].append("added")
    return storage[item_id]

def borrow_item(storage, name):
    item_id = clean_name(name)
    if item_id not in storage:
        return False
    entry = storage[item_id]
    available = entry["copies"] - entry["borrowed"]
    if available <= 0:
        return False
    entry["borrowed"] += 1
    entry["history"].append("borrowed")
    return True

def return_item(storage, name):
    item_id = clean_name(name)
    if item_id not in storage:
        return False
    entry = storage[item_id]
    if entry["borrowed"] == 0:
        return False
    entry["borrowed"] -= 1
    entry["history"].append("returned")
    return True

def find_items_by_section(storage, section):
    results = []
    target = section.strip().lower()
    for key, entry in storage.items():
        if entry["category"].lower() == target:
            results.append(entry["title"])
    return sorted(results)

def build_storage_report(storage):
    report = []
    for key, entry in sorted(storage.items()):
        available = entry["copies"] - entry["borrowed"]
        status = "available" if available > 0 else "unavailable"
        report.append({
            "title": entry["title"],
            "available": available,
            "status": status,
        })
    return report

def show_late_items(records):
    overdue = []
    for record in records:
        days_late = record.get("days_late", 0)
        if days_late > 0:
            fine = days_late * 0.25
            overdue.append((record["student"], record["title"], fine))
    return overdue

def process_library_week_1(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 1, "processed": weekly_total, "alerts": alerts}

def process_library_week_2(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 2, "processed": weekly_total, "alerts": alerts}

def process_library_week_3(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 3, "processed": weekly_total, "alerts": alerts}

def process_library_week_4(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 4, "processed": weekly_total, "alerts": alerts}

def process_library_week_5(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 5, "processed": weekly_total, "alerts": alerts}

def process_library_week_6(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 6, "processed": weekly_total, "alerts": alerts}

def process_library_week_7(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 7, "processed": weekly_total, "alerts": alerts}

def process_library_week_8(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 8, "processed": weekly_total, "alerts": alerts}

def process_library_week_9(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 9, "processed": weekly_total, "alerts": alerts}

def process_library_week_10(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
        else:
            success = False
        if success:
            weekly_total += 1
        else:
            alerts.append(title)
    return {"week": 10, "processed": weekly_total, "alerts": alerts}

def process_library_week_11(storage, loans):
    weekly_total = 0
    alerts = []
    for loan in loans:
        title = loan.get("title", "")
        action = loan.get("action", "")
        if action == "borrow":
            success = borrow_item(storage, title)
        elif action == "return":
            success = return_item(storage, title)
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
