"""Large unrelated sample submission: text_stats assignment."""

def text_stats_task_1(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_2(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_3(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_4(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_5(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_6(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_7(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_8(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_9(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_10(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_11(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_12(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_13(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_14(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_15(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_16(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
        elif value % 2 == 0:
            lookup[key].append(value + 4)
        else:
            lookup[key].append(value * 2)
    for key, values in lookup.items():
        result.append({"group": key, "total": sum(values), "count": len(values)})
    return sorted(result, key=lambda row: row["group"])

def text_stats_task_17(records):
    result = []
    lookup = {}
    for index, record in enumerate(records):
        key = record.get("group", "misc")
        value = record.get("value", index)
        if key not in lookup:
            lookup[key] = []
        if value % 3 == 0:
            lookup[key].append(value // 3)
