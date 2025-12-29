"""
Lambda handler para operaciones sobre el grafo de vuelos.
"""
import json
import sys
import os

# Añadir el path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.graph import FlightGraph
from utils.helpers import load_json_file, get_data_path, format_response, parse_request_body


# Inicializar el grafo
graph = FlightGraph()


def init_graph():
    """Inicializa el grafo con los datos de aeropuertos y vuelos."""
    airports = load_json_file(get_data_path('airports.json'))
    flights = load_json_file(get_data_path('flights.json'))
    graph.load_data(airports, flights)


def lambda_handler(event, context):
    """Handler principal de la Lambda."""
    
    # Inicializar grafo si está vacío
    if graph.graph.number_of_nodes() == 0:
        init_graph()
    
    # Obtener la operación del path
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    query_params = event.get('queryStringParameters', {}) or {}
    
    try:
        # GET /airports - Listar todos los aeropuertos
        if path == '/airports' and method == 'GET':
            return format_response(200, {
                'airports': graph.get_all_airports()
            })
        
        # GET /stats - Estadísticas del grafo
        elif path == '/stats' and method == 'GET':
            return format_response(200, graph.get_graph_stats())
        
        # GET /shortest-path?origin=X&destination=Y
        elif path == '/shortest-path' and method == 'GET':
            origin = query_params.get('origin')
            destination = query_params.get('destination')
            
            if not origin or not destination:
                return format_response(400, {'error': 'origin and destination required'})
            
            path_result = graph.shortest_path(origin.upper(), destination.upper())
            distance = graph.shortest_path_distance(origin.upper(), destination.upper())
            
            if path_result is None:
                return format_response(404, {'error': 'No path found'})
            
            return format_response(200, {
                'origin': origin.upper(),
                'destination': destination.upper(),
                'path': path_result,
                'distance': distance,
                'stops': len(path_result) - 2
            })
        
        # GET /all-paths?origin=X&destination=Y
        elif path == '/all-paths' and method == 'GET':
            origin = query_params.get('origin')
            destination = query_params.get('destination')
            max_length = int(query_params.get('max_length', 5))
            
            if not origin or not destination:
                return format_response(400, {'error': 'origin and destination required'})
            
            paths = graph.all_paths(origin.upper(), destination.upper(), max_length)
            
            return format_response(200, {
                'origin': origin.upper(),
                'destination': destination.upper(),
                'total_paths': len(paths),
                'paths': paths
            })
        
        # GET /hubs?top=N
        elif path == '/hubs' and method == 'GET':
            top_n = int(query_params.get('top', 5))
            return format_response(200, {
                'hubs': graph.get_hubs(top_n)
            })
        
        # GET /isolated
        elif path == '/isolated' and method == 'GET':
            return format_response(200, {
                'isolated_airports': graph.get_isolated_nodes()
            })
        
        # GET /connections?airport=X
        elif path == '/connections' and method == 'GET':
            airport = query_params.get('airport')
            
            if not airport:
                return format_response(400, {'error': 'airport required'})
            
            connections = graph.get_connections(airport.upper())
            
            return format_response(200, {
                'airport': airport.upper(),
                'connections': connections,
                'total': len(connections)
            })
        
        # GET /by-degree?degree=N
        elif path == '/by-degree' and method == 'GET':
            degree = query_params.get('degree')
            
            if degree is None:
                return format_response(400, {'error': 'degree required'})
            
            airports = graph.get_nodes_by_degree(int(degree))
            
            return format_response(200, {
                'degree': int(degree),
                'airports': airports,
                'total': len(airports)
            })
        
        # GET /clusters
        elif path == '/clusters' and method == 'GET':
            clusters = graph.get_clusters()
            return format_response(200, {
                'total_clusters': len(clusters),
                'clusters': clusters
            })
        
        # GET /longest-path?origin=X&destination=Y
        elif path == '/longest-path' and method == 'GET':
            origin = query_params.get('origin')
            destination = query_params.get('destination')
            
            if not origin or not destination:
                return format_response(400, {'error': 'origin and destination required'})
            
            path_result = graph.longest_path(origin.upper(), destination.upper())
            
            if path_result is None:
                return format_response(404, {'error': 'No path found'})
            
            return format_response(200, {
                'origin': origin.upper(),
                'destination': destination.upper(),
                'path': path_result,
                'length': len(path_result)
            })
        
        # Ruta no encontrada
        else:
            return format_response(404, {'error': 'Endpoint not found'})
    
    except Exception as e:
        return format_response(500, {'error': str(e)})