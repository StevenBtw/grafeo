---
title: Crate Structure
description: The five crates that make up Grafeo.
tags:
  - architecture
  - crates
---

# Crate Structure

Grafeo is organized into five crates with clear responsibilities.

## Dependency Graph

```mermaid
graph BT
    COMMON[grafeo-common]
    CORE[grafeo-core]
    ADAPTERS[grafeo-adapters]
    ENGINE[grafeo-engine]
    PYTHON[grafeo-python]

    CORE --> COMMON
    ADAPTERS --> COMMON
    ADAPTERS --> CORE
    ENGINE --> COMMON
    ENGINE --> CORE
    ENGINE --> ADAPTERS
    PYTHON --> ENGINE
```

## grafeo-common

Foundation types and utilities.

| Module | Purpose |
|--------|---------|
| `types/` | NodeId, EdgeId, Value, LogicalType |
| `memory/` | Arena allocator, memory pools |
| `utils/` | Hashing, error types |

```rust
use grafeo_common::types::{NodeId, Value};
use grafeo_common::memory::Arena;
```

## grafeo-core

Core data structures and execution engine.

| Module | Purpose |
|--------|---------|
| `graph/lpg/` | LPG storage (nodes, edges, properties) |
| `index/` | Hash, B-tree, adjacency indexes |
| `execution/` | DataChunk, operators, pipelines |

```rust
use grafeo_core::graph::LpgStore;
use grafeo_core::index::BTreeIndex;
use grafeo_core::execution::DataChunk;
```

## grafeo-adapters

External interfaces and adapters.

| Module | Purpose |
|--------|---------|
| `query/gql/` | GQL parser (lexer, parser, AST) |
| `query/cypher/` | Cypher compatibility layer |
| `storage/` | Storage backends (memory, WAL) |
| `plugins/` | Plugin system |

```rust
use grafeo_adapters::query::gql::GqlParser;
use grafeo_adapters::storage::WalBackend;
```

## grafeo-engine

Database facade and coordination.

| Module | Purpose |
|--------|---------|
| `database.rs` | Database struct, lifecycle |
| `session.rs` | Session management |
| `query/` | Query processor, planner, optimizer |
| `transaction/` | Transaction manager, MVCC |

```rust
use grafeo_engine::{Database, Session, Config};
```

## grafeo-python

Python bindings via PyO3.

| Module | Purpose |
|--------|---------|
| `database.rs` | PyGrafeoDB class |
| `query.rs` | Query execution |
| `types.rs` | Type conversions |

```python
import grafeo
db = grafeo.Database()
```

## Crate Guidelines

1. **No cyclic dependencies** - Strict layering
2. **Public API minimization** - Only expose what's needed
3. **Feature flags** - Optional functionality gated by features
4. **Documentation** - All public items documented
