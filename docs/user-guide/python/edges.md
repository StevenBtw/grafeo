---
title: Working with Edges
description: Edge operations in Python.
tags:
  - python
  - edges
---

# Working with Edges

Learn how to create and manage relationships between nodes.

## Creating Edges

```python
with db.session() as session:
    # First create nodes
    session.execute("""
        INSERT (:Person {name: 'Alice'})
        INSERT (:Person {name: 'Bob'})
    """)

    # Create an edge
    session.execute("""
        MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
        INSERT (a)-[:KNOWS]->(b)
    """)

    # Create edge with properties
    session.execute("""
        MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
        INSERT (a)-[:WORKS_WITH {since: 2020, project: 'Alpha'}]->(b)
    """)
```

## Reading Edges

```python
with db.session() as session:
    # Find edges
    result = session.execute("""
        MATCH (a:Person)-[r:KNOWS]->(b:Person)
        RETURN a.name AS from, b.name AS to, r.since
    """)

    for row in result:
        print(f"{row['from']} knows {row['to']} since {row['r.since']}")

    # Get edge type
    result = session.execute("""
        MATCH (a:Person {name: 'Alice'})-[r]->(b)
        RETURN type(r) AS relationship_type, b.name
    """)
```

## Updating Edges

```python
with db.session() as session:
    # Update edge properties
    session.execute("""
        MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
        SET r.strength = 'close', r.updated = true
    """)
```

## Deleting Edges

```python
with db.session() as session:
    # Delete specific edge
    session.execute("""
        MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
        DELETE r
    """)

    # Delete all edges of a type
    session.execute("""
        MATCH ()-[r:TEMPORARY]->()
        DELETE r
    """)
```
