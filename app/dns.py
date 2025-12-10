from typing import Dict, List, Optional, Tuple

class DNSResolver:
    def __init__(self, records: List[Dict]):
        self.records = records
        self.a_map = {}
        self.cname_map = {}
        for r in records:
            t = r.get("type", "").upper()
            name = r.get("name", "").lower()
            val = r.get("value")
            if t == "A":
                self.a_map[name] = val
            elif t == "CNAME":
                self.cname_map[name] = val


    def resolve(self, name: str) -> Tuple[Optional[str], List[Dict]]:
        trace = []
        name = name.lower()
        visited = set()
        current = name

        while True:
            if current in visited:
                trace.append({"location": "DNS Resolver", "action": f"CNAME loop detected for {name}"})
                return None, trace
            visited.add(current)

            if current in self.a_map:
                ip = self.a_map[current]
                trace.append({"location": "DNS Resolver", "action": f"Resolved {name} -> {ip}"})
                return ip, trace

            if current in self.cname_map:
                nxt = self.cname_map[current]
                trace.append({"location": "DNS Resolver", "action": f"CNAME {current} -> {nxt}"})
                current = nxt.lower()
                continue

            trace.append({"location": "DNS Resolver", "action": f"NXDOMAIN: {name} not found"})
            return None, trace
