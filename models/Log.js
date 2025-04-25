const mongoose = require("mongoose");

const logSchema = new mongoose.Schema({
  timestamp: { type: Date, default: Date.now },
  ip: { type: String, required: true },
  domain: { type: String, default: "Unknown" },  // New field for domains
  app: { type: String, required: true },
  decision: { type: String, enum: ["allow", "block"], required: true },
  reason: { type: String, default: "No reason provided" },
});

module.exports = mongoose.model("Log", logSchema);
