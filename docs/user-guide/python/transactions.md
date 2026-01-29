---
title: Transactions
description: Transaction management in Python.
tags:
  - python
  - transactions
---

# Transactions

Grafeo supports ACID transactions with snapshot isolation.

## Implicit Transactions

By default, each query runs in its own transaction:

```python
with db.session() as session:
    # Each execute is a separate transaction
    session.execute("INSERT (:Person {name: 'Alice'})")
    session.execute("INSERT (:Person {name: 'Bob'})")
```

## Explicit Transactions

For multiple operations in a single transaction:

```python
with db.session() as session:
    # Start explicit transaction
    session.begin()

    try:
        session.execute("INSERT (:Person {name: 'Alice'})")
        session.execute("INSERT (:Person {name: 'Bob'})")

        # Commit the transaction
        session.commit()
    except Exception as e:
        # Rollback on error
        session.rollback()
        raise
```

## Transaction Context Manager

```python
with db.session() as session:
    with session.transaction():
        session.execute("INSERT (:Person {name: 'Alice'})")
        session.execute("INSERT (:Person {name: 'Bob'})")
    # Automatically committed if no exception
```

## Rollback

```python
with db.session() as session:
    session.begin()

    session.execute("INSERT (:Person {name: 'Alice'})")

    # Decide to rollback
    session.rollback()
    # Alice was not created
```

## Isolation Levels

Grafeo uses snapshot isolation by default:

```python
# Session 1 sees a consistent snapshot
with db.session() as session1:
    session1.begin()

    # Session 2 makes changes
    with db.session() as session2:
        session2.execute("MATCH (p:Person) SET p.updated = true")

    # Session 1 still sees old data (snapshot isolation)
    result = session1.execute("MATCH (p:Person) RETURN p.updated")
    # updated will be null/false, not true

    session1.commit()
```

## Read-Only Transactions

```python
with db.session() as session:
    # Read-only transaction for better performance
    with session.transaction(read_only=True):
        result = session.execute("MATCH (p:Person) RETURN count(p)")
```
