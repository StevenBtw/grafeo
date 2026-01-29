"""GraphQL implementation of transaction tests.

Tests transaction commit, rollback, and isolation using GraphQL syntax.
"""

import pytest
from tests.python.bases.test_transactions import BaseTransactionsTest


def execute_graphql(db, query: str):
    """Execute GraphQL query, skip if not supported."""
    try:
        return db.execute_graphql(query)
    except AttributeError:
        pytest.skip("GraphQL support not available in this build")
    except NotImplementedError:
        pytest.skip("GraphQL not implemented")


class TestGraphQLTransactions(BaseTransactionsTest):
    """GraphQL implementation of transaction tests.

    Note: Uses begin_transaction() with GraphQL queries.
    """

    def insert_query(self, labels: list[str], props: dict) -> str:
        """Return GraphQL create mutation."""
        label = labels[0] if labels else "Node"
        args = ", ".join(
            f'{k}: "{v}"' if isinstance(v, str) else f"{k}: {v}"
            for k, v in props.items()
        )
        return f"""
            mutation {{
                create{label}({args}) {{
                    id
                }}
            }}
        """

    def match_by_prop_query(self, label: str, prop: str, value) -> str:
        """Return GraphQL query."""
        val = f'"{value}"' if isinstance(value, str) else value
        return f"""
            query {{
                {label.lower()}({prop}: {val}) {{
                    id
                }}
            }}
        """

    def count_query(self, label: str) -> str:
        """Return GraphQL count query."""
        return f"""
            query {{
                {label.lower()}Count
            }}
        """

    def execute_in_transaction(self, tx, query: str):
        """Execute query in transaction context."""
        try:
            return tx.execute_graphql(query)
        except AttributeError:
            pytest.skip("GraphQL support not available")

    def execute_query(self, db, query: str):
        """Execute query on database."""
        return execute_graphql(db, query)
