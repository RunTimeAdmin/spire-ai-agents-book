# Chapter 2: First Deployment

Production-ready SPIRE deployment configurations from local development to Kubernetes.

## What's Included

- `local/` - Docker Compose setup for local development
- `kubernetes/` - Production-ready Kubernetes manifests

## Quick Start

### Local Development (Docker Compose)

```bash
cd local
docker-compose up -d

# Verify SPIRE server is running
docker-compose exec spire-server spire-server healthcheck

# Verify SPIRE agent is running  
docker-compose exec spire-agent spire-agent healthcheck

# Create a test registration entry
docker-compose exec spire-server \
    spire-server entry create \
    -spiffeID spiffe://example.org/test \
    -parentID spiffe://example.org/spire/agent/x509pop/$(hostname) \
    -selector unix:uid:1000
```

### Kubernetes Deployment

```bash
cd kubernetes

# Create SPIRE namespace
kubectl apply -f spire-namespace.yaml

# Deploy SPIRE server
kubectl apply -f spire-server.yaml

# Deploy SPIRE agent (DaemonSet)
kubectl apply -f spire-agent.yaml

# Verify deployment
kubectl get pods -n spire
kubectl logs -n spire -l app=spire-server
```

## Prerequisites

**For local deployment:**
- Docker 20.10+
- Docker Compose 2.0+

**For Kubernetes deployment:**
- Kubernetes 1.24+
- kubectl configured
- Cluster admin access

## Configuration Files

### Local Setup

**`docker-compose.yml`**
- Complete SPIRE server + agent setup
- Shared Unix socket for workload API
- Persistent storage for server data

**`spire-server.conf`**
- Server configuration
- Trust domain: `example.org`
- SQLite data store (local dev only)

**`spire-agent.conf`**
- Agent configuration
- Join token attestation (local dev)
- Workload API socket: `/tmp/spire-agent/public/api.sock`

### Kubernetes Setup

**`spire-server.yaml`**
- StatefulSet with 1 replica
- ConfigMap for configuration
- PersistentVolume for data
- Service for agent connectivity

**`spire-agent.yaml`**
- DaemonSet (runs on every node)
- Uses Kubernetes PSAT attestation
- HostPath volume for socket

**`spire-namespace.yaml`**
- Creates `spire` namespace
- RBAC configuration for SPIRE

## Testing

### Verify SPIRE Server

```bash
# Local
docker-compose exec spire-server spire-server healthcheck

# Kubernetes
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server healthcheck
```

### Verify SPIRE Agent

```bash
# Local
docker-compose exec spire-agent spire-agent healthcheck

# Kubernetes
AGENT_POD=$(kubectl get pods -n spire -l app=spire-agent -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n spire $AGENT_POD -- \
    /opt/spire/bin/spire-agent healthcheck
```

### Create Test Registration Entry

```bash
# Kubernetes example
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server entry create \
    -spiffeID spiffe://example.org/test-workload \
    -parentID spiffe://example.org/spire/agent/k8s_psat/demo-cluster/default \
    -selector k8s:ns:default \
    -selector k8s:sa:default
```

## Troubleshooting

### SPIRE Server Won't Start

```bash
# Check logs
kubectl logs -n spire spire-server-0

# Common issues:
# - Database not accessible
# - Invalid configuration
# - Insufficient permissions
```

### SPIRE Agent Can't Connect

```bash
# Check agent logs
kubectl logs -n spire -l app=spire-agent

# Verify server service
kubectl get svc -n spire spire-server

# Test connectivity
kubectl exec -n spire $AGENT_POD -- \
    nc -zv spire-server.spire.svc.cluster.local 8081
```

### Workload Can't Fetch SVID

```bash
# Verify registration entry exists
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server entry show

# Check agent has attested
kubectl exec -n spire $AGENT_POD -- \
    /opt/spire/bin/spire-agent api fetch
```

## Next Steps

After completing this chapter:

1. **Chapter 3:** Integrate your first AI agent with SPIRE
2. **Chapter 4:** Set up production high availability
3. **Chapter 6:** Configure audit logging for compliance

## Related Book Sections

- **Chapter 2.1:** Local Development Setup (page XX)
- **Chapter 2.2:** Kubernetes Deployment (page XX)
- **Chapter 2.3:** First Registration Entry (page XX)
- **Chapter 2.4:** Troubleshooting Common Issues (page XX)

## Support

Questions about this chapter? 

- [Open an issue](https://github.com/runtimefence/spire-ai-agents-book/issues)
- Reference: Chapter 2 in the book
- SPIRE Docs: https://spiffe.io/docs/latest/spire/
