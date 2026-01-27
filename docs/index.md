---
title: Graphos - High-Performance Graph Database
description: A pure-Rust, embeddable graph database with Python bindings using GQL (ISO standard) query language.
hide:
  - navigation
  - toc
---

<style>
.md-typeset h1 {
  display: none;
}
</style>

<div class="hero" markdown>

# **Graphos**

### A pure-Rust, high-performance, embeddable graph database

[Get Started](getting-started/index.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/StevenBtw/graphos){ .md-button }

</div>

---

## Why Graphos?

<div class="grid cards" markdown>

-   :material-lightning-bolt:{ .lg .middle } **High Performance**

    ---

    Built from the ground up in Rust for maximum performance with vectorized execution, adaptive chunking, and SIMD-optimized operations.

-   :material-memory:{ .lg .middle } **Embeddable**

    ---

    Embed directly into your application with zero external dependencies. Perfect for edge computing, desktop apps, and serverless environments.

-   :fontawesome-brands-rust:{ .lg .middle } **Pure Rust**

    ---

    Written entirely in safe Rust with no C dependencies. Memory-safe by design with fearless concurrency.

-   :fontawesome-brands-python:{ .lg .middle } **Python Bindings**

    ---

    First-class Python support via PyO3. Use Graphos from Python with a Pythonic API that feels natural.

-   :material-database-search:{ .lg .middle } **GQL Query Language**

    ---

    Uses GQL (ISO/IEC 39075), the international standard for graph query languages. Familiar syntax for graph database users.

-   :material-shield-check:{ .lg .middle } **ACID Transactions**

    ---

    Full ACID compliance with MVCC-based snapshot isolation. Reliable transactions for production workloads.

</div>

---

## Quick Start

=== "Python"

    ```bash
    uv add pygraphos
    ```

    ```python
    import graphos

    # Create an in-memory database
    db = graphos.Database()

    # Create nodes and edges
    with db.session() as session:
        session.execute("""
            INSERT (:Person {name: 'Alice', age: 30})
            INSERT (:Person {name: 'Bob', age: 25})
        """)

        session.execute("""
            MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
            INSERT (a)-[:KNOWS {since: 2024}]->(b)
        """)

        # Query the graph
        result = session.execute("""
            MATCH (p:Person)-[:KNOWS]->(friend)
            RETURN p.name, friend.name
        """)

        for row in result:
            print(f"{row['p.name']} knows {row['friend.name']}")
    ```

=== "Rust"

    ```bash
    cargo add graphos
    ```

    ```rust
    use graphos::Database;

    fn main() -> Result<(), graphos::Error> {
        // Create an in-memory database
        let db = Database::open_in_memory()?;

        // Create a session and execute queries
        let session = db.session()?;

        session.execute(r#"
            INSERT (:Person {name: 'Alice', age: 30})
            INSERT (:Person {name: 'Bob', age: 25})
        "#)?;

        session.execute(r#"
            MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
            INSERT (a)-[:KNOWS {since: 2024}]->(b)
        "#)?;

        // Query the graph
        let result = session.execute(r#"
            MATCH (p:Person)-[:KNOWS]->(friend)
            RETURN p.name, friend.name
        "#)?;

        for row in result {
            println!("{} knows {}", row.get("p.name")?, row.get("friend.name")?);
        }

        Ok(())
    }
    ```

---

## Features

### Data Model

Graphos implements the **Labeled Property Graph (LPG)** model:

- **Nodes** with labels and properties
- **Edges** with types and properties
- **Properties** supporting rich data types (integers, floats, strings, lists, maps)

### Query Language

GQL (Graph Query Language) is the ISO standard for querying property graphs:

```sql
-- Find friends of friends
MATCH (me:Person {name: 'Alice'})-[:KNOWS]->(friend)-[:KNOWS]->(fof)
WHERE fof <> me
RETURN DISTINCT fof.name

-- Shortest path
MATCH path = shortestPath((a:Person)-[:KNOWS*]-(b:Person))
WHERE a.name = 'Alice' AND b.name = 'Charlie'
RETURN path
```

### Architecture Highlights

- **Push-based execution engine** with morsel-driven parallelism
- **Columnar storage** with type-specific compression
- **Cost-based query optimizer** with cardinality estimation
- **MVCC transactions** with snapshot isolation
- **Zone maps** for intelligent data skipping

---

## Installation

=== "Python"

    ```bash
    # Using uv (recommended)
    uv add pygraphos

    # Using pip
    pip install pygraphos
    ```

=== "Rust"

    ```bash
    cargo add graphos
    ```

    Or add to your `Cargo.toml`:

    ```toml
    [dependencies]
    graphos = "0.1"
    ```

---

## License

Graphos is licensed under the [Apache-2.0 License](https://github.com/StevenBtw/graphos/blob/main/LICENSE).
