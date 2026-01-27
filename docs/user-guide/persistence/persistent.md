---
title: Persistent Storage
description: Using Graphos with durable storage.
tags:
  - persistence
  - storage
---

# Persistent Storage

Persistent mode stores data durably on disk.

## Creating a Persistent Database

=== "Python"

    ```python
    import graphos

    db = graphos.Database(path="my_graph.db")
    ```

=== "Rust"

    ```rust
    use graphos::Database;

    let db = Database::open("my_graph.db")?;
    ```

## File Structure

```
my_graph.db/
├── data/           # Main data files
├── wal/            # Write-ahead log
└── metadata        # Database metadata
```

## Durability Guarantees

- **Write-Ahead Logging (WAL)** - All changes logged before applying
- **Checkpointing** - Periodic consolidation of WAL into data files
- **Crash Recovery** - Automatic recovery from WAL on startup

## Configuration

```python
db = graphos.Database(
    path="my_graph.db",
    # Sync mode: 'full' (default), 'normal', 'off'
    sync_mode='full'
)
```

| Sync Mode | Durability | Performance |
|-----------|------------|-------------|
| `full` | Highest | Slower |
| `normal` | Good | Faster |
| `off` | None | Fastest |

## Reopening a Database

```python
# First session
db = graphos.Database(path="my_graph.db")
with db.session() as s:
    s.execute("INSERT (:Person {name: 'Alice'})")
db.close()

# Later session - data persists
db = graphos.Database(path="my_graph.db")
with db.session() as s:
    result = s.execute("MATCH (p:Person) RETURN p.name")
    # Returns 'Alice'
```
