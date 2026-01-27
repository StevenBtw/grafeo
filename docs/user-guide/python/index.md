---
title: Python API
description: Using Graphos from Python.
---

# Python API

Graphos provides first-class Python support through the `pygraphos` package.

## Quick Start

```python
import graphos

# Create a database
db = graphos.Database()

# Execute queries
with db.session() as session:
    session.execute("INSERT (:Person {name: 'Alice'})")

    result = session.execute("MATCH (p:Person) RETURN p.name")
    for row in result:
        print(row['p.name'])
```

## Sections

<div class="grid cards" markdown>

-   **[Database Operations](database.md)**

    ---

    Creating and configuring databases.

-   **[Working with Nodes](nodes.md)**

    ---

    Creating, reading, updating, and deleting nodes.

-   **[Working with Edges](edges.md)**

    ---

    Managing relationships between nodes.

-   **[Transactions](transactions.md)**

    ---

    Transaction management and isolation.

-   **[Query Results](results.md)**

    ---

    Working with query results.

</div>
