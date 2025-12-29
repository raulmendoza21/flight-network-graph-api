"""
Servidor Flask para ejecutar la API localmente.
Ejecutar con: python app.py
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Añadir path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.graph import FlightGraph
from utils.helpers import load_json_file, get_data_path

app = Flask(__name__, static_folder='frontend')
CORS(app)  # Permitir peticiones desde el frontend

# Inicializar el grafo
graph = FlightGraph()

def init_graph():
    """Inicializa el grafo con los datos."""
    airports = load_json_file(get_data_path('airports.json'))
    flights = load_json_file(get_data_path('flights.json'))
    graph.load_data(airports, flights)

# Inicializar al arrancar
init_graph()


# Servir frontend
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')


# API Endpoints
@app.route('/airports', methods=['GET'])
def get_airports():
    return jsonify({'airports': graph.get_all_airports()})


@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(graph.get_graph_stats())


@app.route('/shortest-path', methods=['GET'])
def shortest_path():
    origin = request.args.get('origin', '').upper()
    destination = request.args.get('destination', '').upper()
    
    if not origin or not destination:
        return jsonify({'error': 'origin and destination required'}), 400
    
    path = graph.shortest_path(origin, destination)
    distance = graph.shortest_path_distance(origin, destination)
    
    if path is None:
        return jsonify({'error': 'No path found'}), 404
    
    return jsonify({
        'origin': origin,
        'destination': destination,
        'path': path,
        'distance': distance,
        'stops': len(path) - 2
    })


@app.route('/all-paths', methods=['GET'])
def all_paths():
    origin = request.args.get('origin', '').upper()
    destination = request.args.get('destination', '').upper()
    max_length = int(request.args.get('max_length', 5))
    
    if not origin or not destination:
        return jsonify({'error': 'origin and destination required'}), 400
    
    paths = graph.all_paths(origin, destination, max_length)
    
    return jsonify({
        'origin': origin,
        'destination': destination,
        'total_paths': len(paths),
        'paths': paths
    })


@app.route('/hubs', methods=['GET'])
def get_hubs():
    top_n = int(request.args.get('top', 5))
    return jsonify({'hubs': graph.get_hubs(top_n)})


@app.route('/isolated', methods=['GET'])
def get_isolated():
    return jsonify({'isolated_airports': graph.get_isolated_nodes()})


@app.route('/connections', methods=['GET'])
def get_connections():
    airport = request.args.get('airport', '').upper()
    
    if not airport:
        return jsonify({'error': 'airport required'}), 400
    
    connections = graph.get_connections(airport)
    
    return jsonify({
        'airport': airport,
        'connections': connections,
        'total': len(connections)
    })


@app.route('/by-degree', methods=['GET'])
def get_by_degree():
    degree = request.args.get('degree')
    
    if degree is None:
        return jsonify({'error': 'degree required'}), 400
    
    airports = graph.get_nodes_by_degree(int(degree))
    
    return jsonify({
        'degree': int(degree),
        'airports': airports,
        'total': len(airports)
    })


@app.route('/clusters', methods=['GET'])
def get_clusters():
    clusters = graph.get_clusters()
    return jsonify({
        'total_clusters': len(clusters),
        'clusters': clusters
    })


@app.route('/longest-path', methods=['GET'])
def longest_path():
    origin = request.args.get('origin', '').upper()
    destination = request.args.get('destination', '').upper()
    
    if not origin or not destination:
        return jsonify({'error': 'origin and destination required'}), 400
    
    path = graph.longest_path(origin, destination)
    
    if path is None:
        return jsonify({'error': 'No path found'}), 404
    
    return jsonify({
        'origin': origin,
        'destination': destination,
        'path': path,
        'length': len(path)
    })


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Flight Network Graph API")
    print("=" * 50)
    print(f"📊 Grafo cargado: {graph.graph.number_of_nodes()} aeropuertos, {graph.graph.number_of_edges()} vuelos")
    print(f"🌐 API: http://localhost:5000")
    print(f"🖥️  Frontend: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
