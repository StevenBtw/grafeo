---
title: Properties
description: Property types and values in Grafeo.
tags:
  - data-model
  - properties
---

# Properties

Properties are key-value pairs stored on nodes and edges. Grafeo supports a rich set of property types.

## Supported Types

| Type | Example | Description |
|------|---------|-------------|
| `Boolean` | `true`, `false` | True/false values |
| `Int64` | `42`, `-100` | 64-bit signed integers |
| `Float64` | `3.14`, `-0.5` | 64-bit floating point |
| `String` | `'hello'` | UTF-8 text |
| `List` | `[1, 2, 3]` | Ordered collection |
| `Map` | `{key: 'value'}` | Key-value collection |
| `Date` | `'2024-01-15'` | Calendar date |
| `DateTime` | `'2024-01-15T10:30:00Z'` | Date and time |
| `Null` | `null` | Absence of value |

## Using Properties

### Setting Properties

```sql
INSERT (:Product {
    name: 'Widget',
    price: 29.99,
    in_stock: true,
    tags: ['electronics', 'sale'],
    metadata: {category: 'gadgets', sku: 'WDG-001'}
})
```

### Querying Properties

```sql
-- Simple property access
MATCH (p:Product)
RETURN p.name, p.price

-- Property comparisons
MATCH (p:Product)
WHERE p.price < 50 AND p.in_stock = true
RETURN p.name

-- List operations
MATCH (p:Product)
WHERE 'sale' IN p.tags
RETURN p.name
```

### Updating Properties

```sql
-- Set a property
MATCH (p:Product {name: 'Widget'})
SET p.price = 24.99

-- Set multiple properties
MATCH (p:Product {name: 'Widget'})
SET p.price = 24.99, p.on_sale = true

-- Remove a property
MATCH (p:Product {name: 'Widget'})
REMOVE p.on_sale
```

## Null Handling

```sql
-- Check for null
MATCH (p:Person)
WHERE p.email IS NULL
RETURN p.name

-- Check for not null
MATCH (p:Person)
WHERE p.email IS NOT NULL
RETURN p.name, p.email

-- Coalesce null values
MATCH (p:Person)
RETURN p.name, coalesce(p.email, 'no email') AS email
```
