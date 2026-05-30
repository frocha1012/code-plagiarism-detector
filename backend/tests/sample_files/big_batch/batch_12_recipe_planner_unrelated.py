"""Completely different sample: recipe planning and shopping list builder."""


PANTRY = {
    "rice": 500,
    "beans": 350,
    "tomato": 6,
    "onion": 4,
    "garlic": 10,
    "pasta": 300,
    "cheese": 120,
}


def scale_ingredients(ingredients, servings, target_servings):
    multiplier = target_servings / servings
    scaled = {}

    for name, amount in ingredients.items():
        scaled[name] = round(amount * multiplier, 2)

    return scaled


def pantry_shortages(required, pantry):
    missing = {}

    for ingredient, needed in required.items():
        available = pantry.get(ingredient, 0)
        if available < needed:
            missing[ingredient] = round(needed - available, 2)

    return missing


def recipe_cost(ingredients, prices):
    total = 0

    for ingredient, amount in ingredients.items():
        unit_price = prices.get(ingredient, 0)
        total += amount * unit_price

    return round(total, 2)


def choose_affordable_recipes(recipes, prices, budget):
    selected = []

    for recipe in recipes:
        scaled = scale_ingredients(
            recipe["ingredients"],
            recipe["servings"],
            recipe["target_servings"],
        )
        cost = recipe_cost(scaled, prices)

        if cost <= budget:
            selected.append({
                "name": recipe["name"],
                "cost": cost,
                "ingredients": scaled,
            })

    return sorted(selected, key=lambda item: item["cost"])


def build_shopping_list(recipes, pantry):
    shopping = {}

    for recipe in recipes:
        scaled = scale_ingredients(
            recipe["ingredients"],
            recipe["servings"],
            recipe["target_servings"],
        )
        shortages = pantry_shortages(scaled, pantry)

        for ingredient, amount in shortages.items():
            shopping[ingredient] = shopping.get(ingredient, 0) + amount

    return {
        ingredient: round(amount, 2)
        for ingredient, amount in sorted(shopping.items())
    }


def group_recipes_by_tag(recipes):
    groups = {}

    for recipe in recipes:
        for tag in recipe.get("tags", []):
            if tag not in groups:
                groups[tag] = []
            groups[tag].append(recipe["name"])

    return groups


def format_menu(recipes):
    lines = []

    for day_index, recipe in enumerate(recipes, start=1):
        tags = ", ".join(recipe.get("tags", []))
        lines.append(f"Day {day_index}: {recipe['name']} ({tags})")

    return "\n".join(lines)


def sample_recipes():
    return [
        {
            "name": "Tomato Rice Bowl",
            "servings": 2,
            "target_servings": 4,
            "tags": ["vegetarian", "budget"],
            "ingredients": {"rice": 180, "tomato": 2, "onion": 1, "garlic": 2},
        },
        {
            "name": "Bean Pasta Bake",
            "servings": 3,
            "target_servings": 3,
            "tags": ["dinner", "comfort"],
            "ingredients": {"pasta": 240, "beans": 120, "cheese": 80, "tomato": 3},
        },
        {
            "name": "Garlic Beans",
            "servings": 2,
            "target_servings": 5,
            "tags": ["quick", "protein"],
            "ingredients": {"beans": 250, "garlic": 4, "onion": 2},
        },
    ]


def run_demo():
    prices = {
        "rice": 0.01,
        "beans": 0.02,
        "tomato": 0.4,
        "onion": 0.25,
        "garlic": 0.1,
        "pasta": 0.015,
        "cheese": 0.05,
    }
    recipes = sample_recipes()

    return {
        "menu": format_menu(recipes),
        "tags": group_recipes_by_tag(recipes),
        "shopping": build_shopping_list(recipes, PANTRY),
        "affordable": choose_affordable_recipes(recipes, prices, 10),
    }


if __name__ == "__main__":
    plan = run_demo()
    print(plan["menu"])
    print("Shopping list:", plan["shopping"])
