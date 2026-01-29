---
title: Rust API
description: Using Grafeo from Rust.
---

# Rust API

Grafeo is written in Rust and provides a native Rust API.

## Quick Start

```rust
use grafeo::Database;

fn main() -> Result<(), grafeo::Error> {
    let db = Database::open_in_memory()?;
    let session = db.session()?;

    session.execute("INSERT (:Person {name: 'Alice'})")?;

    let result = session.execute("MATCH (p:Person) RETURN p.name")?;
    for row in result {
        println!("{}", row.get::<String>("p.name")?);
    }

    Ok(())
}
```

## Sections

<div class="grid cards" markdown>

-   **[Database Setup](database.md)**

    ---

    Creating and configuring databases.

-   **[Graph Operations](operations.md)**

    ---

    CRUD operations on nodes and edges.

-   **[Sessions](sessions.md)**

    ---

    Session management and transactions.

</div>
