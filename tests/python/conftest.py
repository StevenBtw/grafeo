"""Pytest fixtures for Graphos Python tests."""

import pytest
import random

# Try to import graphos
try:
    import graphos
    GRAPHOS_AVAILABLE = True
except ImportError:
    GRAPHOS_AVAILABLE = False


@pytest.fixture
def db():
    """Create a fresh in-memory GraphosDB instance."""
    if not GRAPHOS_AVAILABLE:
        pytest.skip("graphos not installed")
    return graphos.GraphosDB()


@pytest.fixture
def node_ids(db):
    """Create a test graph and return node IDs.

    Creates a random graph with 100 nodes and 300 edges for algorithm testing.
    """
    n_nodes = 100
    n_edges = 300

    node_ids = []
    for i in range(n_nodes):
        node = db.create_node(["Node"], {"index": i})
        node_ids.append(node.id)

    edges = set()
    while len(edges) < n_edges:
        src = random.choice(node_ids)
        dst = random.choice(node_ids)
        if src != dst and (src, dst) not in edges:
            db.create_edge(src, dst, "EDGE", {"weight": random.uniform(0.1, 10.0)})
            edges.add((src, dst))

    return node_ids
