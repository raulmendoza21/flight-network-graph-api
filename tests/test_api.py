"""
Tests para la API Lambda.
"""
import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lambdas.graph_operations import lambda_handler, init_graph, graph


@pytest.fixture(autouse=True)
def setup_graph():
    """Inicializa el grafo antes de cada test."""
    graph.graph.clear()
    init_graph()


def test_get_airports():
    """Test endpoint /airports."""
    event = {'path': '/airports', 'httpMethod': 'GET'}
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'airports' in body
    assert len(body['airports']) > 0


def test_get_stats():
    """Test endpoint /stats."""
    event = {'path': '/stats', 'httpMethod': 'GET'}
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'total_airports' in body
    assert 'total_flights' in body


def test_shortest_path():
    """Test endpoint /shortest-path."""
    event = {
        'path': '/shortest-path',
        'httpMethod': 'GET',
        'queryStringParameters': {'origin': 'MAD', 'destination': 'JFK'}
    }
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'path' in body
    assert body['origin'] == 'MAD'
    assert body['destination'] == 'JFK'


def test_shortest_path_missing_params():
    """Test /shortest-path sin parámetros."""
    event = {
        'path': '/shortest-path',
        'httpMethod': 'GET',
        'queryStringParameters': {}
    }
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 400


def test_get_hubs():
    """Test endpoint /hubs."""
    event = {
        'path': '/hubs',
        'httpMethod': 'GET',
        'queryStringParameters': {'top': '3'}
    }
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'hubs' in body
    assert len(body['hubs']) == 3


def test_get_connections():
    """Test endpoint /connections."""
    event = {
        'path': '/connections',
        'httpMethod': 'GET',
        'queryStringParameters': {'airport': 'MAD'}
    }
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'connections' in body
    assert body['airport'] == 'MAD'


def test_get_clusters():
    """Test endpoint /clusters."""
    event = {'path': '/clusters', 'httpMethod': 'GET'}
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'clusters' in body


def test_endpoint_not_found():
    """Test endpoint inexistente."""
    event = {'path': '/invalid', 'httpMethod': 'GET'}
    response = lambda_handler(event, None)
    
    assert response['statusCode'] == 404