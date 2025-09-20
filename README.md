# AI-based-Firewall


🔥 AI-Powered Application Firewall

This project is a real-time, AI-driven firewall that monitors and controls network traffic, enforces application-specific policies, and detects anomalies using machine learning.

It is designed to provide fine-grained security, allowing per-application rules, centralized monitoring, and automated blocking of malicious traffic.

🚀 Features

✅ Application-Based Firewall Policies – Restrict IPs, domains, and protocols per application.

✅ Centralized Web Console – Manage firewall rules and monitor logs from a single interface.

✅ Real-time Traffic Monitoring – Track network activity per application in real time.

✅ AI/ML-based Anomaly Detection – Identify suspicious behavior and block malicious traffic.

✅ Windows Compatibility – Fully compatible with Windows endpoints.

🛠️ Tech Stack

Backend: Node.js (Express.js), Python

Frontend: EJS, Tailwind CSS

Database: MongoDB

Firewall Agent: Python (psutil, socket, requests)

AI/ML: Scikit-learn

📂 Project Structure
/firewall-agent       # Python-based firewall agent
   firewall.py        # Monitors and enforces policies
   predict.py         # AI anomaly detection

/models               # MongoDB models (Log, Policy)
/views                # EJS templates for the dashboard
/public               # Static assets (CSS, JS)

server.js             # Express.js backend server
README.html           # Project documentation

🔧 Installation & Setup
1️⃣ Install Dependencies

Make sure you have Python 3.10+, Node.js, and MongoDB installed.

Backend (Node.js Server):

npm install


Firewall Agent (Python):

pip install psutil requests scikit-learn pandas

2️⃣ Run MongoDB Locally
mongod --dbpath /path/to/database

3️⃣ Start the Web Server
node server.js

4️⃣ Run the Firewall Agent
python firewall.py

🖥️ Dashboard & API Endpoints
Web Dashboard

Access the dashboard at:
http://127.0.0.1:5000/dashboard

API Routes
Method	Endpoint	Description
GET	/logs	Get latest firewall logs
GET	/policies	Fetch firewall policies
POST	/policies	Update firewall policies
POST	/predict	AI-based traffic analysis
POST	/log	Log network activity
⚡ How It Works

🔍 The firewall agent monitors active network connections.

📡 It fetches policies from the centralized server.

🚨 If a connection matches blocked rules, it is blocked via Windows Firewall.

📜 The decision (allow/block) is logged in MongoDB.

🤖 AI detects anomalies and blocks suspicious traffic.

🎯 Future Improvements

✅ Per-application firewall rules

✅ Advanced AI model for anomaly detection

✅ Linux support

✅ Real-time alerts via email/Slack
