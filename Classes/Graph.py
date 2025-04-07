import random
import matplotlib
matplotlib.use('TkAgg')
import networkx as nx
import matplotlib.pyplot as plt


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

    def visualise(self):
        g = nx.DiGraph()

        g.add_nodes_from(range(self.n))

        for i in range(self.n):
            for j in range(self.n):
                if self.adj_matrix[i][j] == 1:
                    g.add_edge(i, j)

        # Draw the graph
        nx.draw(g, with_labels=True, arrows=True, node_color='lightblue')
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
