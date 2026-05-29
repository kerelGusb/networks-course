class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.distances = {name: 0}
        self.next_hop = {name: name}
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        self.distances[neighbor] = cost
        self.next_hop[neighbor] = neighbor
    
    def update_from_neighbor(self, from_node, neighbor_dists):
        changed = False
        
        for dest, dist_to_dest in neighbor_dists.items():
            if dest == self.name:
                continue
            
            new_cost = self.neighbors[from_node] + dist_to_dest
            
            if dest not in self.distances:
                self.distances[dest] = new_cost
                self.next_hop[dest] = from_node
                changed = True
            elif new_cost < self.distances[dest]:
                self.distances[dest] = new_cost
                self.next_hop[dest] = from_node
                changed = True
            elif self.next_hop.get(dest) == from_node and new_cost > self.distances[dest]:
                self.distances[dest] = new_cost
                changed = True
        
        return changed
    
    def send_table(self):
        return self.distances.copy()
    
    def change_link_cost(self, neighbor, new_cost):
        if neighbor in self.neighbors:
            self.neighbors[neighbor] = new_cost
            self.distances[neighbor] = new_cost
            self.next_hop[neighbor] = neighbor
            
            to_remove = []
            for dest, hop in self.next_hop.items():
                if hop == neighbor and dest != neighbor:
                    to_remove.append(dest)
            
            for dest in to_remove:
                del self.distances[dest]
                del self.next_hop[dest]

def distance_vector_routing(nodes):
    changed = True
    iteration = 0
    
    while changed and iteration < 10:  # top cap with const (only for our routing scheme)
        changed = False
        iteration += 1
        
        for node_name, node in nodes.items():
            for neighbor_name in node.neighbors:
                neighbor = nodes[neighbor_name]
                neighbor_table = neighbor.send_table()
                
                if node.update_from_neighbor(neighbor_name, neighbor_table):
                    changed = True

def print_tables(nodes):
    print("ROUTING TABLES")
    for node in nodes.values():
        print(f"\nNode {node.name}:")
        for dest, cost in sorted(node.distances.items()):
            print(f"\tto {dest}: cost = {cost}, next hop = {node.next_hop[dest]}")

def main():
    nodes = {}

    for name in ['0', '1', '2', '3']:
        nodes[name] = Node(name)

    nodes['0'].add_neighbor('1', 1)
    nodes['0'].add_neighbor('2', 3)
    nodes['0'].add_neighbor('3', 7)

    nodes['1'].add_neighbor('0', 1)
    nodes['1'].add_neighbor('2', 1)

    nodes['2'].add_neighbor('1', 1)
    nodes['2'].add_neighbor('0', 3)
    nodes['2'].add_neighbor('3', 2)

    nodes['3'].add_neighbor('0', 7)
    nodes['3'].add_neighbor('2', 2)

    print("Initial state:")
    distance_vector_routing(nodes)
    print_tables(nodes)

    print("\n\n")
    print("Change link 1-2 cost from 1 to 5:")
    nodes['1'].change_link_cost('2', 5)
    nodes['2'].change_link_cost('1', 5)

    distance_vector_routing(nodes)
    print_tables(nodes)

    print("\n\n")
    print("Change link 0-2 cost from 3 to 1:")
    nodes['0'].change_link_cost('2', 1)
    nodes['2'].change_link_cost('0', 1)

    distance_vector_routing(nodes)
    print_tables(nodes)

if __name__ == "__main__":
    main()