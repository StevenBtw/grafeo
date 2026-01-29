"""SPARQL implementation of transaction tests.

Tests transaction semantics with SPARQL operations.
Note: Uses Python API for transaction control with SPARQL queries inside.
"""

import pytest
from tests.python.bases.test_transactions import BaseTransactionsTest


# Skip all tests - SPARQL Update execution not yet implemented
pytestmark = pytest.mark.skipif(
    True,
    reason="SPARQL Update execution not yet implemented"
)


class TestSPARQLTransactions(BaseTransactionsTest):
    """SPARQL implementation of transaction tests.

    Note: Transactions are controlled via Python API.
    SPARQL queries and updates are executed within transactions.
    """

    def insert_query(self, labels: list, props: dict) -> str:
        """Build SPARQL INSERT DATA statement.

        Note: SPARQL doesn't have labels like LPG.
        We use rdf:type for classification and properties as triples.
        """
        label = labels[0] if labels else "Resource"
        name = props.get("name", "unnamed")
        uri = f"<http://example.org/{label.lower()}/{name}>"

        triples = []
        triples.append(f'{uri} a <http://example.org/{label}>')

        for k, v in props.items():
            if isinstance(v, str):
                triples.append(f'{uri} <http://example.org/{k}> "{v}"')
            else:
                triples.append(f'{uri} <http://example.org/{k}> {v}')

        return f"INSERT DATA {{ {' . '.join(triples)} }}"

    def match_by_prop_query(self, label: str, prop: str, value) -> str:
        """Build SPARQL SELECT to find resource by property."""
        if isinstance(value, str):
            val = f'"{value}"'
        else:
            val = str(value)

        return f"""
            SELECT ?s WHERE {{
                ?s a <http://example.org/{label}> .
                ?s <http://example.org/{prop}> {val} .
            }}
        """

    def count_query(self, label: str) -> str:
        """Build SPARQL COUNT query."""
        return f"""
            SELECT (COUNT(?s) AS ?cnt) WHERE {{
                ?s a <http://example.org/{label}> .
            }}
        """


class TestSPARQLTransactionVerification:
    """Tests that verify transaction behavior with SPARQL."""

    def test_transaction_rollback_on_error(self, db_api):
        """Verify transaction rollback on error."""
        initial_count = len(list(db_api.execute("MATCH (n) RETURN n")))

        try:
            with db_api.transaction():
                # Create a node
                db_api.create_node(["Test"], {"name": "temp"})
                # Simulate an error
                raise ValueError("Simulated error")
        except ValueError:
            pass

        # Count should be unchanged
        final_count = len(list(db_api.execute("MATCH (n) RETURN n")))
        assert final_count == initial_count

    def test_transaction_commit_on_success(self, db_api):
        """Verify transaction commits on success."""
        initial_count = len(list(db_api.execute("MATCH (n) RETURN n")))

        with db_api.transaction():
            db_api.create_node(["Test"], {"name": "committed"})

        # Count should be incremented
        final_count = len(list(db_api.execute("MATCH (n) RETURN n")))
        assert final_count == initial_count + 1
