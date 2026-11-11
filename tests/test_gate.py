"""Unit tests for agent-privilege-deescalation-gate."""
import time
import unittest
from agent_privilege_deescalation_gate.gate import PrivilegeGate

class TestPrivilegeGate(unittest.TestCase):
    def setUp(self):
        self.gate = PrivilegeGate(default_ttl_s=1.0)

    def test_grant_and_deescalate(self):
        l = self.gate.grant_lease("agentA", ["admin"])
        self.assertTrue(self.gate.has_privilege(l.lease_id, "admin"))
        self.gate.deescalate(l.lease_id)
        self.assertFalse(self.gate.has_privilege(l.lease_id, "admin"))

    def test_ttl_expiration(self):
        l = self.gate.grant_lease("agentB", ["write"], ttl_s=0.1)
        time.sleep(0.15)
        self.assertFalse(self.gate.has_privilege(l.lease_id, "write"))
