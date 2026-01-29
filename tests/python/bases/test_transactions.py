"""Base class for transaction tests.

This module defines test logic for transaction commit, rollback, and isolation.
"""

from abc import ABC, abstractmethod
import pytest


class BaseTransactionsTest(ABC):
    """Abstract base class for transaction tests."""

    @abstractmethod
    def insert_query(self, labels: list[str], props: dict) -> str:
        """Return query to insert a node.

        Args:
            labels: Node labels
            props: Node properties

        Returns:
            Language-specific INSERT/CREATE query
        """
        raise NotImplementedError

    @abstractmethod
    def match_by_prop_query(self, label: str, prop: str, value) -> str:
        """Return query to match node by property.

        Args:
            label: Node label
            prop: Property name
            value: Property value

        Returns:
            Query that returns matching nodes
        """
        raise NotImplementedError

    @abstractmethod
    def count_query(self, label: str) -> str:
        """Return query to count nodes by label.

        Returns:
            Query that returns count as 'cnt'
        """
        raise NotImplementedError

    # ===== Test Methods =====

    def test_transaction_commit(self, db):
        """Test that committed transaction persists data."""
        with db.begin_transaction() as tx:
            query = self.insert_query(["Person"], {"name": "CommitTest"})
            tx.execute(query)
            tx.commit()

        # Data should be visible after commit
        match_query = self.match_by_prop_query("Person", "name", "CommitTest")
        result = db.execute(match_query)
        rows = list(result)
        assert len(rows) == 1

    def test_transaction_auto_commit(self, db):
        """Test that transactions auto-commit on context exit."""
        with db.begin_transaction() as tx:
            query = self.insert_query(["Person"], {"name": "AutoCommitTest"})
            tx.execute(query)
            # No explicit commit - should auto-commit

        # Data should be visible
        match_query = self.match_by_prop_query("Person", "name", "AutoCommitTest")
        result = db.execute(match_query)
        rows = list(result)
        assert len(rows) == 1

    def test_transaction_rollback(self, db):
        """Test that rollback discards changes."""
        # Verify database is empty for this label/prop combo
        match_query = self.match_by_prop_query("Person", "name", "RollbackTest")
        result = db.execute(match_query)
        assert len(list(result)) == 0

        # Create node and rollback
        with db.begin_transaction() as tx:
            query = self.insert_query(["Person"], {"name": "RollbackTest"})
            tx.execute(query)
            tx.rollback()

        # Data should NOT be visible after rollback
        result = db.execute(match_query)
        rows = list(result)
        assert len(rows) == 0, f"Expected 0 rows after rollback, got {len(rows)}"

    def test_transaction_is_active(self, db):
        """Test transaction is_active property."""
        tx = db.begin_transaction()
        assert tx.is_active is True

        tx.commit()
        assert tx.is_active is False

    def test_multiple_operations_in_transaction(self, db):
        """Test multiple operations in a single transaction."""
        with db.begin_transaction() as tx:
            # Create multiple nodes
            tx.execute(self.insert_query(["Person"], {"name": "Multi1", "idx": 1}))
            tx.execute(self.insert_query(["Person"], {"name": "Multi2", "idx": 2}))
            tx.execute(self.insert_query(["Person"], {"name": "Multi3", "idx": 3}))
            tx.commit()

        # All nodes should exist
        count_query = self.count_query("Person")
        result = db.execute(count_query)
        rows = list(result)
        assert rows[0]["cnt"] >= 3
