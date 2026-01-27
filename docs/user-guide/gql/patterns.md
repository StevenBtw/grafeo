---
title: Pattern Matching
description: Advanced pattern matching in GQL.
tags:
  - gql
  - patterns
---

# Pattern Matching

Pattern matching is the core of GQL. This guide covers node and edge patterns in detail.

## Node Patterns

```sql
-- Any node
(n)

-- Node with label
(p:Person)

-- Node with multiple labels
(e:Person:Employee)

-- Node with properties
(p:Person {name: 'Alice'})

-- Anonymous node (no variable)
(:Person)
```

## Edge Patterns

```sql
-- Outgoing edge
(a)-[:KNOWS]->(b)

-- Incoming edge
(a)<-[:KNOWS]-(b)

-- Either direction
(a)-[:KNOWS]-(b)

-- Any edge type
(a)-[r]->(b)

-- Edge with properties
(a)-[:KNOWS {since: 2020}]->(b)
```

## Complex Patterns

```sql
-- Chain of relationships
MATCH (a:Person)-[:KNOWS]->(b)-[:KNOWS]->(c)
RETURN a.name, b.name, c.name

-- Multiple patterns
MATCH (a:Person)-[:KNOWS]->(b), (a)-[:WORKS_AT]->(c)
RETURN a.name, b.name, c.name

-- Triangle pattern
MATCH (a)-[:KNOWS]->(b)-[:KNOWS]->(c)-[:KNOWS]->(a)
RETURN a.name, b.name, c.name
```

## Multiple Relationship Types

```sql
-- Match any of multiple types
MATCH (a)-[:KNOWS|:WORKS_WITH]->(b)
RETURN a.name, b.name

-- Match with type variable
MATCH (a)-[r:KNOWS|:WORKS_WITH]->(b)
RETURN a.name, type(r), b.name
```

## Optional Patterns

```sql
-- Return results even if pattern doesn't match
MATCH (p:Person)
OPTIONAL MATCH (p)-[:HAS_PET]->(pet)
RETURN p.name, pet.name
```
