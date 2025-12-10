# app/router.py
from typing import List, Dict, Optional
import ipaddress

class Route:
    def __init__(self, dest_cidr: str, next_hop: Optional[str], interface: str, router: str):
        self.network = ipaddress.ip_network(dest_cidr)
        self.next_hop = next_hop
        self.interface = interface
        self.router = router
        self.prefixlen = self.network.prefixlen

class RoutingEngine:
    def __init__(self, routes_config: List[Dict], ingress_router: str):
        self.routes = [Route(r['dest'], r.get('next_hop'), r['interface'], r['router']) for r in routes_config]
        self.ingress_router = ingress_router

    def longest_prefix_match(self, dest_ip: str) -> Optional[Route]:
        ip = ipaddress.ip_address(dest_ip)
        candidates = []
        for r in self.routes:
            if ip in r.network:
                candidates.append(r)
        if not candidates:
            return None
        candidates.sort(key=lambda r: r.prefixlen, reverse=True)
        return candidates[0]
