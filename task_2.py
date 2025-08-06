import pandas as pd
import random
from timeit import timeit
from BTrees.OOBTree import OOBTree

# Завантаження даних з CSV
def load_items_from_csv(file_path):
    df = pd.read_csv(file_path)
    df["ID"] = df["ID"].astype(int)
    df["Price"] = df["Price"].astype(float)
    return df.to_dict(orient="records")

# Додавання в OOBTree
def add_item_to_tree(tree, item):
    price = item["Price"]
    if price not in tree:
        tree[price] = []
    tree[price].append(item)

# Додавання в dict
def add_item_to_dict(d, item):
    d[item["ID"]] = item

# Діапазонний запит для OOBTree
def range_query_tree(tree, min_price, max_price):
    result = []
    for _, items in tree.items(min_price, max_price):
        result.extend(items)
    return result

# Діапазонний запит для dict
def range_query_dict(d, min_price, max_price):
    return [v for v in d.values() if min_price <= v["Price"] <= max_price]

# Основна функція
def main():
    file_path = "generated_items_data.csv"
    items = load_items_from_csv(file_path)

    tree = OOBTree()
    d = {}

    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(d, item)

        # Створення 100 випадкових діапазонів цін
    all_prices = [item["Price"] for item in items]
    min_p, max_p = min(all_prices), max(all_prices)

    query_ranges = [
        (
            round(random.uniform(min_p, max_p - 10), 2),
            round(random.uniform(min_p + 10, max_p), 2)
        )
        for _ in range(100)
    ]

    # Вимірювання часу для OOBTree
    def run_tree_queries():
        for qmin, qmax in query_ranges:
            range_query_tree(tree, qmin, qmax)

    # Вимірювання часу для dict
    def run_dict_queries():
        for qmin, qmax in query_ranges:
            range_query_dict(d, qmin, qmax)

    tree_time = timeit(run_tree_queries, number=1)
    dict_time = timeit(run_dict_queries, number=1)

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")


if __name__ == "__main__":
    main()