# Packet Tracer Simulator (API-Based Networking Project)

This project simulates how a network packet travels through a virtual network.  
It models DNS resolution, routing (longest prefix match), TTL handling, and firewall rules.

---

## 1. Setup Instructions

### Install dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

### Run with default BASIC scenario
```powershell
uvicorn app.main:app --reload --port 8000
```

### Run with COMPLEX scenario
```powershell
$env:SCENARIO = "config/scenario-complex.json"
uvicorn app.main:app --reload --port 8000
```

---

## 2. POST /trace API

### Endpoint
```
POST /trace
```

### Request Body Example
```json
{
  "src_ip": "192.168.2.10",
  "dst": "example.com",
  "dst_port": 80,
  "protocol": "TCP",
  "ttl": 5
}
```

---

## Successful Trace Example
```json
[
  {
    "location": "DNS Resolver",
    "action": "Resolved example.com -> 10.0.5.12"
  },
  {
    "location": "Router-B",
    "action": "Routing lookup matched 10.0.5.0/24 -> next_hop=None via LOCAL",
    "ttl": 4
  },
  {
    "location": "Host",
    "action": "Delivered to 10.0.5.12:80"
  }
]
```

---

## Firewall Block Example
```json
[
  {"location": "DNS Resolver", "action": "Resolved blocked.example -> 10.1.5.12"},
  {"location": "Edge-Router", "action": "Routing lookup matched 0.0.0.0/0 -> next_hop=10.254.1.1 via eth0", "ttl": 4},
  {"location": "Edge-Router", "action": "Blocked by rule #1"}
]
```

---

## 3. Configuration Scenarios

Configuration files inside `config/`:

### scenario-basic.json
- DNS A records  
- Basic routing  
- Single allow firewall rule  

### scenario-complex.json
- A + CNAME resolution  
- Overlapping routes  
- Allow + deny firewall rules  
- TTL behavior  

To switch:
```powershell
$env:SCENARIO = "config/scenario-complex.json"
```

---

## 4. Demo Evidence

All demo files are stored in:

```
demo/
 ├── demo_success.json
 ├── demo_nxdomain.json
 ├── demo_ttl.json
 ├── demo_blocked.json
 └── screenshots/
```

---

## 5. Project Structure
```
packet-tracer/
│ README.md
│ SUBMISSION.md
│ requirements.txt
│
├── app/
│   ├── dns.py
│   ├── router.py
│   ├── firewall.py
│   └── main.py
│
├── config/
│   ├── scenario-basic.json
│   └── scenario-complex.json
│
└── demo/
    └── screenshots/
```

---

## 6. Notes

- DNS supports A + CNAME  
- Routing uses Longest Prefix Match  
- TTL decreases per hop  
- Firewall rules process top → bottom  
- Simulation ends when:
  - Delivered  
  - Blocked  
  - TTL expired  
  - No route  
  - NXDOMAIN
