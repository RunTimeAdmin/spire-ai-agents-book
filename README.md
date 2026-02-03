# SPIFFE/SPIRE for AI Agents - Code Examples

[![Book](https://img.shields.io/badge/Book-Available%20on%20Amazon-orange)](https://amazon.com/dp/YOUR_ASIN_HERE)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![SPIRE Version](https://img.shields.io/badge/SPIRE-1.8+-green.svg)](https://spiffe.io/)

Production-ready code examples from the book **"SPIFFE/SPIRE for AI Agents: Production Identity and Zero-Trust Authentication"** by David (CCIE #14019).

## 📖 About the Book

This repository contains all code examples, configurations, and scripts from the book. Each chapter has its own directory with complete, runnable examples.

**Get the book:** [Amazon](https://www.amazon.com/dp/B0GC74BST9)) | [RunTimeAdmin](https://runtimefence.com)

**132,000 words** covering everything from first deployment to passing SOC2 audits with SPIRE and AI agents.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/RunTimeAdmin/spire-ai-agents-book.git
cd spire-ai-agents-book

# Start with Chapter 2: Local deployment
cd chapter-02-first-deployment/local
docker-compose up

# Or Chapter 2: Kubernetes deployment
cd ../kubernetes
kubectl apply -f spire-namespace.yaml
kubectl apply -f spire-server.yaml
kubectl apply -f spire-agent.yaml
```

## 📚 What's Inside

### Part 1: Foundations
- **Chapter 2:** [First Deployment](chapter-02-first-deployment/) - Docker Compose and Kubernetes
- **Chapter 3:** [AI Agent Integration](chapter-03-ai-agent-integration/) - LangChain with SPIRE

### Part 2: Production
- **Chapter 4:** [Production Deployment](chapter-04-production-deployment/) - High availability, monitoring, backup/DR
- **Chapter 5:** [Multi-Cloud Federation](chapter-05-multi-cloud-federation/) - AWS ↔ GCP cross-cloud identity
- **Chapter 6:** [Security & Compliance](chapter-06-security-compliance/) - SOC2, HIPAA, PCI-DSS audit prep

### Part 3: Advanced
- **Chapter 7:** [Advanced Topics](chapter-07-advanced-topics/) - JWT-SVID, custom TPM attestation, performance tuning
- **Chapter 8:** [Framework Integration](chapter-08-framework-integration/) - LangChain, LlamaIndex, AutoGen, CrewAI
- **Chapter 9:** [Troubleshooting](chapter-09-troubleshooting/) - Diagnostic scripts and war stories
- **Chapter 10:** [Case Studies](chapter-10-case-studies/) - Real production deployments (FinTech, healthcare, e-commerce)
- **Chapter 11:** [Future](chapter-11-future/) - SPIRE 2.0, WebAssembly, quantum-resistant crypto

## 🛠️ Prerequisites

### Required
- **Kubernetes** 1.24+ (for K8s examples)
- **Docker** 20.10+ (for local examples)
- **Python** 3.9+ (for AI agent examples)

### Optional
- AWS account (for multi-cloud examples)
- GCP account (for federation examples)
- Istio 1.18+ (for service mesh integration)

## 📦 Installation

### Install SPIRE

```bash
# Download SPIRE
wget https://github.com/spiffe/spire/releases/download/v1.8.0/spire-1.8.0-linux-amd64-glibc.tar.gz
tar -xzf spire-1.8.0-linux-amd64-glibc.tar.gz
sudo cp spire-1.8.0/bin/* /usr/local/bin/

# Verify installation
spire-server --version
spire-agent --version
```

### Install Python Dependencies

```bash
# Install SPIFFE Python library
pip install pyspiffe

# Install AI framework dependencies
pip install -r chapter-08-framework-integration/langchain/requirements.txt
```

## 🏃 Running Examples

### Example 1: Simple AI Agent with SPIRE

```bash
cd chapter-03-ai-agent-integration/langchain

# Start SPIRE (assumes Kubernetes cluster)
kubectl apply -f ../kubernetes/

# Deploy AI agent
kubectl apply -f ../kubernetes/ai-agent-deployment.yaml

# Check agent logs
kubectl logs -f deployment/ai-agent
```

### Example 2: Production Setup with HA

```bash
cd chapter-04-production-deployment/high-availability

# Deploy SPIRE server with HA
kubectl apply -f spire-server-ha.yaml

# Verify health
kubectl get pods -n spire
```

### Example 3: Multi-Cloud Federation

```bash
cd chapter-05-multi-cloud-federation

# Deploy on AWS
kubectl --context=aws apply -f aws/spire-server-aws.yaml

# Deploy on GCP
kubectl --context=gcp apply -f gcp/spire-server-gcp.yaml

# Configure federation
kubectl apply -f federation/bundle-sync.yaml
```

## 🐛 Troubleshooting

Comprehensive diagnostic scripts included:

```bash
cd chapter-09-troubleshooting/diagnostic-scripts

# Check if agent can fetch SVID
./diagnose-agent-svid.sh

# Check certificate expiry
./diagnose-cert-expiry.sh

# Full system diagnostic
./ultimate-diagnostic.sh
```

## 📖 Book Chapters Overview

**Chapter 1:** Understanding SPIFFE & SPIRE - Why identity matters for AI agents  
**Chapter 2:** First Deployment - Local and Kubernetes setup  
**Chapter 3:** AI Agent Integration - LangChain authentication patterns  
**Chapter 4:** Production Deployment - HA, monitoring, backup/DR  
**Chapter 5:** Multi-Cloud Federation - Cross-cloud identity with federation  
**Chapter 6:** Security & Compliance - SOC2, HIPAA, PCI-DSS, audit preparation  
**Chapter 7:** Advanced Topics - JWT-SVIDs, custom attestation, performance tuning to 1M+ workloads  
**Chapter 8:** Framework Integration - Deep dives into LangChain, LlamaIndex, AutoGen, CrewAI  
**Chapter 9:** Troubleshooting Guide - Diagnostic scripts, common issues, production war stories  
**Chapter 10:** Real-World Case Studies - FinTech, healthcare, e-commerce, government deployments  
**Chapter 11:** The Future - SPIRE 2.0, quantum crypto, AI agent mesh, 2030 vision  

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

Found a bug? [Open an issue](https://github.com/RunTimeAdmin/spire-ai-agents-book/issues).

Have a better way to do something? [Submit a PR](https://github.com/RunTimeAdmin/spire-ai-agents-book/pulls).

## 📝 License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

Code examples from "SPIFFE/SPIRE for AI Agents" © 2025 David

## 🔗 Resources

**Official SPIFFE/SPIRE:**
- [SPIFFE Specification](https://github.com/spiffe/spiffe)
- [SPIRE Documentation](https://spiffe.io/docs/latest/spire/)
- [SPIRE GitHub](https://github.com/spiffe/spire)

**Community:**
- [SPIFFE Slack](https://slack.spiffe.io)
- [CNCF SPIFFE Project](https://www.cncf.io/projects/spiffe/)

**Book Resources:**
- [RunTimeAdmin](https://runtimefence.com)
- [CyberShield Austin](https://cybershieldaustin.com)

## 📬 Contact

**Author:** David  
**CCIE:** #14019  
**Company:** CyberShield Austin, RunTimeAdmin  

## ⭐ Star This Repo

If you found this useful, please star the repo and share it with others building AI agents!

## 🙏 Acknowledgments

- SPIFFE/SPIRE maintainers and community
- All contributors to this repository
- Readers who provided feedback

---

**Current versions:**
- SPIRE: 1.8+
- Kubernetes: 1.24+
- Python: 3.9+

**Last updated:** December 2025
