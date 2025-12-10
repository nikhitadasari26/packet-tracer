# app/firewall.py
from typing import Dict, List, Optional, Tuple
import ipaddress

def port_in_range(port: int, pr: str) -> bool:
    if "-" in pr:
        a,b = pr.split("-",1)
        return int(a) <= port <= int(b)
    return int(pr) == port

class Firewall:
    def __init__(self, fw_config: Dict[str, List[Dict]]):
        self.fw = fw_config or {}

    def check(self, router_name: str, src_ip: str, protocol: str, dst_port: int) -> Tuple[bool, Optional[int], Optional[str]]:
        rules = self.fw.get(router_name, [])
        proto = protocol.upper()
        src_addr = ipaddress.ip_address(src_ip)
        for idx, r in enumerate(rules, start=1):
            rproto = r.get('protocol', '*').upper()
            if rproto != '*' and rproto != proto:
                continue
            try:
                net = ipaddress.ip_network(r['src'])
            except Exception:
                net = ipaddress.ip_network(r['src'] + '/32')
            if src_addr in net:
                if r.get('dst_port') is None:
                    matched = True
                else:
                    if port_in_range(dst_port, str(r['dst_port'])):
                        matched = True
                    else:
                        matched = False
                if matched:
                    if r['action'].lower() == 'allow':
                        return True, idx, f"Allowed by rule #{idx}"
                    else:
                        return False, idx, f"Blocked by rule #{idx}"
        return True, None, "No matching rule, allowed by default"
