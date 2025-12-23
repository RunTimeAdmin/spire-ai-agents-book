# Chapter 3: AI Agent Integration

Integrate AI agents with SPIRE for authenticated API access.

## What's Included

- `langchain/` - LangChain agent with SPIRE authentication
- `kubernetes/` - Kubernetes deployments for AI agents

## Quick Start

```bash
cd langchain

# Install dependencies
pip install -r requirements.txt

# Run simple agent (requires SPIRE running)
python simple_agent.py
```

## Prerequisites

- SPIRE deployed (see Chapter 2)
- Python 3.9+
- OpenAI API key (for LangChain examples)

## Examples

### 1. Simple SPIRE Client

`simple_agent.py` - Basic example of fetching SVID from SPIRE agent

```bash
python simple_agent.py
# Output: My SPIFFE ID: spiffe://example.org/ai-agent/simple
```

### 2. LangChain with SPIRE

`langchain_spire_agent.py` - LangChain agent that uses SPIRE for API authentication

```bash
export OPENAI_API_KEY=your-key-here
python langchain_spire_agent.py
```

## File Descriptions

**`requirements.txt`**
- Python dependencies
- pyspiffe for SPIRE integration
- langchain and openai for AI

**`simple_agent.py`**
- Minimal example
- Fetches SVID from SPIRE agent
- Displays SPIFFE ID

**`spire_integration.py`**
- Reusable SPIRE client wrapper
- Automatic SVID rotation
- mTLS helper functions

**`langchain_spire_agent.py`**
- Complete LangChain agent
- Uses SPIRE for tool authentication
- Example: Calling authenticated APIs

## Kubernetes Deployment

```bash
cd kubernetes

# Deploy AI agent with SPIRE integration
kubectl apply -f ai-agent-deployment.yaml

# Check logs
kubectl logs -f deployment/ai-agent
```

## Testing

### Test SVID Fetch

```bash
python simple_agent.py

# Expected output:
# ✅ SPIRE client initialized
# My SPIFFE ID: spiffe://example.org/ai-agent/simple
# Certificate expires: 2025-01-15 10:30:00 UTC
```

### Test Authenticated API Call

```bash
# Requires API server running (see book Chapter 3.4)
python test_authenticated_call.py

# Expected: 200 OK response with data
```

## Troubleshooting

### Error: "No SPIFFE workload API socket"

```bash
# Check SPIRE agent socket exists
ls -la /tmp/spire-agent/public/api.sock

# If missing, check SPIRE agent is running
kubectl get pods -n spire -l app=spire-agent
```

### Error: "No registration entry found"

```bash
# Create registration entry for AI agent
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server entry create \
    -spiffeID spiffe://example.org/ai-agent/simple \
    -parentID spiffe://example.org/spire/agent/k8s_psat/demo-cluster/default \
    -selector k8s:ns:default \
    -selector k8s:sa:ai-agent
```

### Error: "Certificate expired"

SVID automatically rotates. If this persists:

```bash
# Check SPIRE agent health
kubectl exec -n spire <agent-pod> -- \
    /opt/spire/bin/spire-agent healthcheck

# Force new SVID fetch
kubectl delete pod <ai-agent-pod>
```

## Architecture

```
┌─────────────────────┐
│   AI Agent (Pod)    │
│                     │
│  ┌──────────────┐  │
│  │ LangChain    │  │
│  │ Agent        │  │
│  └──────┬───────┘  │
│         │          │
│  ┌──────▼───────┐  │
│  │ SPIRE Client │──┼─── Fetch SVID ──→ SPIRE Agent (Socket)
│  └──────┬───────┘  │
│         │          │
│  ┌──────▼───────┐  │
│  │ API Call     │  │
│  │ (with mTLS)  │  │
│  └──────────────┘  │
└──────────┬──────────┘
           │
           │ mTLS (authenticated with SVID)
           ▼
   ┌────────────────┐
   │ API Server     │
   │ (validates     │
   │  SPIFFE ID)    │
   └────────────────┘
```

## Next Steps

After completing this chapter:

1. **Chapter 4:** Deploy to production with HA
2. **Chapter 6:** Add audit logging
3. **Chapter 8:** Advanced framework integration

## Related Book Sections

- **Chapter 3.1:** SPIRE Python Client (page XX)
- **Chapter 3.2:** LangChain Integration (page XX)
- **Chapter 3.3:** Agent Authentication Patterns (page XX)
- **Chapter 3.4:** Troubleshooting Integration (page XX)

## Support

Questions? [Open an issue](https://github.com/runtimefence/spire-ai-agents-book/issues)
