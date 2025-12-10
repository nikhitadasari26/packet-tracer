# Submission – Packet Tracer Simulator

**GitHub Repository:**  
https://github.com/nikhitadasari26/packet-tracer

---

## 1. Project Description
This project implements a Packet Tracer–style network simulation API using FastAPI.

It includes:
- DNS Resolution (A + CNAME)
- Longest Prefix Match Routing
- Firewall Allow/Deny Rules (first-match)
- TTL decrement on each hop
- All required outcomes:
  - Delivered  
  - Blocked  
  - NXDOMAIN  
  - No Route  
  - TTL Expired  

---

## 2. How to Run the Project

### **Basic Scenario (default)**  
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### **Complex Scenario**  
```powershell
$env:SCENARIO = "config/scenario-complex.json"
uvicorn app.main:app --reload --port 8000
```

---

## 3. API Documentation

### **Endpoint**
```
POST /trace
```

### **Example Request**
```json
{
  "src_ip": "192.168.2.10",
  "dst": "example.com",
  "dst_port": 80,
  "protocol": "TCP",
  "ttl": 5
}
```

### **Example Successful Response**
```json
[
  { "location": "DNS Resolver", "action": "Resolved example.com -> 10.0.5.12" },
  { "location": "Router-B", "action": "Routing lookup matched 10.0.5.0/24 -> next_hop=None via LOCAL", "ttl": 4 },
  { "location": "Host", "action": "Delivered to 10.0.5.12:80" }
]
```

---

## 4. Demo Evidence

All required demo artifacts are stored in:

```
demo/
 ├── demo_success.json
 ├── demo_nxdomain.json
 ├── demo_ttl.json
 ├── demo_blocked.json
 └── screenshots/
      ├── project_structure.png
      ├── config_folder.png
      ├── success_trace.png
      ├── blocked_trace.png
      ├── ttl_trace.png
      └── nxdomain_trace.png
```

(Optional) Video demo is stored as:
```
demo/video.mp4
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
    ├── *.json
    └── screenshots/
```

---

## 6. Notes for Graders
- DNS supports A + CNAME  
- Routing uses Longest Prefix Match (CIDR)  
- Firewall processed top → bottom (first match wins)  
- TTL decreases per hop  
- Simulation ends when:
  - Delivered  
  - Blocked  
  - NXDOMAIN  
  - No route  
  - TTL expired  

---

# ✔ End of Submission
Everything required for evaluation is included in this repository.
