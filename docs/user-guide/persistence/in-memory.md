---
title: In-Memory Mode
description: Using Graphos with in-memory storage.
tags:
  - persistence
  - in-memory
---

# In-Memory Mode

In-memory mode provides the fastest performance by keeping all data in RAM.

## Creating an In-Memory Database

=== "Python"

    ```python
    import graphos

    # Default is in-memory
    db = graphos.Database()
    ```

=== "Rust"

    ```rust
    use graphos::Database;

    let db = Database::open_in_memory()?;
    ```

## Characteristics

- **No persistence** - Data is lost when the database is closed
- **Maximum performance** - No disk I/O overhead
- **Memory bound** - Limited by available RAM

## Use Cases

- Unit testing
- Development and prototyping
- Caching layers
- Temporary computations
- Benchmarking

## Memory Management

```python
# Set memory limit for in-memory database
db = graphos.Database(
    memory_limit=1 * 1024 * 1024 * 1024  # 1 GB
)
```

!!! warning "Data Loss"
    All data in an in-memory database is lost when the database is closed or the process terminates.
