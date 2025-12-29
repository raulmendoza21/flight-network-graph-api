"""
Modelo del grafo de aeropuertos y vuelos.
Usa NetworkX para operaciones sobre grafos.
"""
import networkx as nx
from typing import List, Dict, Optional


class FlightGraph:
    """Clase que representa el grafo de vuelos entre aeropuertos."""
    
    def __init__(self):
        self.graph = nx.Graph()
    
    def add_airport(self, code: str, name: str, city: str, country: str) -> None:
        """Añade un aeropuerto (nodo) al grafo."""
        self.graph.add_node(code, name=name, city=city, country=country)
    
    def add_flight(self, origin: str, destination: str, distance: int) -> None:
        """Añade un vuelo (arista) entre dos aeropuertos."""
        self.graph.add_edge(origin, destination, weight=distance)
    
    def load_data(self, airports: List[Dict], flights: List[Dict]) -> None:
        """Carga los datos de aeropuertos y vuelos al grafo."""
        for airport in airports:
            self.add_airport(
                airport["code"],
                airport["name"],
                airport["city"],
                airport["country"]
            )
        for flight in flights:
            self.add_flight(
                flight["origin"],
                flight["destination"],
                flight["distance"]
            )
    
    def shortest_path(self, origin: str, destination: str) -> Optional[List[str]]:
        """Devuelve el camino más corto entre dos aeropuertos."""
        try:
            return nx.shortest_path(self.graph, origin, destination, weight="weight")
        except nx.NetworkXNoPath:
            return None
    
    def shortest_path_distance(self, origin: str, destination: str) -> Optional[int]:
        """Devuelve la distancia del camino más corto."""
        try:
            return nx.shortest_path_length(self.graph, origin, destination, weight="weight")
        except nx.NetworkXNoPath:
            return None
    
    def all_paths(self, origin: str, destination: str, max_length: int = 5) -> List[List[str]]:
        """Devuelve todos los caminos entre dos aeropuertos (limitado)."""
        try:
            paths = list(nx.all_simple_paths(self.graph, origin, destination, cutoff=max_length))
            return paths
        except nx.NetworkXNoPath:
            return []
    
    def get_hubs(self, top_n: int = 5) -> List[Dict]:
        """Devuelve los aeropuertos con más conexiones."""
        degrees = sorted(self.graph.degree(), key=lambda x: x[1], reverse=True)
        return [{"airport": code, "connections": degree} for code, degree in degrees[:top_n]]
    
    def get_isolated_nodes(self) -> List[str]:
        """Devuelve aeropuertos sin conexiones."""
        return list(nx.isolates(self.graph))
    
    def get_connections(self, airport: str) -> List[str]:
        """Devuelve los aeropuertos conectados directamente."""
        if airport in self.graph:
            return list(self.graph.neighbors(airport))
        return []
    
    def get_nodes_by_degree(self, degree: int) -> List[str]:
        """Devuelve aeropuertos con un número específico de conexiones."""
        return [node for node, deg in self.graph.degree() if deg == degree]
    
    def get_clusters(self) -> List[List[str]]:
        """Detecta comunidades/clusters en el grafo."""
        communities = nx.community.greedy_modularity_communities(self.graph)
        return [list(community) for community in communities]
    
    def longest_path(self, origin: str, destination: str) -> Optional[List[str]]:
        """Devuelve el camino más largo sin ciclos (aproximado)."""
        try:
            all_paths = list(nx.all_simple_paths(self.graph, origin, destination, cutoff=10))
            if not all_paths:
                return None
            return max(all_paths, key=len)
        except nx.NetworkXNoPath:
            return None
    
    def get_all_airports(self) -> List[Dict]:
        """Devuelve todos los aeropuertos con su información."""
        airports = []
        for node in self.graph.nodes(data=True):
            airports.append({
                "code": node[0],
                "name": node[1].get("name", ""),
                "city": node[1].get("city", ""),
                "country": node[1].get("country", "")
            })
        return airports
    
    def get_graph_stats(self) -> Dict:
        """Devuelve estadísticas generales del grafo."""
        return {
            "total_airports": self.graph.number_of_nodes(),
            "total_flights": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "is_connected": nx.is_connected(self.graph)
        }