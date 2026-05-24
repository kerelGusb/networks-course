import json
import copy
import threading
import time
import socket

class Router:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.neighbors = []
        self.running = True
        self.routing_table = {
            ip: {
                "next_hop": ip,
                "metric": 0
            }
        }

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1", self.port))
        self.socket.settimeout(0.5)

    def run(self):
        while self.running:
            self.send_table()
            self.process_messages()
            time.sleep(1)
        self.socket.close()

    def add_neighbor(self, neighbor_ip, neighbor_port):
        self.neighbors.append((neighbor_ip, neighbor_port))
        self.routing_table[neighbor_ip] = {
            "next_hop": neighbor_ip,
            "metric": 1
        }
    
    def send_table(self):
        message = {
            "sender_ip": self.ip,
            "table": self.routing_table
        }

        data = json.dumps(message).encode()

        for neighbor_ip, neighbor_port in self.neighbors:
            self.socket.sendto(
                data,
                ("127.0.0.1", neighbor_port)
            )


    def process_messages(self):
        updated = False
        while True:
            try:
                data, addr = self.socket.recvfrom(65536)
            except socket.timeout:
                break
            message = json.loads(data.decode())

            sender_ip = message["sender_ip"]
            table = message["table"]

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
        
        return updated

    
    def print_table(self):
        print("[Src IP]\t[Dest IP]\t[Next hop]\t[Metric]")
        for destination, route in self.routing_table.items():
            print(f"{self.ip}\t{destination}\t{route['next_hop']}\t{route['metric']}")
    


def main():
    with open("network2.json", "r") as f:
        data = json.load(f)

    routers = {}

    for router_data in data["routers"]:
        ip = router_data["ip"]
        port = router_data["port"]
        routers[ip] = Router(ip, port)
    
    for router_data in data["routers"]:
        cur_router = routers[router_data["ip"]]
        for neighbor in router_data["neighbors"]:
            cur_router.add_neighbor(
                neighbor["ip"],
                neighbor["port"]
            )


    threads = []

    for router in routers.values():
        t = threading.Thread(target=router.run)
        t.start()
        threads.append(t)
    
    # засыпаем на константное время, чтобы продемонстрировать работу
    time.sleep(10) 

    for router in routers.values():
        router.running = False
    
    for t in threads:
        t.join()

    for router in routers.values():
        print(f"\nFinal state of router {router.ip} table:")
        router.print_table()

if __name__ == "__main__":
    main()

    