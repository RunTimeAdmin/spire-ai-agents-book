# Chapter 9: Troubleshooting Guide

Diagnostic scripts and solutions for common SPIRE production issues.

## What's Included

- `diagnostic-scripts/` - Shell scripts for diagnosing problems
- `common-issues/` - Solutions to frequent problems
- `war-stories/` - Real production incidents and fixes

## Quick Diagnosis

### Problem: AI Agent Can't Fetch SVID

```bash
cd diagnostic-scripts
./diagnose-agent-svid.sh
```

### Problem: Certificate Expired / Rotation Failed

```bash
./diagnose-cert-expiry.sh
```

### Problem: mTLS Connection Failures

```bash
./diagnose-mtls.sh
```

### Problem: Everything is Broken

```bash
./ultimate-diagnostic.sh
```

## The 5-Layer Diagnostic Stack

Always diagnose top-down:

```
Layer 5: Application (AI Agent)
    ↓ Check: Can agent fetch SVID?
    
Layer 4: SPIRE Agent
    ↓ Check: Can agent reach SPIRE server?
    
Layer 3: Network
    ↓ Check: Is SPIRE server running?
    
Layer 2: SPIRE Server
    ↓ Check: Is database reachable?
    
Layer 1: Data Store
    ✓ Fix: Restore database connection
```

## Common Problems

### 1. Agent Can't Fetch SVID

**Symptoms:**
```
spire-agent: ERROR: failed to fetch SVID
workload: FATAL: no SPIFFE ID available
```

**Diagnostic:**
```bash
./diagnose-agent-svid.sh
```

**Common Causes:**
- Agent not attested
- No registration entry
- Network connectivity issues
- SPIRE server down

### 2. Certificate Expired

**Symptoms:**
```
workload: ERROR: certificate expired
api-server: ERROR: x509: certificate has expired
```

**Diagnostic:**
```bash
./diagnose-cert-expiry.sh
```

**Common Causes:**
- SPIRE server overloaded
- Network partition during rotation
- Clock skew
- Database issues preventing rotation

### 3. mTLS Connection Failures

**Symptoms:**
```
workload: ERROR: tls: bad certificate
api-server: ERROR: remote error: tls: unknown certificate authority
```

**Diagnostic:**
```bash
./diagnose-mtls.sh
```

**Common Causes:**
- Trust bundle mismatch
- Expired server certificate
- Wrong certificate used
- SNI mismatch

### 4. Authorization Failures

**Symptoms:**
```
workload: ERROR: 403 Forbidden
api-server: WARN: Rejected request from spiffe://example.org/unknown
```

**Diagnostic:**
```bash
./diagnose-authorization.sh
```

**Common Causes:**
- SPIFFE ID not in allow list
- Wrong SPIFFE ID assigned
- Authorization policy not loaded

## Production War Stories

### The Midnight Certificate Apocalypse

**What happened:**
All certificates expired simultaneously at 2 AM. 

**Root cause:**
Database disk full → SPIRE server couldn't write new certs → all agents missed rotation.

**Fix:**
```bash
# Immediate fix: Increase PVC size
kubectl edit pvc -n spire postgres-data

# Long-term fix: Monitor disk at 80%
# Alert before it fills up
```

**Lesson:** Always monitor database disk space.

### The Registration Entry Explosion

**What happened:**
127,000 registration entries. SPIRE server took 45 seconds to respond.

**Root cause:**
Pod restarts created new entries (selectors included pod name).

**Fix:**
```bash
# Delete duplicate entries
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server entry delete -entryID <duplicate-id>

# Use stable selectors (service account, not pod name)
```

**Lesson:** Use stable selectors. Monitor entry count.

## Diagnostic Scripts

All scripts require:
- `kubectl` configured
- Access to `spire` namespace
- SPIRE deployed in cluster

### diagnose-agent-svid.sh

Checks why agent can't fetch SVID:
1. Agent pod running?
2. Agent logs show errors?
3. Can reach SPIRE server?
4. Agent attested?
5. Registration entries exist?

### diagnose-cert-expiry.sh

Checks certificate rotation:
1. Certificate age
2. Rotation metrics
3. SPIRE server backlog
4. Recent rotation failures

### diagnose-mtls.sh

Checks mTLS connections:
1. Client SVID valid?
2. Server certificate valid?
3. Trust bundle match?
4. Connection test

### diagnose-authorization.sh

Checks authorization failures:
1. Caller's SPIFFE ID
2. Expected SPIFFE ID
3. Authorization policy
4. Audit logs

### ultimate-diagnostic.sh

Runs all diagnostics when everything is broken:
1. Cluster health
2. SPIRE server status
3. Database connectivity
4. Network policies
5. Recent errors
6. Resource usage
7. Certificate status
8. Agent attestation
9. Registration entries
10. Audit logs

## Manual Troubleshooting

### Check SPIRE Server Logs

```bash
kubectl logs -n spire spire-server-0 --tail=100 | grep ERROR
```

### Check SPIRE Agent Logs

```bash
# Get agent pod name
AGENT_POD=$(kubectl get pods -n spire -l app=spire-agent -o jsonpath='{.items[0].metadata.name}')

# Check logs
kubectl logs -n spire $AGENT_POD --tail=100 | grep ERROR
```

### Check Database Connection

```bash
kubectl exec -n spire spire-server-0 -- \
    nc -zv postgres.spire.svc.cluster.local 5432
```

### List All Registration Entries

```bash
kubectl exec -n spire spire-server-0 -- \
    /opt/spire/bin/spire-server entry show
```

### Force Agent Re-Attestation

```bash
kubectl delete pod -n spire <agent-pod-name>
```

### Check Certificate Expiry

```bash
kubectl exec -n spire <agent-pod> -- \
    /opt/spire/bin/spire-agent api fetch | \
    openssl x509 -noout -dates
```

## Performance Debugging

### Check Database Performance

```bash
kubectl top pod -n spire -l app=postgres
```

### Check SPIRE Server Resource Usage

```bash
kubectl top pod -n spire -l app=spire-server
```

### Check API Response Times

```bash
# Via Prometheus metrics
curl http://spire-server:9988/metrics | grep spire_server_api_latency
```

## When to Escalate

Escalate to SPIRE community when:
- Bug in SPIRE itself
- Unexpected behavior after upgrade
- Performance issue with no obvious cause
- Data corruption

**Where to get help:**
- [SPIRE GitHub Issues](https://github.com/spiffe/spire/issues)
- [SPIFFE Slack](https://slack.spiffe.io)
- [SPIRE Discussions](https://github.com/spiffe/spire/discussions)

## Prevention

### Monitoring Alerts

Set up alerts for:
- Certificate expiring in < 6 hours
- SVID fetch failures > 5/minute
- Database connection pool > 80%
- SPIRE server CPU > 80%

### Regular Health Checks

Run diagnostics weekly:
```bash
./ultimate-diagnostic.sh > weekly-health-$(date +%Y%m%d).txt
```

### Backup Testing

Test backup/restore monthly:
```bash
# See Chapter 4: Backup and Recovery
cd ../chapter-04-production-deployment/backup
./test-backup-restore.sh
```

## Next Steps

After troubleshooting:

1. **Document the incident** (runbook update)
2. **Add monitoring** (prevent recurrence)
3. **Test the fix** (verify resolution)
4. **Review with team** (share learnings)

## Related Book Sections

- **Chapter 9.1:** Diagnostic Framework (page XX)
- **Chapter 9.2:** Common Issues (page XX)
- **Chapter 9.3:** Production War Stories (page XX)
- **Chapter 9.4:** Prevention Strategies (page XX)

## Support

Found a new issue not covered here? 
[Open an issue](https://github.com/RunTimeAdmin/spire-ai-agents-book/issues)
