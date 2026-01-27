---
title: Sessions
description: Session management in Rust.
tags:
  - rust
  - sessions
---

# Sessions

Sessions provide transactional access to the database.

## Creating Sessions

```rust
let db = Database::open_in_memory()?;

// Create a session
let session = db.session()?;

// Use the session
session.execute("INSERT (:Person {name: 'Alice'})")?;
```

## Transactions

```rust
let session = db.session()?;

// Begin explicit transaction
session.begin()?;

session.execute("INSERT (:Person {name: 'Alice'})")?;
session.execute("INSERT (:Person {name: 'Bob'})")?;

// Commit
session.commit()?;
```

## Rollback

```rust
let session = db.session()?;

session.begin()?;
session.execute("INSERT (:Person {name: 'Alice'})")?;

// Something went wrong, rollback
session.rollback()?;
```

## Transaction Closure

```rust
let session = db.session()?;

// Execute in transaction with automatic commit/rollback
session.transaction(|tx| {
    tx.execute("INSERT (:Person {name: 'Alice'})")?;
    tx.execute("INSERT (:Person {name: 'Bob'})")?;
    Ok(())
})?;
```

## Multiple Sessions

```rust
let db = Database::open_in_memory()?;

// Each session has isolated transactions
let session1 = db.session()?;
let session2 = db.session()?;

session1.begin()?;
session1.execute("INSERT (:Person {name: 'Alice'})")?;
// session2 won't see Alice until session1 commits

session1.commit()?;
// Now session2 can see Alice
```
