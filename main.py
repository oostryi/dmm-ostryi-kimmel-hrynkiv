from Classes.Graph import *

vertices = int(input("\nEnter the number of vertices: "))
density = float(input("Enter the density (0.0-1.0): "))
representation = input("Enter desired representation: ")

graph = Graph(vertices, density, representation)

print(f"\nExpected count of edges: {graph.get_expected_edges()}")
print(f"\nActual count of edges: {graph.get_actual_edges()}\n")
sizes = [10,30,70,100,150,170,190,200]
densities = [0.1, 0.3, 0.5, 0.7, 1.0]
representation = "matrix"

for size in sizes:
    for density in densities:
        execution_time = Graph.execution_time(size, density, representation)
        print(f"Graph size: {size} vertices, Density: {density}")
        print(f"Execution time: {execution_time:.6f}\n")
graph.show_adjacency()


order = graph.topological_sort_dfs()
if order:
    print("Topological Sort:", order)


graph.visualise_both()

