---
title: Graph Operations
description: CRUD operations in Rust.
tags:
  - rust
  - operations
---

# Graph Operations

Learn how to perform CRUD operations using the Rust API.

## Creating Data

```rust
let session = db.session()?;

// Create nodes
session.execute(r#"
    INSERT (:Person {name: 'Alice', age: 30})
    INSERT (:Person {name: 'Bob', age: 25})
"#)?;

// Create edges
session.execute(r#"
    MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
    INSERT (a)-[:KNOWS {since: 2020}]->(b)
"#)?;
```

## Reading Data

```rust
let session = db.session()?;

// Query with results
let result = session.execute(r#"
    MATCH (p:Person)
    RETURN p.name, p.age
"#)?;

for row in result {
    let name: String = row.get("p.name")?;
    let age: i64 = row.get("p.age")?;
    println!("{}: {}", name, age);
}
```

## Updating Data

```rust
let session = db.session()?;

session.execute(r#"
    MATCH (p:Person {name: 'Alice'})
    SET p.age = 31
"#)?;
```

## Deleting Data

```rust
let session = db.session()?;

// Delete edges
session.execute(r#"
    MATCH (a:Person)-[r:KNOWS]->(b:Person)
    DELETE r
"#)?;

// Delete nodes
session.execute(r#"
    MATCH (p:Person {name: 'Alice'})
    DETACH DELETE p
"#)?;
```

## Parameterized Queries

```rust
use grafeo::params;

let session = db.session()?;

let result = session.execute_with_params(
    "MATCH (p:Person {name: $name}) RETURN p",
    params! {
        "name" => "Alice"
    }
)?;
```
