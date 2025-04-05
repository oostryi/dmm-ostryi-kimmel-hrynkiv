from Classes.Graph import *

vertices = int(input("\nEnter the number of vertices: "))
density = float(input("Enter the density: "))
representation = input("Enter desired representation: ")

graph = Graph(vertices, density, representation)

print(f"\nExpected count of edges: {graph.get_expected_edges()}")
print(f"\nActual count of edges: {graph.get_actual_edges()}\n")
graph.show_adjacency()

Graph.visualise(graph)
