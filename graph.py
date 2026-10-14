
import heapq


class BuildingGraph:
    def __init__(self):
        # Each location stores its connected paths.
        self.graph = {}

    def add_location(self, location):
        if location not in self.graph:
            self.graph[location] = []

    def add_path(self, start, end, distance, danger, congestion):
        # Lower total cost means a better evacuation route.
        cost = distance + (danger * 5) + (congestion * 3)

        self.add_location(start)
        self.add_location(end)

        # Add a path in both directions.
        self.graph[start].append((end, cost))
        self.graph[end].append((start, cost))

    def safest_route(self, start, destination):
        if start not in self.graph or destination not in self.graph:
            return [], float("inf")

        distances = {location: float("inf") for location in self.graph}
        previous = {}
        distances[start] = 0

        priority_queue = [(0, start)]

        while priority_queue:
            current_cost, current = heapq.heappop(priority_queue)

            if current_cost > distances[current]:
                continue

            if current == destination:
                break

            for neighbor, path_cost in self.graph[current]:
                new_cost = current_cost + path_cost

                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current
                    heapq.heappush(
                        priority_queue, (new_cost, neighbor)
                    )

        if distances[destination] == float("inf"):
            return [], float("inf")

        route = []
        current = destination

        while current != start:
            route.append(current)
            current = previous[current]

        route.append(start)
        route.reverse()

        return route, distances[destination]


if __name__ == "__main__":
    building = BuildingGraph()

    # Example building layout
    building.add_path("Room A", "Corridor", 2, 0, 1)
    building.add_path("Corridor", "Exit 1", 3, 0, 1)
    building.add_path("Room A", "Stairs", 4, 1, 0)
    building.add_path("Stairs", "Exit 2", 2, 0, 0)
    building.add_path("Corridor", "Stairs", 1, 2, 3)

    route, cost = building.safest_route("Room A", "Exit 2")

    print("SAFEFLOW - Emergency Evacuation System")
    print("---------------------------------------")

    if route:
        print("Recommended evacuation route:")
        print(" -> ".join(route))
        print("Total route cost:", cost)
    else:
        print("No available route to the selected exit.")