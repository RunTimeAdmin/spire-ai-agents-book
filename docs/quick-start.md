# Quick Start Guide

Get SPIRE + AI agents running in 15 minutes.

## Prerequisites

- **Kubernetes cluster** (1.24+) OR **Docker** (20.10+)
- **kubectl** configured (for K8s)
- **Python** 3.9+ (for AI agents)

## Option 1: Local with Docker (Fastest)

```bash
# Clone repo
git clone https://github.com/runtimefence/spire-ai-agents-book.git
cd spire-ai-agents-book

# Start SPIRE
cd chapter-02-first-deployment/local
docker-compose up -d

# Verify
docker-compose exec spire-server spire-server healthcheck
# Output: Server is healthy

# Run simple AI agent
cd ../../chapter-03-ai-agent-integration/langchain
pip install -r requirements.txt
python simple_agent.py
# Output: My SPIFFE ID: spiffe://example.org/...
```

**Time:** ~5 minutes

## Option 2: Kubernetes (Production-Ready)

```bash
# Clone repo
git clone https://github.com/runtimefence/spire-ai-agents-book.git
cd spire-ai-agents-book/chapter-02-first-deployment/kubernetes

# Deploy SPIRE
kubectl apply -f spire-namespace.yaml
kubectl apply -f spire-server.yaml
kubectl apply -f spire-agent.yaml

# Wait for pods
kubectl wait --for=condition=ready pod -l app=spire-server -n spire --timeout=300s
kubectl wait --for=condition=ready pod -l app=spire-agent -n spire --timeout=300s

# Verify
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server healthcheck
# Output: Server is healthy
```

**Time:** ~10 minutes

## What You Get

After completing quick start:

✅ SPIRE server running  
✅ SPIRE agent running  
✅ Workload API accessible  
✅ Ready to integrate AI agents  

## Next Steps

### 1. Create Your First Registration Entry

```bash
# For Kubernetes
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server entry create \
    -spiffeID spiffe://example.org/myapp \
    -parentID spiffe://example.org/spire/agent/k8s_psat/demo-cluster/default \
    -selector k8s:ns:default \
    -selector k8s:sa:default

# For Docker
docker-compose exec spire-server \
    spire-server entry create \
    -spiffeID spiffe://example.org/myapp \
    -parentID spiffe://example.org/spire/agent/x509pop/$(hostname) \
    -selector unix:uid:1000
```

### 2. Run AI Agent Example

```bash
cd chapter-03-ai-agent-integration/langchain
pip install -r requirements.txt
python simple_agent.py
```

### 3. Explore More Examples

- **Chapter 4:** Production deployment with HA
- **Chapter 6:** Add compliance audit logging
- **Chapter 8:** Advanced framework integration
- **Chapter 9:** Troubleshooting tools

## Common Issues

### "Connection refused" to SPIRE server

```bash
# Check server is running
kubectl get pods -n spire -l app=spire-server
# or
docker ps | grep spire-server

# Check logs
kubectl logs -n spire spire-server-0
# or
docker logs spire-server
```

### "No such file or directory" for socket

```bash
# Verify agent socket exists
ls -la /tmp/spire-agent/public/api.sock  # Docker
# or check pod mount
kubectl exec -n spire <agent-pod> -- ls -la /run/spire/agent/sockets/
```

### "No registration entry found"

You need to create a registration entry (see step 1 above).

## Getting Help

- **Issues:** https://github.com/runtimefence/spire-ai-agents-book/issues
- **SPIRE Docs:** https://spiffe.io/docs/latest/spire/
- **SPIRE Slack:** https://slack.spiffe.io
- **Book:** Get full context at [Amazon](https://amazon.com/dp/YOUR_ASIN_HERE)

## What's Next?

This quick start gets you running. For production:

1. **Read Chapter 4** - High availability setup
2. **Read Chapter 6** - Security and compliance
3. **Read Chapter 9** - Troubleshooting and monitoring

The book provides full context, best practices, and production patterns.

---

**Quick start complete!** You now have SPIRE running and can integrate AI agents.
