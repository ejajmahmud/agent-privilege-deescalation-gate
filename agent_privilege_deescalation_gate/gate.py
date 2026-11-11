"""Core Privilege De-escalation Gate implementation."""
import time
import uuid
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

@dataclass
class PrivilegeLease:
    lease_id: str
    agent_id: str
    scopes: Set[str]
    expires_at: float
    is_active: bool = True

class PrivilegeGate:
    """Provisions just-in-time micro-privilege leases and revokes them immediately upon completion."""
    
    def __init__(self, default_ttl_s: float = 60.0):
        self.default_ttl = default_ttl_s
        self.active_leases: Dict[str, PrivilegeLease] = {}

    def grant_lease(self, agent_id: str, scopes: List[str], ttl_s: Optional[float] = None) -> PrivilegeLease:
        lid = f"lease_{uuid.uuid4().hex[:10]}"
        dur = ttl_s or self.default_ttl
        lease = PrivilegeLease(
            lease_id=lid,
            agent_id=agent_id,
            scopes=set(scopes),
            expires_at=time.time() + dur,
            is_active=True
        )
        self.active_leases[lid] = lease
        return lease

    def has_privilege(self, lease_id: str, required_scope: str) -> bool:
        lease = self.active_leases.get(lease_id)
        if not lease or not lease.is_active:
            return False
        if time.time() > lease.expires_at:
            lease.is_active = False
            return False
        return required_scope in lease.scopes

    def deescalate(self, lease_id: str) -> bool:
        """Explicitly and immediately revokes all granted privileges."""
        lease = self.active_leases.get(lease_id)
        if lease and lease.is_active:
            lease.is_active = False
            lease.scopes.clear()
            return True
        return False
