const express = require("express");
const { PythonShell } = require("python-shell");
const mongoose = require("mongoose");
const path = require("path");
const cors = require("cors");

const Log = require("./models/Log");
const Policy = require("./models/Policy"); // Import Policy Model

const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.json());
app.use(cors()); // Allow frontend to access API

mongoose.connect("mongodb://127.0.0.1:27017/firewall_logs", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => console.log("✅ Connected to MongoDB"))
  .catch(err => console.error("❌ MongoDB Connection Error:", err));

// 🔥 **Dashboard Route**
app.get("/dashboard", async (req, res) => {
  try {
    const logs = await Log.find().sort({ timestamp: -1 }).limit(50);
    res.render("dashboard", { logs });
  } catch (error) {
    console.error("❌ Error fetching logs:", error);
    res.status(500).send("Failed to load dashboard");
  }
});

// 🔥 **AI Traffic Prediction (`/predict`)**
app.post("/predict", async (req, res) => {
  const { ip, app, packet_size, request_frequency, port } = req.body;

  if (!ip || !packet_size || !request_frequency || !port) {
    return res.status(400).json({ error: "Missing required parameters" });
  }

  let options = {
    mode: "json",
    pythonPath: "python",
    scriptPath: "./",
    args: [packet_size, request_frequency, port],
  };

  PythonShell.run("predict.py", options)
    .then(async (results) => {
      const prediction = results[0]?.prediction; // 1 = block, 0 = allow

      if (prediction === undefined) {
        throw new Error("Invalid ML model output");
      }

      const decision = prediction === "1" ? "block" : "allow";
      const logEntry = new Log({
        ip,
        app: app || "Unknown",
        decision,
        reason: decision === "block" ? "Suspicious traffic detected" : "Normal traffic",
      });

      await logEntry.save();
      res.json({ message: `Traffic ${decision}`, decision, ip, app });
    })
    .catch((err) => {
      console.error("❌ Python Error:", err);
      res.status(500).json({ error: "Internal Server Error" });
    });
});

// 🔥 **Log Incoming Traffic (`/log`)**
app.post("/log", async (req, res) => {
  console.log("📥 Incoming Log Data:", req.body);

  const { ip, app, domain, decision, reason } = req.body;

  if (!ip || !decision) {
    return res.status(400).json({ error: "Missing parameters" });
  }

  try {
    const logEntry = new Log({
      ip,
      app: app || "Unknown",
      domain: domain || "Unknown",
      decision,
      reason: reason || "No reason provided",
    });

    await logEntry.save();
    console.log("✅ Log saved to DB:", logEntry);
    
    res.json({ message: "Log received", ip, app, domain, decision });
  } catch (err) {
    console.error("❌ Error saving log:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// 🔥 **Get Logs (`/logs`)**
app.get("/logs", async (req, res) => {
  try {
    const logs = await Log.find().sort({ timestamp: -1 }).limit(50);
    res.json(logs);
  } catch (error) {
    console.error("❌ Error fetching logs:", error);
    res.status(500).json({ error: "Failed to retrieve logs" });
  }
});

// 🔥 **Get Firewall Policies (`/policies`)**
app.get("/policies", async (req, res) => {
  try {
    let policy = await Policy.findOne();
    if (!policy) {
      policy = new Policy({ blocked_ips: [], blocked_domains: [], blocked_protocols: [] });
      await policy.save();
    }
    res.json(policy);
  } catch (err) {
    console.error("❌ Error fetching policies:", err);
    res.status(500).json({ error: "Failed to retrieve firewall policies" });
  }
});

// 🔥 **Update Firewall Policies (`/policies`)**
app.post("/policies", async (req, res) => {
  try {
    const { blocked_ips, blocked_domains, blocked_protocols } = req.body;

    let policy = await Policy.findOne();
    if (!policy) {
      policy = new Policy({ blocked_ips: [], blocked_domains: [], blocked_protocols: [] });
    }

    if (blocked_ips) policy.blocked_ips = blocked_ips;
    if (blocked_domains) policy.blocked_domains = blocked_domains;
    if (blocked_protocols) policy.blocked_protocols = blocked_protocols;

    await policy.save();
    res.json({ message: "Firewall policies updated", policy });
  } catch (err) {
    console.error("❌ Error updating policies:", err);
    res.status(500).json({ error: "Failed to update firewall policies" });
  }
});

// 🚀 **Start Server**
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`🔥 Server running on http://127.0.0.1:${PORT}`);
});
