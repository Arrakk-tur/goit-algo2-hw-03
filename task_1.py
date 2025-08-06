from collections import deque
import pandas as pd


# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity, source, sink, parent):
    num_nodes = len(capacity)
    visited = [False] * num_nodes
    queue = deque([source])
    visited[source] = True
    parent[source] = -1

    while queue:
        u = queue.popleft()

        for v in range(num_nodes):
            if not visited[v] and capacity[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    return False


def edmonds_karp(capacity, source, sink):
    num_nodes = len(capacity)
    flow = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    while bfs(capacity, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s])
            s = parent[s]

        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            flow[u][v] += path_flow
            v = u

    return max_flow, flow


# Визначення вузлів і їх індексів
nodes = ["Джерело", "Стік"] + [f"Термінал {i}" for i in range(1, 3)] + \
        [f"Склад {i}" for i in range(1, 5)] + [f"Магазин {i}" for i in range(1, 15)]
node_to_index = {name: i for i, name in enumerate(nodes)}
index_to_node = {i: name for i, name in enumerate(nodes)}

source_node = "Джерело"
sink_node = "Стік"

# Побудова матриці пропускної здатності
num_nodes = len(nodes)
capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]

capacity_matrix[node_to_index[source_node]][node_to_index["Термінал 1"]] = float('inf')
capacity_matrix[node_to_index[source_node]][node_to_index["Термінал 2"]] = float('inf')

for i in range(1, 15):
    capacity_matrix[node_to_index[f"Магазин {i}"]][node_to_index[sink_node]] = float('inf')

edges = [
    ("Термінал 1", "Склад 1", 25), ("Термінал 1", "Склад 2", 20), ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15), ("Термінал 2", "Склад 4", 30), ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15), ("Склад 1", "Магазин 2", 10), ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15), ("Склад 2", "Магазин 5", 10), ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20), ("Склад 3", "Магазин 8", 15), ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20), ("Склад 4", "Магазин 11", 10), ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5), ("Склад 4", "Магазин 14", 10)
]

for u, v, cap in edges:
    capacity_matrix[node_to_index[u]][node_to_index[v]] = cap

# Запуск алгоритму Едмондса-Карпа
source_index = node_to_index[source_node]
sink_index = node_to_index[sink_node]

max_flow, final_flow_matrix = edmonds_karp(
    [row[:] for row in capacity_matrix], source_index, sink_index
)

# Максимальний потік
print(f"Максимальний потік у мережі: {max_flow} одиниць\n")


# Пошук шляхів і обчислення потоків
def find_terminal_to_store_flow(terminal_name, store_name, flow_matrix, node_to_index, index_to_node):
    terminal_idx = node_to_index[terminal_name]
    store_idx = node_to_index[store_name]

    total_flow = 0

    # Шляхи через склади
    for warehouse_idx in range(len(flow_matrix)):
        warehouse_name = index_to_node[warehouse_idx]
        if "Склад" in warehouse_name:
            flow_from_terminal_to_warehouse = flow_matrix[terminal_idx][warehouse_idx]
            flow_from_warehouse_to_store = flow_matrix[warehouse_idx][store_idx]

            path_flow = min(flow_from_terminal_to_warehouse, flow_from_warehouse_to_store)

            if path_flow > 0:
                total_flow += path_flow

    return total_flow


print("Таблиця фактичних потоків від терміналів до магазинів:\n")
final_flows_data = []

terminals = ["Термінал 1", "Термінал 2"]
stores = [f"Магазин {i}" for i in range(1, 15)]

for terminal in terminals:
    for store in stores:
        flow = find_terminal_to_store_flow(terminal, store, final_flow_matrix, node_to_index, index_to_node)
        if flow > 0:
            final_flows_data.append({"Термінал": terminal, "Магазин": store, "Фактичний Потік (одиниць)": flow})

flows_df = pd.DataFrame(final_flows_data)
print(flows_df)