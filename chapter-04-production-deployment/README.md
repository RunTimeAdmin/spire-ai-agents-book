# Chapter 4: Production Deployment

Production-ready SPIRE deployment with high availability, monitoring, and backup/recovery.

## What's Included

- `high-availability/` - HA SPIRE server with PostgreSQL
- `monitoring/` - Prometheus metrics and Grafana dashboards
- `backup/` - Backup and restore procedures

## Architecture

```
                    ┌──────────────────┐
                    │   PostgreSQL     │
                    │   (HA cluster)   │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐       ┌────▼─────┐       ┌────▼─────┐
    │  SPIRE   │       │  SPIRE   │       │  SPIRE   │
    │ Server 1 │       │ Server 2 │       │ Server 3 │
    └────┬─────┘       └────┬─────┘       └────┬─────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼─────────┐
                    │   Load Balancer  │
                    │   (Service)      │
                    └────────┬─────────┘
                             │
                      SPIRE Agents
```

## Prerequisites

- Kubernetes 1.24+
- 3+ nodes (for HA)
- Storage class for PersistentVolumes
- Helm 3+ (optional, for PostgreSQL)

## Quick Start

```bash
cd high-availability

# Deploy PostgreSQL
kubectl apply -f postgresql-ha.yaml

# Deploy HA SPIRE server (3 replicas)
kubectl apply -f spire-server-ha.yaml

# Verify deployment
kubectl get pods -n spire
kubectl get statefulset -n spire

# Check all servers are healthy
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server healthcheck
kubectl exec -n spire spire-server-1 -- \
    /opt/spire/bin/spire-server healthcheck
kubectl exec -n spire spire-server-2 -- \
    /opt/spire/bin/spire-server healthcheck
```

## Features

### High Availability
- 3 SPIRE server replicas
- Shared PostgreSQL database
- Session affinity for gRPC
- Survives single server failure

### Scalability
- PostgreSQL instead of SQLite
- Handles 1000+ concurrent agents
- Connection pooling
- Registration entry caching

### Observability
- Prometheus metrics
- Grafana dashboards
- Health check endpoints
- Structured logging

### Performance
- Sub-second attestation
- <100ms SVID fetch
- mTLS connection reuse
- Optimized database queries

## Monitoring

```bash
cd monitoring

# Deploy Prometheus ServiceMonitor
kubectl apply -f prometheus-servicemonitor.yaml

# Import Grafana dashboard
kubectl apply -f grafana-dashboard.json

# View metrics
kubectl port-forward -n monitoring svc/grafana 3000:80
# Open http://localhost:3000
```

### Key Metrics to Watch

**SPIRE Server:**
- `spire_server_ca_manager_x509_ca_rotate_total` - CA rotations
- `spire_server_svid_issued_total` - SVIDs issued
- `spire_server_api_latency_seconds` - API response time

**Database:**
- Connection pool utilization
- Query duration
- Failed queries

## Backup & Recovery

```bash
cd backup

# Manual backup
./backup-spire.sh

# Automated backup (CronJob)
kubectl apply -f backup-cronjob.yaml

# Restore from backup
./restore-spire.sh <backup-file>
```

## Production Checklist

**Before deploying to production:**

- [ ] Use managed database (RDS, Cloud SQL, not in-cluster PostgreSQL)
- [ ] Configure database backups (automated, tested)
- [ ] Set up monitoring alerts (Prometheus AlertManager)
- [ ] Test failover scenarios (kill server pod, verify no downtime)
- [ ] Configure resource limits (CPU, memory)
- [ ] Enable audit logging (Chapter 6)
- [ ] Document runbooks (incident response)
- [ ] Test backup/restore procedures

## Troubleshooting

### All SPIRE servers show "database connection failed"

```bash
# Check PostgreSQL is running
kubectl get pods -n spire -l app=postgres

# Check database connectivity
kubectl exec -n spire spire-server-0 -- \
    nc -zv postgres.spire.svc.cluster.local 5432

# Check credentials
kubectl get secret -n spire postgres-credentials -o yaml
```

### SVID issuance slow (>1 second)

```bash
# Check database performance
kubectl top pod -n spire -l app=postgres

# Check for connection pool exhaustion
kubectl logs -n spire spire-server-0 | grep "connection pool"

# Increase database resources
kubectl edit statefulset -n spire postgres
```

### One server unhealthy, others healthy

```bash
# Check specific server logs
kubectl logs -n spire spire-server-1

# Common issues:
# - Data directory corruption
# - Network partition
# - Resource limits hit

# Restart unhealthy server
kubectl delete pod -n spire spire-server-1
```

## Performance Tuning

For 1000+ agents, tune these settings:

**PostgreSQL:**
```sql
-- /high-availability/postgres-tuning.sql
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '1GB';
ALTER SYSTEM SET effective_cache_size = '3GB';
```

**SPIRE Server:**
```hcl
# Increase connection pool
DataStore "sql" {
    plugin_data {
        max_open_conns = 50
        max_idle_conns = 25
    }
}
```

## Next Steps

After completing this chapter:

1. **Chapter 5:** Multi-cloud federation
2. **Chapter 6:** Add audit logging and compliance
3. **Chapter 9:** Troubleshooting production issues

## Related Book Sections

- **Chapter 4.1:** PostgreSQL Setup (page XX)
- **Chapter 4.2:** HA SPIRE Server (page XX)
- **Chapter 4.3:** Monitoring and Alerting (page XX)
- **Chapter 4.4:** Backup and Recovery (page XX)

## Support

Questions? [Open an issue](https://github.com/RunTimeAdmin/spire-ai-agents-book/issues)
