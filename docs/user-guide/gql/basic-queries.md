---
title: Basic Queries
description: Learn basic GQL queries with MATCH and RETURN.
tags:
  - gql
  - queries
---

# Basic Queries

This guide covers the fundamentals of querying graphs with GQL.

## MATCH Clause

The `MATCH` clause finds patterns in the graph:

```sql
-- Match all nodes
MATCH (n)
RETURN n

-- Match nodes with a label
MATCH (p:Person)
RETURN p

-- Match nodes with properties
MATCH (p:Person {name: 'Alice'})
RETURN p
```

## RETURN Clause

The `RETURN` clause specifies what to return:

```sql
-- Return entire nodes
MATCH (p:Person)
RETURN p

-- Return specific properties
MATCH (p:Person)
RETURN p.name, p.age

-- Return with aliases
MATCH (p:Person)
RETURN p.name AS name, p.age AS age
```

## Combining MATCH and RETURN

```sql
-- Find all people and return their names
MATCH (p:Person)
RETURN p.name

-- Find people over 30
MATCH (p:Person)
WHERE p.age > 30
RETURN p.name, p.age

-- Find Alice's friends
MATCH (a:Person {name: 'Alice'})-[:KNOWS]->(friend)
RETURN friend.name
```

## Ordering Results

```sql
-- Order by property
MATCH (p:Person)
RETURN p.name, p.age
ORDER BY p.age

-- Descending order
MATCH (p:Person)
RETURN p.name, p.age
ORDER BY p.age DESC

-- Multiple sort keys
MATCH (p:Person)
RETURN p.name, p.age
ORDER BY p.age DESC, p.name ASC
```

## Limiting Results

```sql
-- Return first 10 results
MATCH (p:Person)
RETURN p.name
LIMIT 10

-- Skip and limit (pagination)
MATCH (p:Person)
RETURN p.name
ORDER BY p.name
SKIP 20 LIMIT 10
```

## DISTINCT Results

```sql
-- Remove duplicates
MATCH (p:Person)-[:LIVES_IN]->(c:City)
RETURN DISTINCT c.name
```
