const express = require("express");
const Policy = require("../models/Policy");

const router = express.Router();

// Get firewall policies
router.get("/", async (req, res) => {
    try {
        let policy = await Policy.findOne();
        if (!policy) {
            policy = new Policy();
            await policy.save();
        }
        res.json(policy);
    } catch (err) {
        res.status(500).json({ error: "Server error" });
    }
});

// Update firewall policies
router.post("/", async (req, res) => {
    try {
        const { blocked_ips, blocked_domains, blocked_protocols } = req.body;

        let policy = await Policy.findOne();
        if (!policy) {
            policy = new Policy();
        }

        if (blocked_ips) policy.blocked_ips = blocked_ips;
        if (blocked_domains) policy.blocked_domains = blocked_domains;
        if (blocked_protocols) policy.blocked_protocols = blocked_protocols;

        await policy.save();
        res.json({ message: "Firewall policies updated", policy });
    } catch (err) {
        res.status(500).json({ error: "Server error" });
    }
});

module.exports = router;
