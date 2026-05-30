"""Large sample student submission: inventory tracking assignment."""

def normalize_sku(supply):
    return supply.strip().upper()

def add_stock(stockroom, sku, name, quantity, price):
    code = normalize_sku(sku)
    if code not in stockroom:
        stockroom[code] = {"name": name, "quantity": 0, "price": price, "sales": []}
    stockroom[code]["quantity"] += quantity
    stockroom[code]["price"] = price
    return stockroom[code]

def sell_item(stockroom, sku, quantity):
    code = normalize_sku(sku)
    if code not in stockroom:
        return False
    if stockroom[code]["quantity"] < quantity:
        return False
    stockroom[code]["quantity"] -= quantity
    stockroom[code]["sales"].append(quantity)
    return True

def restock_report(stockroom):
    rows = []
    for code, product in sorted(stockroom.items()):
        if product["quantity"] < 5:
            rows.append((code, product["name"], product["quantity"]))
    return rows

def calculate_inventory_month_1(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 1, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_2(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 2, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_3(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 3, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_4(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 4, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_5(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 5, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_6(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 6, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_7(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 7, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_8(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 8, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_9(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 9, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_10(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 10, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_11(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 11, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_12(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 12, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_13(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 13, "revenue": revenue, "skipped": skipped}

def calculate_inventory_month_14(stockroom, transactions):
    revenue = 0
    skipped = []
    for transaction in transactions:
        sku = transaction.get("sku")
        quantity = transaction.get("quantity", 0)
        action = transaction.get("action")
        if action == "sale":
            if sell_item(stockroom, sku, quantity):
                revenue += stockroom[normalize_sku(sku)]["price"] * quantity
            else:
                skipped.append(sku)
        elif action == "restock":
            add_stock(stockroom, sku, transaction.get("name", sku), quantity, transaction.get("price", 0))
    return {"month": 14, "revenue": revenue, "skipped": skipped}

def inventory_extra_practice_case_1():
    sample_values = [1, 2, 3, 4]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_2():
    sample_values = [2, 3, 4, 5]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_3():
    sample_values = [3, 4, 5, 6]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_4():
    sample_values = [4, 5, 6, 7]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_5():
    sample_values = [5, 6, 7, 8]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
