import heapq

# Define the network topology and link costs
network_topology = {
    "1": [("2", 1)],
    "2": [("1", 1), ("3", 6), ("5", 3)],
    "3": [("2", 6), ("4", 2)],
    "4": [("3", 2), ("5", 4)],
    "5": [("2", 3), ("4", 4)],
}

# Initialize the initial routing tables for all routers
initial_routing_tables = {}

for router, neighbors in network_topology.items():
    initial_routing_tables[router] = {neighbor: distance for neighbor, distance in neighbors}

# Print the initial routing tables
print("Initial Routing Tables:")
for router, neighbors in initial_routing_tables.items():
    print(f"Router {router}:")
    for neighbor, distance in neighbors.items():  # Changed this line
        print(f"  {neighbor} \t Distance: {distance}")

# Dijkstra's algorithm to calculate the final routing table for Router R1
def dijkstra(start_router, network_topology):
    distances = {router: float('inf') for router in network_topology}
    distances[start_router] = 0
    via = {router: [] for router in network_topology}

    # Priority queue to keep track of the routers to visit
    priority_queue = [(0, start_router)]

    while priority_queue:
        current_distance, current_router = heapq.heappop(priority_queue)

        if current_distance > distances[current_router]:
            continue

        for neighbor, neighbor_distance in network_topology[current_router]:
            total_distance = current_distance + neighbor_distance

            if total_distance < distances[neighbor]:
                distances[neighbor] = total_distance
                via[neighbor] = via[current_router] + [current_router]
                heapq.heappush(priority_queue, (total_distance, neighbor))

    return distances, via

# Calculate the final routing table for Router R1
for keys in network_topology:
    final_routing_table, via = dijkstra(keys, network_topology)

    # Print the final routing table for Router R1
    print(f'\nFinal Routing Table for Router {keys}:')
    print("Router\tDistance\tVia")
    for router, distance in final_routing_table.items():
        path = " -> ".join(via[router] + [router])
        print(f"{router}\t{distance}\t{path}")
