"""SPARQL pattern tests.

Tests SPARQL queries against the RDF model.
"""

import pytest


# Try to import grafeo
try:
    from grafeo import GrafeoDB
    GRAFEO_AVAILABLE = True
except ImportError:
    GRAFEO_AVAILABLE = False


pytestmark = pytest.mark.skipif(
    not GRAFEO_AVAILABLE,
    reason="Grafeo Python bindings not installed"
)


class TestSPARQLSelect:
    """Test SPARQL SELECT queries."""

    def setup_method(self):
        """Create a database with RDF test data."""
        self.db = GrafeoDB()
        self._setup_test_data()

    def _setup_test_data(self):
        """Create RDF-like test data."""
        self.alice = self.db.create_node(["Resource"], {
            "uri": "http://example.org/person/alice",
            "rdf:type": "http://xmlns.com/foaf/0.1/Person",
            "foaf:name": "Alice",
            "foaf:age": 30
        })

        self.bob = self.db.create_node(["Resource"], {
            "uri": "http://example.org/person/bob",
            "rdf:type": "http://xmlns.com/foaf/0.1/Person",
            "foaf:name": "Bob",
            "foaf:age": 25
        })

        self.charlie = self.db.create_node(["Resource"], {
            "uri": "http://example.org/person/charlie",
            "rdf:type": "http://xmlns.com/foaf/0.1/Person",
            "foaf:name": "Charlie",
            "foaf:age": 35
        })

        self.db.create_edge(self.alice.id, self.bob.id, "foaf:knows", {})
        self.db.create_edge(self.bob.id, self.charlie.id, "foaf:knows", {})

    def _execute_sparql(self, query: str):
        """Execute SPARQL query, skip if not supported."""
        try:
            return self.db.execute_sparql(query)
        except AttributeError:
            pytest.skip("SPARQL support not available")
        except NotImplementedError:
            pytest.skip("SPARQL not implemented")

    def test_sparql_select_all(self):
        """SPARQL: SELECT * WHERE { ?s ?p ?o }"""
        result = self._execute_sparql("""
            SELECT * WHERE {
                ?s ?p ?o
            }
        """)
        rows = list(result)
        assert len(rows) > 0

    def test_sparql_select_with_type(self):
        """SPARQL: SELECT with rdf:type filter."""
        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT ?name WHERE {
                ?person rdf:type foaf:Person .
                ?person foaf:name ?name .
            }
        """)
        rows = list(result)
        # Should find Alice, Bob, and Charlie
        assert len(rows) == 3

    def test_sparql_select_with_filter(self):
        """SPARQL: SELECT with FILTER."""
        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?name ?age WHERE {
                ?person foaf:name ?name .
                ?person foaf:age ?age .
                FILTER(?age > 28)
            }
        """)
        rows = list(result)
        # Alice (30) and Charlie (35) match
        assert len(rows) == 2

    def test_sparql_select_relationship(self):
        """SPARQL: SELECT with relationship pattern."""
        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?name1 ?name2 WHERE {
                ?p1 foaf:knows ?p2 .
                ?p1 foaf:name ?name1 .
                ?p2 foaf:name ?name2 .
            }
        """)
        rows = list(result)
        # Alice->Bob and Bob->Charlie
        assert len(rows) == 2

    def test_sparql_optional(self):
        """SPARQL: SELECT with OPTIONAL."""
        # Create a person without email
        self.db.create_node(["Resource"], {
            "uri": "http://example.org/person/diana",
            "rdf:type": "http://xmlns.com/foaf/0.1/Person",
            "foaf:name": "Diana",
            # No email
        })

        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?name ?email WHERE {
                ?person foaf:name ?name .
                OPTIONAL { ?person foaf:mbox ?email }
            }
        """)
        rows = list(result)
        # Should include Diana with NULL email
        assert len(rows) >= 4

    def test_sparql_order_by(self):
        """SPARQL: SELECT with ORDER BY."""
        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?name ?age WHERE {
                ?person foaf:name ?name .
                ?person foaf:age ?age .
            }
            ORDER BY ?age
        """)
        rows = list(result)
        # Bob (25) should be first
        if len(rows) >= 1:
            assert rows[0].get("age") == 25 or rows[0].get("name") == "Bob"

    def test_sparql_limit(self):
        """SPARQL: SELECT with LIMIT."""
        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?name WHERE {
                ?person foaf:name ?name .
            }
            LIMIT 2
        """)
        rows = list(result)
        assert len(rows) == 2


class TestSPARQLAggregate:
    """Test SPARQL aggregate queries."""

    def setup_method(self):
        """Create a database with RDF test data."""
        self.db = GrafeoDB()
        self._setup_test_data()

    def _setup_test_data(self):
        """Create RDF-like test data."""
        for name, age in [("Alice", 30), ("Bob", 25), ("Charlie", 35)]:
            self.db.create_node(["Resource"], {
                "uri": f"http://example.org/person/{name.lower()}",
                "rdf:type": "http://xmlns.com/foaf/0.1/Person",
                "foaf:name": name,
                "foaf:age": age
            })

    def _execute_sparql(self, query: str):
        """Execute SPARQL query, skip if not supported."""
        try:
            return self.db.execute_sparql(query)
        except AttributeError:
            pytest.skip("SPARQL support not available")
        except NotImplementedError:
            pytest.skip("SPARQL not implemented")

    def test_sparql_count(self):
        """SPARQL: COUNT aggregate."""
        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT (COUNT(?person) AS ?count) WHERE {
                ?person foaf:name ?name .
            }
        """)
        rows = list(result)
        assert len(rows) == 1
        assert rows[0]["count"] == 3

    def test_sparql_sum_avg(self):
        """SPARQL: SUM and AVG aggregates."""
        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT (SUM(?age) AS ?total) (AVG(?age) AS ?average) WHERE {
                ?person foaf:age ?age .
            }
        """)
        rows = list(result)
        assert rows[0]["total"] == 90  # 30 + 25 + 35
        assert abs(rows[0]["average"] - 30.0) < 0.01

    def test_sparql_min_max(self):
        """SPARQL: MIN and MAX aggregates."""
        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT (MIN(?age) AS ?youngest) (MAX(?age) AS ?oldest) WHERE {
                ?person foaf:age ?age .
            }
        """)
        rows = list(result)
        assert rows[0]["youngest"] == 25
        assert rows[0]["oldest"] == 35

    def test_sparql_group_by(self):
        """SPARQL: GROUP BY."""
        # Add city property
        self.db.create_node(["Resource"], {
            "uri": "http://example.org/person/diana",
            "foaf:name": "Diana",
            "foaf:city": "NYC"
        })

        result = self._execute_sparql("""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>

            SELECT ?city (COUNT(?person) AS ?count) WHERE {
                ?person foaf:city ?city .
            }
            GROUP BY ?city
        """)
        rows = list(result)
        # Should have city groups
        assert len(rows) >= 1
