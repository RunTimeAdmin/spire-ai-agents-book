# Chapter 8: Framework Integration

Production-ready SPIRE integration for major AI agent frameworks.

## What's Included

- `langchain/` - LangChain tools with SPIRE authentication
- `llamaindex/` - LlamaIndex vector store access control
- `autogen/` - AutoGen multi-agent authentication
- `universal/` - Framework-agnostic SPIRE patterns

## Supported Frameworks

### LangChain
- ✅ Authenticated tool execution
- ✅ Automatic SVID rotation
- ✅ mTLS for API calls
- ✅ Audit logging

### LlamaIndex
- ✅ Vector store access control
- ✅ Multi-agent RAG with authorization
- ✅ Collection-level permissions

### AutoGen
- ✅ Agent-to-agent authentication
- ✅ Message signing with SVID
- ✅ Group chat authorization

### Universal Pattern
- ✅ Works with any framework
- ✅ Service mesh for AI agents
- ✅ @spire_authenticated decorator

## Quick Start

### LangChain Integration

```python
from langchain_spire_tools import SPIREAuthenticatedTool, CustomerDataTool

# Initialize SPIRE once at startup
SPIREAuthenticatedTool.initialize_spire()

# Create authenticated tool
customer_tool = CustomerDataTool()

# Use in LangChain agent (automatic mTLS authentication)
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

agent = initialize_agent(
    tools=[customer_tool],
    llm=ChatOpenAI(),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Tool calls are automatically authenticated with SPIRE
result = agent.run("Get data for customer 12345")
```

### LlamaIndex Integration

```python
from llamaindex_spire_vectorstore import SPIREAuthenticatedQdrantClient

# Create Qdrant client with SPIRE authentication
client = SPIREAuthenticatedQdrantClient(
    url="https://qdrant.example.com",
    collection_name="documents"
)

# Access is authorized by SPIFFE ID
# Only agents with correct SPIFFE ID can read/write
vector_store = QdrantVectorStore(client=client)
index = VectorStoreIndex.from_vector_store(vector_store)
```

### AutoGen Integration

```python
from autogen_spire_integration import SPIREAuthenticatedAgent

# Create agents with SPIRE authentication
orchestrator = SPIREAuthenticatedAgent(
    name="orchestrator",
    required_spiffe_id="spiffe://company.com/ai/orchestrator"
)

specialist = SPIREAuthenticatedAgent(
    name="specialist",
    required_spiffe_id="spiffe://company.com/ai/specialist"
)

# Messages between agents are authenticated
# Agents verify each other's SPIFFE IDs
```

### Universal Pattern (Any Framework)

```python
from spire_agent_mesh import AgentServiceMesh, spire_authenticated

# Initialize service mesh
mesh = AgentServiceMesh.get_instance()

# Decorate any function for SPIRE authentication
@spire_authenticated
def call_api(customer_id: str):
    # Automatic mTLS, SVID rotation, circuit breaking
    response = requests.get(f"https://api/customers/{customer_id}")
    return response.json()

# Works with any AI framework!
```

## Installation

```bash
cd chapter-08-framework-integration

# LangChain
cd langchain
pip install -r requirements.txt
python langchain_spire_tools.py

# LlamaIndex
cd ../llamaindex
pip install -r requirements.txt

# AutoGen
cd ../autogen
pip install -r requirements.txt

# Universal
cd ../universal
pip install -r requirements.txt
```

## Architecture Patterns

### Pattern 1: Tool-Level Authentication (LangChain)

```
┌─────────────────┐
│ LangChain Agent │
└────────┬────────┘
         │
    ┌────▼────┐
    │  Tool   │
    └────┬────┘
         │
    ┌────▼────────────┐
    │ SPIRE Client    │
    │ (fetch SVID)    │
    └────┬────────────┘
         │ mTLS
    ┌────▼────────┐
    │ API Server  │
    │ (validates  │
    │  SPIFFE ID) │
    └─────────────┘
```

### Pattern 2: Vector Store Authorization (LlamaIndex)

```
┌──────────────┐     ┌──────────────┐
│  Agent A     │────→│ Qdrant Proxy │
│ SPIFFE: /a   │     │ (checks ID)  │
└──────────────┘     └──────┬───────┘
                            │
┌──────────────┐            │ Allowed
│  Agent B     │────→       ▼
│ SPIFFE: /b   │     ┌──────────────┐
└──────────────┘     │   Qdrant     │
       ↑             │ Vector Store │
       │             └──────────────┘
       └─ Denied
```

### Pattern 3: Agent-to-Agent Auth (AutoGen)

```
┌─────────────┐                    ┌─────────────┐
│ Orchestrator│   Sign message     │  Specialist │
│ SPIFFE: /o  │   with SVID        │ SPIFFE: /s  │
└──────┬──────┘                    └──────▲──────┘
       │                                   │
       │  Message + Signature              │
       └───────────────────────────────────┘
                   Verify SPIFFE ID
```

## Testing

Each framework integration includes tests:

```bash
# Test LangChain integration
cd langchain
python test_langchain_spire.py

# Test LlamaIndex integration
cd ../llamaindex
python test_llamaindex_spire.py

# Test AutoGen integration
cd ../autogen
python test_autogen_spire.py
```

## Production Considerations

### SVID Rotation
All integrations handle automatic SVID rotation:
- Background thread checks every 5 minutes
- Seamless rotation (no dropped requests)
- Graceful degradation on rotation failure

### Connection Pooling
Reuse mTLS connections for performance:
- Single `requests.Session` per tool class
- Persistent connections to API servers
- Configurable pool size

### Error Handling
Robust error handling for production:
- Retry logic for transient failures
- Circuit breaker for downstream services
- Fallback strategies

### Monitoring
Integration with monitoring systems:
- Prometheus metrics for tool execution
- Audit logs for compliance
- Distributed tracing support

## Troubleshooting

### Tool fails with "SPIRE not initialized"

```python
# Call initialize_spire() before using tools
SPIREAuthenticatedTool.initialize_spire()
```

### mTLS connection fails

```bash
# Check SPIRE agent is running
kubectl get pods -n spire -l app=spire-agent

# Check registration entry exists
kubectl exec -n spire spire-server-0 -- \
    spire-server entry show -spiffeID spiffe://company.com/ai/agent
```

### SVID rotation fails

```bash
# Check agent logs
kubectl logs -n spire <agent-pod> | grep rotation

# Verify SVID not expired
openssl x509 -in /path/to/svid.pem -noout -dates
```

## Next Steps

After integrating your framework:

1. **Chapter 6:** Add audit logging for compliance
2. **Chapter 9:** Use diagnostic scripts for troubleshooting
3. **Chapter 10:** Review case studies for your use case

## Related Book Sections

- **Chapter 8.1:** LangChain Integration (page XX)
- **Chapter 8.2:** LlamaIndex Integration (page XX)
- **Chapter 8.3:** AutoGen Integration (page XX)
- **Chapter 8.4:** CrewAI Integration (page XX)
- **Chapter 8.5:** Universal Patterns (page XX)

## Support

Questions about framework integration?  
[Open an issue](https://github.com/RunTimeAdmin/spire-ai-agents-book/issues)
