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

def summarize_supplier_quality(suppliers):
    totals = {}
    for supplier in suppliers:
        region = supplier.get("region", "unknown")
        if region not in totals:
            totals[region] = {"count": 0, "score": 0}
        totals[region]["count"] += 1
        totals[region]["score"] += supplier.get("rating", 0)
    for region, data in totals.items():
        data["average"] = data["score"] / data["count"]
    return totals

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
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_6():
    sample_values = [6, 7, 8, 9]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_7():
    sample_values = [7, 8, 9, 10]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_8():
    sample_values = [8, 9, 10, 11]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_9():
    sample_values = [9, 10, 11, 12]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_10():
    sample_values = [10, 11, 12, 13]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_11():
    sample_values = [11, 12, 13, 14]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_12():
    sample_values = [12, 13, 14, 15]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_13():
    sample_values = [13, 14, 15, 16]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
            total += value * 2
    return total

def inventory_extra_practice_case_14():
    sample_values = [14, 15, 16, 17]
    total = 0
    for value in sample_values:
        if value % 2 == 0:
            total += value
        else:
