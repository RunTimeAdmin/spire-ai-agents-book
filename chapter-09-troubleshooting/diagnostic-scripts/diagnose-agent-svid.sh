#!/bin/bash
# diagnose-agent-svid.sh
# Diagnoses why a SPIRE agent cannot fetch SVID

set -e

echo "🔍 Diagnosing SVID fetch failure..."
echo ""

# Step 1: Is SPIRE agent running?
echo "Step 1: Check SPIRE agent status"
kubectl get pods -n spire -l app=spire-agent

AGENT_POD=$(kubectl get pods -n spire -l app=spire-agent -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -z "$AGENT_POD" ]; then
    echo "❌ SPIRE agent pod not found"
    echo ""
    echo "Possible causes:"
    echo "  - SPIRE agent DaemonSet not deployed"
    echo "  - Agent pod crashed (check: kubectl get pods -n spire)"
    echo "  - Wrong namespace (check: kubectl get ns)"
    exit 1
fi

echo "✅ Agent pod running: $AGENT_POD"
echo ""

# Step 2: Check agent logs for errors
echo "Step 2: Check agent logs for errors"
kubectl logs -n spire $AGENT_POD --tail=50 | grep -i error || echo "No errors in recent logs"
echo ""

# Step 3: Can agent reach SPIRE server?
echo "Step 3: Test connectivity to SPIRE server"
kubectl exec -n spire $AGENT_POD -- nc -zv spire-server.spire.svc.cluster.local 8081

if [ $? -ne 0 ]; then
    echo "❌ Agent cannot reach SPIRE server"
    echo ""
    echo "Possible causes:"
    echo "  - NetworkPolicy blocking traffic"
    echo "  - SPIRE server not running"
    echo "  - DNS resolution failure"
    echo ""
    echo "Debug commands:"
    echo "  kubectl get networkpolicies -n spire"
    echo "  kubectl get svc -n spire spire-server"
    echo "  kubectl exec -n spire $AGENT_POD -- nslookup spire-server.spire.svc.cluster.local"
    exit 1
fi

echo "✅ Agent can reach SPIRE server"
echo ""

# Step 4: Check agent's attestation status
echo "Step 4: Check agent attestation"
kubectl exec -n spire $AGENT_POD -- \
    /opt/spire/bin/spire-agent api fetch -socketPath /run/spire/agent/sockets/api.sock 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Agent not attested"
    echo ""
    echo "Fix: Force agent re-attestation"
    echo "  kubectl delete pod -n spire $AGENT_POD"
    echo ""
    echo "Check SPIRE server logs for attestation errors:"
    echo "  kubectl logs -n spire spire-server-0 | grep attest"
    exit 1
fi

echo "✅ Agent successfully attested"
echo ""

# Step 5: Check for registration entries
echo "Step 5: Check registration entries"
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server entry show -socketPath /run/spire/server/sockets/api.sock | head -20

echo ""
echo "✅ Diagnosis complete!"
echo ""
echo "If agent still can't fetch SVID, check:"
echo "  1. Registration entry exists for workload"
echo "  2. Selectors match workload attributes"
echo "  3. SPIFFE ID is correctly formatted"
