import json
import copy

class Router:
    def __init__(self, ip):
        self.ip = ip
        self.neighbors = []
        self.inbox = []
        self.routing_table = {
            ip: {
                "next_hop": ip,
                "metric": 0
            }
        }

    def add_neighbor(self, neighbor_router):
        self.neighbors.append(neighbor_router)
        self.routing_table[neighbor_router.ip] = {
            "next_hop": neighbor_router.ip,
            "metric": 1
        }
    
    def send_table(self):
        for neighbor in self.neighbors:
            neighbor.inbox.append((self.ip, copy.deepcopy(self.routing_table)))
    
    def process_inbox(self):
        updated = False
        for sender_ip, table in self.inbox:
            for destination, route in table.items():
                if destination == self.ip:
                    continue

                new_metric = route["metric"] + 1
                if destination not in self.routing_table:
                    self.routing_table[destination] = {
                        "next_hop": sender_ip,
                        "metric": new_metric
                    }

                    updated = True
                
                elif new_metric < self.routing_table[destination]["metric"]:
                    self.routing_table[destination] = {
                        "next_hop": sender_ip,
                        "metric": new_metric
                    }

                    updated = True
        
        self.inbox.clear()

        return updated

    
    def print_table(self):
        print("[Src IP]\t[Dest IP]\t[Next hop]\t[Metric]")
        for destination, route in self.routing_table.items():
            print(f"{self.ip}\t{destination}\t{route['next_hop']}\t{route['metric']}")
    


def main():
    with open("network1.json", "r") as f:
        data = json.load(f)

    routers = {}

    for router_data in data["routers"]:
        ip = router_data["ip"]
        routers[ip] = Router(ip)
    
    for router_data in data["routers"]:
        cur_router = routers[router_data["ip"]]
        for neighbor_ip in router_data["neighbors"]:
            cur_router.add_neighbor(routers[neighbor_ip])

    changed = True
    step = 0

    while changed:
        changed = False
        for router in routers.values():
            router.send_table()
        
        for router in routers.values():
            if router.process_inbox():
                changed = True

        print(f"\nSimulation step {step}:")
        for router in routers.values():
            print(f"\nRouter {router.ip} table:")
            router.print_table()
        
        step += 1

    print('\n')

    for router in routers.values():
        print(f"\nFinal state of router {router.ip} table:")
        router.print_table()

if __name__ == "__main__":
    main()

    