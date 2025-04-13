import random
import matplotlib
matplotlib.use('TkAgg')
import networkx as nx
import matplotlib.pyplot as plt
import time

class Graph:

    def __init__(self, n: int, density: float = 0.1, representation: str = "matrix") -> None:
        self.n = n
        self.density = density
        self.representation = self.set_representation(self, representation)
        self.adj_matrix = self._generate_dag_adjacency_matrix()
        self.adj_list = self._matrix_to_list()

    def _generate_dag_adjacency_matrix(self) -> list[list[int]]:
        matrix = [[0] * self.n for _ in range(self.n)]

        order = list(range(self.n))
        random.shuffle(order)
        index = {node: i for i, node in enumerate(order)}

        for i in range(self.n):
            for j in range(self.n):
                if index[i] < index[j] and random.random() < self.density:
                    matrix[i][j] = 1

        return matrix

    def _matrix_to_list(self) -> dict[int, list[int]]:
        adj_list = {i: [] for i in range(self.n)}

        for i in range(self.n):
            for j in range(self.n):
                if self.adj_matrix[i][j] == 1:
                    adj_list[i].append(j)

        return adj_list

    def get_expected_edges(self) -> int:
        return int(self.density * self.n * (self.n - 1))

    def get_actual_edges(self) -> int:
        return sum(sum(row) for row in self.adj_matrix)

    def visualise(self, topo_order: list[int] = None):
        g = nx.DiGraph()
        g.add_nodes_from(range(self.n))

        for i in range(self.n):
            for j in range(self.n):
                if self.adj_matrix[i][j] == 1:
                    g.add_edge(i, j)

        if topo_order:
            pos = {node: (i, 0) for i, node in enumerate(topo_order)}
        else:
            pos = nx.spring_layout(g)

        nx.draw(g, pos, with_labels=True, arrows=True, node_color='lightblue', edge_color='grey')
        plt.title("Topological Sort using DFS Visualization" if topo_order else "Graph Visualization")
        plt.show()

    def visualise_both(self):
        g = nx.DiGraph()
        g.add_nodes_from(range(self.n))

        for i in range(self.n):
            for j in range(self.n):
                if self.adj_matrix[i][j] == 1:
                    g.add_edge(i, j)

        topo_order = self.topological_sort_dfs()
        if not topo_order:
            print("Graph contains a cycle — topological sort is not possible.")
            return

        pos_circular = nx.circular_layout(g)
        center_offset = self.n / 2
        pos_topo = {node: (i - center_offset, 0) for i, node in enumerate(topo_order)}

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        plt.suptitle("Comparison: Circular Layout vs Topological Sort", fontsize=16)

        edge_style = dict(
            arrows=True,
            arrowsize=20,
            edge_color='black',
            connectionstyle='arc3,rad=0.1',
            node_size=800,
            width=1.5
        )

        edge_style_top = dict(
            arrows=True,
            arrowsize=20,
            edge_color='black',
            connectionstyle='arc3,rad=0.6',
            node_size=800,
            width=1.5
        )

        nx.draw_networkx_nodes(g, pos=pos_circular, ax=ax1, node_color='lightblue', node_size=800)
        nx.draw_networkx_labels(g, pos=pos_circular, ax=ax1, font_size=10)
        nx.draw_networkx_edges(g, pos=pos_circular, ax=ax1, **edge_style)
        ax1.set_title("Circular Layout")

        nx.draw_networkx_nodes(g, pos=pos_topo, ax=ax2, node_color='lightgreen', node_size=800)
        nx.draw_networkx_labels(g, pos=pos_topo, ax=ax2, font_size=10)
        nx.draw_networkx_edges(g, pos=pos_topo, ax=ax2, **edge_style_top)
        ax2.set_title("Topological Sort using DFS")

        ax2.set_xlim(-self.n / 2 - 1, self.n / 2 + 1)
        ax2.set_ylim(-2, 2)

        ax1.axis('off')
        ax2.axis('off')

        plt.tight_layout()
        plt.show()

    def show_adjacency(self):
        match self.representation:
            case "matrix":
                for row in self.adj_matrix:
                    print(row)
            case "list":
                for key, value in self.adj_list.items():
                    print(f"{key}: {value}")

    @staticmethod
    def set_representation(self, representation: str):
        match representation:
            case "matrix":
                return "matrix"
            case "list":
                return "list"
            case _:
                print("Invalid representation. Must be either matrix or list. Representation set to matrix.")
                return "matrix"



    def topological_sort_dfs(self) -> list[int] | None:
        visited = set()
        temp_mark = set()
        topo_order = []

        def dfs(node):
            if node in temp_mark:
                return False
            if node not in visited:
                temp_mark.add(node)
                for neighbor in self.adj_list[node]:
                    if not dfs(neighbor):
                        return False
                temp_mark.remove(node)
                visited.add(node)
                topo_order.append(node)
            return True

        for v in range(self.n):
            if v not in visited:
                if not dfs(v):
                    print("Graph has a cycle! Topological sort not possible.")
                    return None

        topo_order.reverse()
        return topo_order
    def execution_time(vertices: int, density: float, representation: str) -> float:
        start_time = time.time()
        graph = Graph(vertices, density, representation)
        graph.topological_sort_dfs()
        end_time = time.time()
        return end_time - start_time
