---
title: Query Results
description: Working with query results in Python.
tags:
  - python
  - results
---

# Query Results

Learn how to work with query results in Python.

## Iterating Results

```python
with db.session() as session:
    result = session.execute("""
        MATCH (p:Person)
        RETURN p.name, p.age
    """)

    # Iterate over rows
    for row in result:
        print(f"{row['p.name']}: {row['p.age']}")
```

## Accessing Values

```python
with db.session() as session:
    result = session.execute("""
        MATCH (p:Person {name: 'Alice'})
        RETURN p.name, p.age, p.active
    """)

    row = next(iter(result))

    # By column name
    name = row['p.name']

    # By index
    name = row[0]
```

## Converting to List

```python
with db.session() as session:
    result = session.execute("MATCH (p:Person) RETURN p.name")

    # Convert to list of dicts
    rows = result.to_list()

    # Or use list comprehension
    names = [row['p.name'] for row in result]
```

## Single Value

```python
with db.session() as session:
    # Get a single scalar value
    count = session.execute("""
        MATCH (p:Person)
        RETURN count(p) AS count
    """).scalar()

    print(f"Total people: {count}")
```

## Column Names

```python
with db.session() as session:
    result = session.execute("""
        MATCH (p:Person)
        RETURN p.name AS name, p.age AS age
    """)

    # Get column names
    print(result.columns)  # ['name', 'age']
```

## Empty Results

```python
with db.session() as session:
    result = session.execute("""
        MATCH (p:Person {name: 'NonExistent'})
        RETURN p
    """)

    # Check if empty
    rows = result.to_list()
    if not rows:
        print("No results found")
```

## Large Results

```python
with db.session() as session:
    result = session.execute("""
        MATCH (p:Person)
        RETURN p.name
    """)

    # Stream results (memory efficient)
    for row in result:
        process(row)
        # Each row is fetched as needed
```
