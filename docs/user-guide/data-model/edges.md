---
title: Edges and Types
description: Working with edges and relationship types in Graphos.
tags:
  - data-model
  - edges
---

# Edges and Types

Edges represent relationships between nodes. Each edge has a type, direction, and can have properties.

## Creating Edges

```sql
-- Create an edge between existing nodes
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
INSERT (a)-[:KNOWS]->(b)

-- Create an edge with properties
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
INSERT (a)-[:KNOWS {since: 2020, strength: 'close'}]->(b)
```

## Edge Direction

Edges have a direction (source -> target):

```sql
-- Outgoing edges from Alice
MATCH (a:Person {name: 'Alice'})-[:KNOWS]->(friend)
RETURN friend.name

-- Incoming edges to Bob
MATCH (person)-[:KNOWS]->(b:Person {name: 'Bob'})
RETURN person.name

-- Either direction
MATCH (a:Person {name: 'Alice'})-[:KNOWS]-(connected)
RETURN connected.name
```

## Edge Types

Edge types categorize relationships:

```sql
-- Different relationship types
INSERT (alice)-[:KNOWS]->(bob)
INSERT (alice)-[:WORKS_WITH]->(carol)
INSERT (alice)-[:MANAGES]->(dave)

-- Query specific types
MATCH (a:Person)-[:MANAGES]->(employee)
RETURN a.name AS manager, employee.name AS employee
```

## Updating Edges

```sql
-- Update edge properties
MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
SET r.strength = 'best friend'
```

## Deleting Edges

```sql
-- Delete a specific edge
MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
DELETE r

-- Delete all edges of a type
MATCH ()-[r:KNOWS]->()
DELETE r
```
