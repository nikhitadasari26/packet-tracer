
from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Optional, List, Tuple
import os, json

from app.dns import DNSResolver
from app.router import RoutingEngine
from app.firewall import Firewall

app = FastAPI(title="Packet Tracer Simulator")


class TraceRequest(BaseModel):
    src_ip: str
    dst: str
    dst_port: int = Field(..., ge=0, le=65535)
    protocol: str
    ttl: int

CONFIG_PATH = os.environ.get("SCENARIO", "config/scenario-basic.json")

def load_config(path: str):
    with open(path) as f:
        return json.load(f)

cfg = load_config(CONFIG_PATH)

dns = DNSResolver(cfg.get("dns", []))
routing = RoutingEngine(cfg.get("routes", []), cfg.get("Ingress_router"))
firewall = Firewall(cfg.get("firewalls", {}))


# -------- Main Trace Endpoint --------
@app.post("/trace")
def trace(req: TraceRequest):
    trace_steps = []

    # ---- DNS resolution ----
    dst = req.dst
    try:
        import ipaddress
        dest_ip = str(ipaddress.ip_address(dst))  # numeric IP stays unchanged
    except Exception:
        ip, dns_trace = dns.resolve(dst)
        trace_steps.extend(dns_trace)
        if ip is None:
            return trace_steps
        dest_ip = ip

    ttl = req.ttl
    src_ip = req.src_ip
    protocol = req.protocol.upper()
    dst_port = req.dst_port

    hops = 0

    while True:
        hops += 1
        if hops > 30:
            trace_steps.append({"location": "Simulator", "action": "Hop limit exceeded (too many hops)"})
            break

        # ---- routing ----
        route = routing.longest_prefix_match(dest_ip)
        if not route:
            trace_steps.append({"location": "Router", "action": f"No route to host {dest_ip}"})
            break

        router_name = route.router
        ttl -= 1

        trace_steps.append({
            "location": router_name,
            "action": f"Routing lookup matched {str(route.network)} -> next_hop={route.next_hop} via {route.interface}",
            "ttl": ttl
        })

        if ttl <= 0:
            trace_steps.append({"location": router_name, "action": "Time to Live exceeded"})
            break

        # ---- firewall ----
        allowed, rule_idx, reason = firewall.check(router_name, src_ip, protocol, dst_port)
        if not allowed:
            trace_steps.append({"location": router_name, "action": f"Blocked by rule #{rule_idx}: {reason}"})
            break
        else:
            if rule_idx:
                trace_steps.append({"location": router_name, "action": f"Allowed by rule #{rule_idx}: {reason}"})

        # ---- locally delivered host ----
        if route.next_hop is None or route.interface.upper() == "LOCAL":
            trace_steps.append({"location": "Host", "action": f"Delivered to {dest_ip}:{dst_port}"})
            break

        # ---- forward to next hop ----
        trace_steps.append({
            "location": router_name,
            "action": f"Forwarded to {route.next_hop} via {route.interface}",
            "ttl": ttl
        })

    return trace_steps
