"""
Tests para el modelo del grafo.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.graph import FlightGraph


@pytest.fixture
def sample_graph():
    """Crea un grafo de ejemplo para tests."""
    graph = FlightGraph()
    
    # Añadir aeropuertos
    graph.add_airport("MAD", "Madrid", "Madrid", "Spain")
    graph.add_airport("BCN", "Barcelona", "Barcelona", "Spain")
    graph.add_airport("LHR", "London", "London", "UK")
    graph.add_airport("JFK", "New York", "New York", "USA")
    graph.add_airport("ISO", "Isolated", "Isolated", "Test")  # Sin conexiones
    
    # Añadir vuelos
    graph.add_flight("MAD", "BCN", 500)
    graph.add_flight("MAD", "LHR", 1200)
    graph.add_flight("LHR", "JFK", 5500)
    
    return graph


def test_add_airport(sample_graph):
    """Test añadir aeropuerto."""
    assert sample_graph.graph.number_of_nodes() == 5


def test_add_flight(sample_graph):
    """Test añadir vuelo."""
    assert sample_graph.graph.number_of_edges() == 3


def test_shortest_path(sample_graph):
    """Test camino más corto."""
    path = sample_graph.shortest_path("MAD", "JFK")
    assert path == ["MAD", "LHR", "JFK"]


def test_shortest_path_no_route(sample_graph):
    """Test camino cuando no existe ruta."""
    path = sample_graph.shortest_path("MAD", "ISO")
    assert path is None


def test_get_connections(sample_graph):
    """Test obtener conexiones de un aeropuerto."""
    connections = sample_graph.get_connections("MAD")
    assert set(connections) == {"BCN", "LHR"}


def test_get_isolated_nodes(sample_graph):
    """Test obtener nodos aislados."""
    isolated = sample_graph.get_isolated_nodes()
    assert isolated == ["ISO"]


def test_get_hubs(sample_graph):
    """Test obtener hubs (más conectados)."""
    hubs = sample_graph.get_hubs(2)
    assert len(hubs) == 2
    assert hubs[0]["airport"] == "MAD"
    assert hubs[0]["connections"] == 2


def test_get_nodes_by_degree(sample_graph):
    """Test filtrar por grado de conexión."""
    nodes = sample_graph.get_nodes_by_degree(2)
    assert "MAD" in nodes
    assert "LHR" in nodes


def test_all_paths(sample_graph):
    """Test obtener todos los caminos."""
    paths = sample_graph.all_paths("MAD", "JFK")
    assert len(paths) == 1
    assert paths[0] == ["MAD", "LHR", "JFK"]


def test_graph_stats(sample_graph):
    """Test estadísticas del grafo."""
    stats = sample_graph.get_graph_stats()
    assert stats["total_airports"] == 5
    assert stats["total_flights"] == 3
    assert stats["is_connected"] == False  # ISO está aislado