---
title: Configuration
description: Configure Graphos for your use case.
---

# Configuration

Graphos can be configured for different use cases, from small embedded applications to high-performance server deployments.

## Database Modes

### In-Memory Mode

For temporary data or maximum performance:

=== "Python"

    ```python
    import graphos

    # In-memory database (default)
    db = graphos.Database()
    ```

=== "Rust"

    ```rust
    use graphos::Database;

    let db = Database::open_in_memory()?;
    ```

!!! note "Data Persistence"
    In-memory databases do not persist data. All data is lost when the database is closed.

### Persistent Mode

For durable storage:

=== "Python"

    ```python
    import graphos

    # Persistent database
    db = graphos.Database(path="my_graph.db")
    ```

=== "Rust"

    ```rust
    use graphos::Database;

    let db = Database::open("my_graph.db")?;
    ```

## Configuration Options

### Memory Limit

Control the maximum memory usage:

=== "Python"

    ```python
    db = graphos.Database(
        path="my_graph.db",
        memory_limit=4 * 1024 * 1024 * 1024  # 4 GB
    )
    ```

=== "Rust"

    ```rust
    use graphos::{Database, Config};

    let config = Config::builder()
        .memory_limit(4 * 1024 * 1024 * 1024)  // 4 GB
        .build()?;

    let db = Database::open_with_config("my_graph.db", config)?;
    ```

### Thread Pool Size

Configure parallelism:

=== "Python"

    ```python
    db = graphos.Database(
        path="my_graph.db",
        threads=8
    )
    ```

=== "Rust"

    ```rust
    use graphos::{Database, Config};

    let config = Config::builder()
        .threads(8)
        .build()?;

    let db = Database::open_with_config("my_graph.db", config)?;
    ```

!!! tip "Default Thread Count"
    By default, Graphos uses the number of available CPU cores.

## Configuration Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `path` | `string` | `None` | Database file path (None for in-memory) |
| `memory_limit` | `int` | System RAM | Maximum memory usage in bytes |
| `threads` | `int` | CPU cores | Number of worker threads |
| `read_only` | `bool` | `false` | Open database in read-only mode |

## Environment Variables

Graphos can also be configured via environment variables:

| Variable | Description |
|----------|-------------|
| `GRAPHOS_MEMORY_LIMIT` | Maximum memory in bytes |
| `GRAPHOS_THREADS` | Number of worker threads |
| `GRAPHOS_LOG_LEVEL` | Logging level (error, warn, info, debug, trace) |

## Performance Tuning

### For High-Throughput Workloads

```python
db = graphos.Database(
    path="high_throughput.db",
    memory_limit=8 * 1024 * 1024 * 1024,  # 8 GB
    threads=16
)
```

### For Low-Memory Environments

```python
db = graphos.Database(
    path="embedded.db",
    memory_limit=256 * 1024 * 1024,  # 256 MB
    threads=2
)
```

### For Read-Heavy Workloads

```python
# Multiple read replicas can be opened read-only
db = graphos.Database(
    path="replica.db",
    read_only=True
)
```

## Next Steps

- [User Guide](../user-guide/index.md) - Learn more about using Graphos
- [Architecture](../architecture/index.md) - Understand how Graphos works
