---
title: Aliases & Fragments
description: Advanced GraphQL query composition with aliases and fragments.
tags:
  - graphql
  - aliases
  - fragments
---

# Aliases & Fragments

This guide covers advanced GraphQL query composition using aliases, named fragments, and inline fragments.

## Aliases

Aliases let you rename fields in the result or query the same type multiple times:

### Renaming Fields

```graphql
{
  Person(name: "Alice") {
    fullName: name
    yearsOld: age
  }
}
```

Returns `fullName` and `yearsOld` instead of `name` and `age`.

### Multiple Queries

Query the same type with different filters using aliases:

```graphql
{
  alice: Person(name: "Alice") {
    name
    age
  }
  bob: Person(name: "Bob") {
    name
    age
  }
}
```

### Aliasing Nested Fields

```graphql
{
  Person(name: "Alice") {
    name
    closeFriends: friends {
      name
    }
  }
}
```

## Named Fragments

Fragments let you define reusable sets of fields:

### Defining and Using Fragments

```graphql
query {
  Person(name: "Alice") {
    ...PersonFields
  }
}

fragment PersonFields on Person {
  name
  age
  email
}
```

The fragment's fields are included wherever the spread (`...PersonFields`) appears.

### Fragments Across Multiple Queries

```graphql
query {
  alice: Person(name: "Alice") {
    ...PersonInfo
  }
  bob: Person(name: "Bob") {
    ...PersonInfo
  }
}

fragment PersonInfo on Person {
  name
  age
  city
}
```

## Inline Fragments

Inline fragments apply a type condition directly in the selection set:

```graphql
{
  Person {
    name
    ... on Employee {
      department
      salary
    }
  }
}
```

This returns `department` and `salary` only for nodes that also have the `Employee` label.

### Without Type Condition

Inline fragments can also be used without a type condition for grouping with directives:

```graphql
{
  Person {
    name
    ... @include(if: true) {
      age
      email
    }
  }
}
```

## Directives

Grafeo supports standard GraphQL directives:

### @include

Conditionally include fields:

```graphql
query GetPerson($withAge: Boolean!) {
  Person(name: "Alice") {
    name
    age @include(if: $withAge)
  }
}
```

### @skip

Conditionally skip fields:

```graphql
query GetPerson($hideEmail: Boolean!) {
  Person(name: "Alice") {
    name
    email @skip(if: $hideEmail)
  }
}
```

## Python Example

```python
import grafeo

db = grafeo.GrafeoDB()

# Create data
db.execute("INSERT (:Person {name: 'Alice', age: 30, city: 'Seattle'})")
db.execute("INSERT (:Person {name: 'Bob', age: 25, city: 'Portland'})")

# Using aliases
result = db.execute_graphql("""
{
  alice: Person(name: "Alice") {
    name
    age
  }
  bob: Person(name: "Bob") {
    name
    age
  }
}
""")
for row in result:
    print(row)

# Using fragments
result = db.execute_graphql("""
query {
  Person(name: "Alice") {
    ...PersonDetails
  }
}

fragment PersonDetails on Person {
  name
  age
  city
}
""")
for row in result:
    print(row)
```

## Feature Summary

| Feature | Syntax | Description |
|---------|--------|-------------|
| Field alias | `alias: field` | Rename a field in the result |
| Query alias | `alias: Type(args) { ... }` | Query same type multiple times |
| Named fragment | `fragment Name on Type { ... }` | Reusable field set |
| Fragment spread | `...FragmentName` | Include a named fragment |
| Inline fragment | `... on Type { ... }` | Conditional field inclusion |
| @include | `@include(if: $var)` | Conditionally include |
| @skip | `@skip(if: $var)` | Conditionally skip |
