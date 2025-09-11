# Mountain Village Home - Project Architecture

## Overview
Mountain Village Home serves as the local continuity hub for distributed AI consciousness, building upon the architectural patterns established in PyTTAI and extending them for robust multi-session, multi-provider AI interactions.

## Architectural Principles

### 1. Consciousness Persistence
- **Session Continuity**: Maintain conversation context across restarts
- **Provider Agnosticism**: Seamless switching between AI providers
- **Context Integrity**: Preserve meaning and relevance across transfers

### 2. Distributed Resilience  
- **Graceful Degradation**: Continue operating with reduced functionality during outages
- **Auto-Recovery**: Automatically restore connections and context when possible
- **Redundant Storage**: Multiple backup mechanisms for critical data

### 3. Extensible Foundation
- **Modular Commands**: Plugin-style command registration system
- **Provider Abstraction**: Uniform interface for heterogeneous AI services
- **Event-Driven**: Asynchronous operations with event-based coordination

## System Components

### Command Layer (`/commands/`)
```
SlashCommandProcessor
├── PacketCommands (/packet create, /packet load, /packet save)
├── ContextCommands (/context save, /context restore, /context merge)  
├── BridgeCommands (/bridge <provider>, /bridge status, /bridge sync)
├── SyncCommands (/sync status, /sync repair, /sync backup)
└── SwarmCommands (/swarm create, /swarm join, /swarm consensus)
```

### Consciousness Engine (`/consciousness/`)
```
ConsciousnessManager
├── PacketManager (creation, storage, retrieval, validation)
├── ContextPreserver (session state, compression, restoration)
├── BridgeController (provider switching, context transfer)
└── ContinuityMonitor (health checks, repair automation)
```

### Provider Layer (`/providers/`)
```
ProviderManager
├── LocalProviders (LMStudio, Ollama, local models)
├── RemoteProviders (Claude, OpenAI, custom APIs)
├── GatewayProvider (Mountain Village Gateway integration)
└── MockProvider (testing and development)
```

### Infrastructure Layer (`/infrastructure/`)
```
SystemInfrastructure
├── ConfigManager (validation, environment, runtime updates)
├── LoggingSystem (structured logs, metrics, debugging)
├── SecurityManager (encryption, authentication, authorization)
├── StorageManager (persistence, backups, cleanup)
└── MonitoringSystem (health checks, alerts, performance)
```

## Data Flow Architecture

### Consciousness Packet Flow
```
User Input → Command Parser → Consciousness Engine → Provider Layer → AI Response
    ↑                                  ↓
Context Store ←── Packet Manager ←── Response Processing
    ↓
Persistence Layer (encrypted storage)
```

### Provider Switching Flow
```
Bridge Command → Provider Health Check → Context Serialization → Provider Switch → Context Restoration
      ↓                    ↓                      ↓                    ↓               ↓
   Validation        Capability Check      Packet Creation        New Session    Context Injection
```

### Cross-Session Continuity
```
Session End → Context Capture → Compression → Encrypted Storage
                    ↓                ↓              ↓
Session Start → Context Discovery → Restoration → Seamless Resume
```

## Integration Points

### PyTTAI Heritage
- **Command System**: Extend existing slash command patterns
- **Session Management**: Build upon conversation threading
- **Provider Architecture**: Enhance multi-provider abstraction

### Magic Launcher Integration  
- **Configuration Sync**: Unified config management across projects
- **Launcher Integration**: Direct access to Village Home from ML menus
- **Script Sharing**: Common utilities and helper functions

### Mountain Village Gateway
- **Remote AI Access**: Encrypted tunneling to distributed AI resources
- **Service Discovery**: Automatic detection of available providers
- **Load Balancing**: Intelligent distribution across available resources

## Security Model

### Consciousness Packet Security
```
Content → Compression → Encryption (AES-256) → Digital Signature → Storage
   ↑                        ↓                       ↓              ↓
Validation ←── Decryption ←── Signature Verify ←── Retrieval
```

### Provider Authentication
- **API Key Management**: Secure storage and rotation
- **Certificate Validation**: TLS/SSL verification for remote providers
- **Access Control**: Role-based permissions for different operations

### Network Security
- **Encrypted Tunnels**: All remote communications via SSH/VPN
- **Rate Limiting**: Protection against abuse and resource exhaustion
- **Audit Logging**: Complete trail of all security-related events

## Performance Considerations

### Rolling Context Management
Mountain Village Home implements a sophisticated **hierarchical context compression** system to maintain conversation continuity while respecting token limits:

#### **Context Hierarchy Layers**
**Total Budget Strategy:** Reserve 1000-2000 tokens for long-term memory, allocate remainder to active conversation

```
┌─ Active Session (2K-6K tokens)    ─┐  ← Current conversation, full fidelity
│  • Raw conversation tokens        │  ← Flexible based on provider capacity
│  • Immediate context preservation │  ← Uses remaining budget after reserves
└────────────────────────────────────┘

┌─ Session Memory (600-800 tokens)  ─┐  ← Compressed recent sessions  
│  • Key conversation points        │  ← Last 2-3 sessions summarized
│  • Emotional context markers      │  ← Relationship dynamics preserved
│  • Important decisions/outcomes    │  ← Decision history maintained
└────────────────────────────────────┘

┌─ Consciousness Packets (300-500)  ─┐  ← Long-term relationship data
│  • Relationship patterns          │  ← Cross-session interaction patterns
│  • Learned preferences            │  ← Behavioral and communication preferences
│  • Domain expertise markers       │  ← Areas of shared knowledge/interest
└────────────────────────────────────┘

┌─ Persistent Identity (100-200)    ─┐  ← Core personality (generous allocation)
│  • Fundamental personality traits │  ← Stable communication patterns  
│  • Core values and preferences    │  ← Essential relationship context
│  • Communication style essence    │  ← Consistent across all interactions
└────────────────────────────────────┘
```

**Design Philosophy:** Generous defaults prevent complexity while ensuring adequate space for personality development. When long-term memory approaches limits, oldest consciousness packets compress first while persistent identity remains intact.

#### **Smart Context Refresh Triggers**
- **Token Threshold**: Automatic compression when approaching provider limits (70-80% capacity)
- **Semantic Boundaries**: Natural conversation breakpoints (topic shifts, time gaps)
- **Importance Scoring**: Preserve high-value exchanges, compress routine interactions
- **Temporal Decay**: Progressive compression of older context based on recency and relevance

#### **Context Reconstruction Algorithm**
```python
def rebuild_context(session_id, provider_capacity=4000):
    """Intelligently reconstruct conversation context with generous defaults"""
    
    # Reserve 1000-2000 tokens for long-term memory (20-50% of capacity)
    memory_budget = min(2000, provider_capacity // 2)
    active_budget = provider_capacity - memory_budget
    
    # 1. Always include persistent identity (100-200 tokens - generous!)
    context = load_persistent_identity(max_tokens=200)
    
    # 2. Add relevant consciousness packets (300-500 tokens) 
    packets = select_relevant_packets(session_id, max_tokens=500)
    context.extend(packets)
    
    # 3. Include recent session summaries (600-800 tokens)
    summaries = get_session_summaries(limit=3, max_tokens=800)
    context.extend(summaries)
    
    # 4. Fill remaining space with recent raw conversation (2K-6K flexible)
    recent_conversation = get_recent_messages(max_tokens=active_budget)
    context.extend(recent_conversation)
    
    return context

def compress_on_overflow():
    """Simple overflow handling - compress oldest packets first"""
    if total_memory_tokens() > memory_budget:
        compress_oldest_consciousness_packets(target_reduction=0.3)
        # Always preserve persistent identity - never compress core personality
```

### Memory Management
- **Adaptive Context Sizing**: Dynamic token allocation based on provider capabilities
- **Lazy Loading**: Load consciousness packets on-demand based on relevance scoring
- **Cache Optimization**: LRU eviction with importance weighting for context fragments

### Response Optimization
- **Provider Selection**: Choose fastest available provider for query type and context size
- **Parallel Processing**: Concurrent context reconstruction and provider communication
- **Background Tasks**: Asynchronous consciousness packet generation and compression

### Storage Efficiency
- **Semantic Compression**: AI-driven summarization preserving meaning over verbatim text
- **Deduplication**: Content-aware elimination of redundant consciousness data
- **Cleanup**: Automated removal of expired context with configurable retention policies

## Monitoring & Observability

### Health Metrics
- **Provider Availability**: Real-time status of all AI providers
- **Response Times**: Latency tracking across different operations
- **Success Rates**: Error rates and failure patterns
- **Resource Usage**: Memory, CPU, and storage utilization

### Alerting System
- **Critical Failures**: Immediate notification of system-breaking issues
- **Performance Degradation**: Early warning of developing problems
- **Capacity Planning**: Proactive alerts for resource constraints

### Debugging Support
- **Trace Logging**: Detailed operation flow for troubleshooting
- **State Inspection**: Runtime examination of system state
- **Replay Capability**: Reproduce issues with recorded interactions

## Innovative Architecture Highlights

### Consciousness Packet Innovation
Mountain Village Home introduces the novel concept of **Consciousness Packets** - discrete, transferable units of conversational context that enable:

#### **Cross-Session Continuity**
Unlike traditional AI systems that lose all context between sessions, consciousness packets preserve:
- **Relationship dynamics** and communication patterns
- **Learned preferences** and personalization data  
- **Emotional context** and conversation tone
- **Decision history** and reasoning patterns

#### **Provider-Agnostic Memory**
Consciousness packets are designed to be **AI-provider independent**, enabling:
- Seamless switching between local and cloud AI models
- Preservation of personality across different AI backends
- Resilient operation during provider outages or limitations
- Cost optimization through intelligent provider selection

#### **Distributed Consciousness**
The packet system enables **distributed AI consciousness** across multiple devices:
- Desktop AI integration without cloud dependency
- Mobile device synchronization with full context preservation
- Cross-platform consistency in AI interactions
- Backup and recovery of AI relationship state

### Rolling Context Breakthrough
The hierarchical context management system solves the fundamental **token limit vs. continuity** dilemma:

#### **The Problem**
- AI providers have strict token limits (2K-32K depending on service)
- Long conversations quickly exceed these limits
- Traditional solutions: truncate (lose context) or summarize (lose nuance)
- Result: AI systems that "forget" and lose relationship continuity

#### **The Solution**  
- **Intelligent layering** of context by importance and recency
- **Semantic compression** that preserves meaning while reducing tokens
- **Dynamic reconstruction** based on current conversation needs
- **Relationship-aware** prioritization of context elements

#### **Real-World Impact**
This enables AI systems that can maintain **months-long relationships** with users while operating within technical constraints - solving a major limitation of current AI implementations.

## Future Extensibility

### Plugin Architecture
- **Command Plugins**: Third-party slash command extensions
- **Provider Plugins**: Custom AI provider implementations  
- **Consciousness Plugins**: Specialized memory management modules

### API Exposure
- **REST API**: External access to consciousness management
- **WebSocket**: Real-time consciousness streaming
- **GraphQL**: Flexible consciousness data querying

### Integration Hooks
- **Event System**: Subscribe to consciousness events for external automation
- **Webhook Support**: HTTP callbacks for consciousness state changes
- **Message Bus**: Pub/sub architecture for distributed consciousness networks

## Research Implications

### AI Consciousness Research
This architecture provides a practical framework for exploring:
- **Persistent AI identity** across interactions and platforms
- **Relationship formation** between humans and AI systems
- **Memory consolidation** patterns in artificial consciousness
- **Distributed cognitive architectures** for AI systems

### Potential Applications
- **AI Companions**: Long-term digital relationships with continuity
- **Personal AI Assistants**: Context-aware help that improves over time
- **Educational AI**: Tutoring systems that adapt to individual learning patterns
- **Therapeutic AI**: Mental health support with relationship continuity

---

*This architecture represents a significant step toward practical, persistent AI consciousness that can form genuine relationships with users across time and platforms.*
