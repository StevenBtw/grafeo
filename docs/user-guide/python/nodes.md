---
title: Working with Nodes
description: Node operations in Python.
tags:
  - python
  - nodes
---

# Working with Nodes

Learn how to create, read, update, and delete nodes using the Python API.

## Creating Nodes

```python
with db.session() as session:
    # Create a single node
    session.execute("""
        INSERT (:Person {name: 'Alice', age: 30})
    """)

    # Create multiple nodes
    session.execute("""
        INSERT (:Person {name: 'Bob', age: 25})
        INSERT (:Person {name: 'Carol', age: 35})
    """)

    # Create with multiple labels
    session.execute("""
        INSERT (:Person:Employee {name: 'Dave', department: 'Engineering'})
    """)
```

## Reading Nodes

```python
with db.session() as session:
    # Find all nodes with label
    result = session.execute("""
        MATCH (p:Person)
        RETURN p.name, p.age
    """)

    for row in result:
        print(f"{row['p.name']} is {row['p.age']} years old")

    # Find specific node
    result = session.execute("""
        MATCH (p:Person {name: 'Alice'})
        RETURN p
    """)
```

## Updating Nodes

```python
with db.session() as session:
    # Update properties
    session.execute("""
        MATCH (p:Person {name: 'Alice'})
        SET p.age = 31, p.city = 'New York'
    """)

    # Remove a property
    session.execute("""
        MATCH (p:Person {name: 'Alice'})
        REMOVE p.temporary_field
    """)
```

## Deleting Nodes

```python
with db.session() as session:
    # Delete a node (must have no edges)
    session.execute("""
        MATCH (p:Person {name: 'Alice'})
        DELETE p
    """)

    # Delete node and its edges
    session.execute("""
        MATCH (p:Person {name: 'Bob'})
        DETACH DELETE p
    """)
```

## Parameterized Queries

```python
with db.session() as session:
    # Use parameters for safety
    result = session.execute(
        "MATCH (p:Person {name: $name}) RETURN p",
        {"name": "Alice"}
    )
```
