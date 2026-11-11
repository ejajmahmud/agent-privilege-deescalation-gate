"""CLI for agent-privilege-deescalation-gate."""
import sys
import argparse
from .gate import PrivilegeGate

def main():
    parser = argparse.ArgumentParser(description="Agent Privilege De-escalation Gate CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate JIT privilege lifecycle")
    args = parser.parse_args()

    if args.demo:
        gate = PrivilegeGate(default_ttl_s=10)
        lease = gate.grant_lease("agent_worker", ["db:write", "fs:delete"])
        print(f"Granted Lease {lease.lease_id}: {lease.scopes}")
        print(f"Has db:write: {gate.has_privilege(lease.lease_id, 'db:write')}")
        gate.deescalate(lease.lease_id)
        print(f"After deescalate, has db:write: {gate.has_privilege(lease.lease_id, 'db:write')}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
