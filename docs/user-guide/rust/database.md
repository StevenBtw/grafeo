---
title: Database Setup
description: Creating and configuring databases in Rust.
tags:
  - rust
  - database
---

# Database Setup

Learn how to create and configure Graphos databases in Rust.

## Creating a Database

```rust
use graphos::Database;

// In-memory database
let db = Database::open_in_memory()?;

// Persistent database
let db = Database::open("my_graph.db")?;
```

## Configuration

```rust
use graphos::{Database, Config};

let config = Config::builder()
    .memory_limit(4 * 1024 * 1024 * 1024)  // 4 GB
    .threads(8)
    .build()?;

let db = Database::open_with_config("my_graph.db", config)?;
```

## Database Lifecycle

```rust
use graphos::Database;

fn main() -> Result<(), graphos::Error> {
    // Create database
    let db = Database::open("my_graph.db")?;

    // Use the database
    let session = db.session()?;
    session.execute("INSERT (:Person {name: 'Alice'})")?;

    // Database is dropped and closed when it goes out of scope
    Ok(())
}
```

## Thread Safety

`Database` is `Send` and `Sync`, so it can be shared across threads:

```rust
use graphos::Database;
use std::sync::Arc;
use std::thread;

let db = Arc::new(Database::open_in_memory()?);

let handles: Vec<_> = (0..4).map(|i| {
    let db = Arc::clone(&db);
    thread::spawn(move || {
        let session = db.session().unwrap();
        session.execute(&format!(
            "INSERT (:Person {{id: {}}})", i
        )).unwrap();
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}
```
