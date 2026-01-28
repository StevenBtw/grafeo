---
title: Relationships
description: Query graph relationships using nested GraphQL selections.
tags:
  - graphql
  - relationships
  - traversals
---

# Relationships

This guide covers querying graph relationships using nested field selections in GraphQL.

## Nested Selections

In Graphos, nested fields in a GraphQL query map to edge traversals. The field name corresponds to the edge type:

```graphql
{
  Person(name: "Alice") {
    name
    friends {
      name
      age
    }
  }
}
```

This query:

1. Finds nodes with label `Person` where `name = "Alice"`
2. Returns the `name` property
3. Traverses outgoing `friends` edges
4. Returns `name` and `age` of connected nodes

## How Nesting Maps to the Graph

| GraphQL | Graph Operation |
|---------|-----------------|
| Root field name (`Person`) | Node label filter |
| Scalar field (`name`) | Property access |
| Object field (`friends { ... }`) | Edge traversal (outgoing) |
| Arguments on nested field | Filter on target nodes |

## Multi-Level Nesting

Query multiple levels of relationships:

```graphql
{
  Person(name: "Alice") {
    name
    friends {
      name
      friends {
        name
      }
    }
  }
}
```

This traverses two hops: Alice's friends, then their friends.

## Filtering Nested Results

Apply arguments to nested fields to filter related nodes:

```graphql
{
  Person(name: "Alice") {
    name
    friends(age: 30) {
      name
      age
    }
  }
}
```

## Multiple Relationship Types

Query different relationship types in the same query:

```graphql
{
  Person(name: "Alice") {
    name
    friends {
      name
    }
    colleagues {
      name
      company
    }
  }
}
```

## Python Example

```python
import graphos

db = graphos.GraphosDB()

# Create a social graph
db.execute("INSERT (:Person {name: 'Alice', age: 30})")
db.execute("INSERT (:Person {name: 'Bob', age: 25})")
db.execute("INSERT (:Person {name: 'Charlie', age: 35})")
db.execute("""
    MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
    INSERT (a)-[:friends]->(b)
""")
db.execute("""
    MATCH (b:Person {name: 'Bob'}), (c:Person {name: 'Charlie'})
    INSERT (b)-[:friends]->(c)
""")

# Query relationships
result = db.execute_graphql("""
{
  Person(name: "Alice") {
    name
    friends {
      name
      friends {
        name
      }
    }
  }
}
""")
for row in result:
    print(row)
```

## Rust Example

```rust
use graphos_engine::GraphosDB;

let db = GraphosDB::new_in_memory();

// Create data
db.execute("INSERT (:Person {name: 'Alice'})").unwrap();
db.execute("INSERT (:Person {name: 'Bob'})").unwrap();
db.execute(
    "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) INSERT (a)-[:friends]->(b)"
).unwrap();

// Query with nested relationships
let result = db.execute_graphql(r#"
{
  Person(name: "Alice") {
    name
    friends {
      name
    }
  }
}
"#).unwrap();
```
