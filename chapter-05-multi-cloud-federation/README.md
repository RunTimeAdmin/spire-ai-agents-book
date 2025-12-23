# Chapter 5: Multi-Cloud Federation

Cross-cloud SPIRE federation for AWS ↔ GCP ↔ Azure identity.

## What's Included

- `aws/` - AWS SPIRE server configuration
- `gcp/` - GCP SPIRE server configuration  
- `federation/` - Bundle sync and trust configuration

## Quick Start

```bash
# Deploy on AWS
kubectl --context=aws apply -f aws/spire-server-aws.yaml

# Deploy on GCP
kubectl --context=gcp apply -f gcp/spire-server-gcp.yaml

# Configure federation
kubectl apply -f federation/bundle-sync.yaml
```

## Architecture

```
    AWS                              GCP
┌──────────┐                    ┌──────────┐
│  SPIRE   │ ←── Bundle Sync ──→│  SPIRE   │
│  Server  │                    │  Server  │
└────┬─────┘                    └────┬─────┘
     │                                │
  Agents                          Agents
```

See book Chapter 5 for complete implementation.
