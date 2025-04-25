const mongoose = require("mongoose");

const policySchema = new mongoose.Schema({
  blocked_ips: [String],
  blocked_domains: [String],
  blocked_protocols: [String],
});

const Policy = mongoose.model("Policy", policySchema);
module.exports = Policy;
