import sqlite3
import heapq
import os
import sys

# Yeh line ensure karti hai ki cost_model.py mil jaye
sys.path.append(os.path.dirname(__file__))
from cost_model import calculate_edge_weight

def get_graph_from_db():
    """Database se nodes aur edges fetch karke graph banao"""
    conn = sqlite3.connect('safeflow.db')
    cursor = conn.cursor()
    
    # Nodes fetch karo
    cursor.execute('SELECT id, name FROM nodes')
    nodes = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Edges fetch karo (Adjacency list banao)
    cursor.execute('SELECT from_node, to_node, distance FROM edges')
    graph = {}
    for from_node, to_node, distance in cursor.fetchall():
        if from_node not in graph:
            graph[from_node] = []
        if to_node not in graph:
            graph[to_node] = []
        
        # Dono direction mein edge add karo (undirected graph)
        graph[from_node].append((to_node, distance))
        graph[to_node].append((from_node, distance))
        
    conn.close()
    return graph, nodes

def dijkstra(graph, start, end, crowd_density='Low'):
    """Dijkstra's Algorithm with Dynamic Cost Model"""
    # Priority Queue: (cost, current_node, path)
    pq = [(0, start, [])]
    visited = set()
    
    while pq:
        (cost, node, path) = heapq.heappop(pq)
        
        if node not in visited:
            visited.add(node)
            path = path + [node]
            
            if node == end:
                return (cost, path)
                
            for neighbor, base_distance in graph.get(node, []):
                if neighbor not in visited:
                    # Yahan Cost Model use ho raha hai!
                    dynamic_weight = calculate_edge_weight(base_distance, crowd_density)
                    heapq.heappush(pq, (cost + dynamic_weight, neighbor, path))
                    
    return float("inf"), [] # Agar raasta na mile

if __name__ == '__main__':
    # Test karne ke liye
    print("Loading graph from database...")
    graph, nodes = get_graph_from_db()
    
    print(f"Nodes found: {nodes}")
    
    start_node = 1
    end_node = 4
    
    # Test 1: Low Crowd
    print(f"\n--- Test 1: Low Crowd ---")
    cost, path = dijkstra(graph, start_node, end_node, crowd_density='Low')
    if path:
        path_names = [nodes.get(n, f"Unknown({n})") for n in path]
        print(f"✅ Path: {' -> '.join(path_names)} | Cost: {cost}")

    # Test 2: High Crowd (Cost badh jana chahiye)
    print(f"\n--- Test 2: High Crowd ---")
    cost, path = dijkstra(graph, start_node, end_node, crowd_density='High')
    if path:
        path_names = [nodes.get(n, f"Unknown({n})") for n in path]
        print(f"✅ Path: {' -> '.join(path_names)} | Cost: {cost}")