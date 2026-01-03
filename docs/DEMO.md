# Demostración del Sistema

## Flight Network Graph API - Resultados de Ejecución

Esta demostración muestra los resultados reales de ejecutar la API localmente.

---

## 1. Estadísticas del Grafo

```
GET /stats

{
    "total_airports": 15,
    "total_flights": 27,
    "density": 0.257,
    "is_connected": true
}
```

---

## 2. Lista de Aeropuertos

```
GET /airports

Total aeropuertos: 15

| Código | Ciudad | País |
|--------|--------|------|
| MAD | Madrid | Spain |
| BCN | Barcelona | Spain |
| LPA | Las Palmas | Spain |
| TFN | Tenerife | Spain |
| LHR | London | UK |
| CDG | Paris | France |
| FCO | Rome | Italy |
| FRA | Frankfurt | Germany |
| AMS | Amsterdam | Netherlands |
| JFK | New York | USA |
| MIA | Miami | USA |
| LAX | Los Angeles | USA |
| IST | Istanbul | Turkey |
| DXB | Dubai | UAE |
| SIN | Singapore | Singapore |
```

---

## 3. Ruta Más Corta (Dijkstra)

```
GET /shortest-path?origin=MAD&destination=JFK

{
    "origin": "MAD",
    "destination": "JFK",
    "path": ["MAD", "JFK"],
    "distance": 5768,
    "stops": 0
}
```

```
GET /shortest-path?origin=LPA&destination=SIN

{
    "origin": "LPA",
    "destination": "SIN",
    "path": ["LPA", "MAD", "LHR", "DXB", "SIN"],
    "distance": 14211,
    "stops": 3
}
```

---

## 4. Aeropuertos Hub (Mayor Conectividad)

```
GET /hubs?top=5

| Ranking | Aeropuerto | Conexiones |
|---------|------------|------------|
| 1 | MAD (Madrid) | 8 conexiones |
| 2 | LHR (London) | 6 conexiones |
| 3 | CDG (Paris) | 5 conexiones |
| 4 | JFK (New York) | 5 conexiones |
| 5 | BCN (Barcelona) | 4 conexiones |
```

---

## 5. Conexiones Directas

```
GET /connections?airport=MAD

{
    "airport": "MAD",
    "connections": ["BCN", "LPA", "TFN", "LHR", "CDG", "FCO", "JFK", "FRA"],
    "total": 8
}
```

---

## 6. Detección de Clusters (Comunidades)

```
GET /clusters

{
    "total_clusters": 3,
    "clusters": [
        {
            "id": 1,
            "name": "Cluster Europa Sur",
            "airports": ["CDG", "BCN", "LPA", "TFN", "MAD", "FCO"]
        },
        {
            "id": 2,
            "name": "Cluster Europa Norte + Asia",
            "airports": ["IST", "LHR", "AMS", "DXB", "FRA", "SIN"]
        },
        {
            "id": 3,
            "name": "Cluster América",
            "airports": ["LAX", "JFK", "MIA"]
        }
    ]
}
```

---

## 7. Ejecución de Tests

```bash
$ pytest tests/ -v

tests/test_api.py::test_get_airports PASSED
tests/test_api.py::test_get_stats PASSED
tests/test_api.py::test_shortest_path PASSED
tests/test_api.py::test_shortest_path_missing_params PASSED
tests/test_api.py::test_get_hubs PASSED
tests/test_api.py::test_get_connections PASSED
tests/test_api.py::test_get_clusters PASSED
tests/test_api.py::test_endpoint_not_found PASSED
tests/test_graph.py::test_add_airport PASSED
tests/test_graph.py::test_add_flight PASSED
tests/test_graph.py::test_shortest_path PASSED
tests/test_graph.py::test_shortest_path_no_route PASSED
tests/test_graph.py::test_get_connections PASSED
tests/test_graph.py::test_get_isolated_nodes PASSED
tests/test_graph.py::test_get_hubs PASSED
tests/test_graph.py::test_get_nodes_by_degree PASSED
tests/test_graph.py::test_all_paths PASSED
tests/test_graph.py::test_graph_stats PASSED

=================== 18 passed in 0.32s ===================
```

---

## 8. Cómo Ejecutar la Demostración

### Opción 1: Servidor Flask (Recomendado)

```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Ejecutar servidor
python app.py

# Abrir navegador en http://localhost:5000
```

### Opción 2: Script de Test

```bash
python test_local.py
```

### Opción 3: LocalStack (Docker)

```bash
# Iniciar LocalStack
docker-compose up -d

# Verificar servicios
docker ps
```

---

## 9. Captura del Frontend

El frontend web permite:
- Ver estadísticas en tiempo real
- Buscar rutas entre aeropuertos
- Visualizar hubs principales
- Consultar conexiones directas
- Ver clusters detectados

Accesible en: `http://localhost:5000` cuando el servidor está corriendo.

---

## 10. Captura del CI/CD

Ver `docs/capturaCICD.png` para la captura del pipeline de GitHub Actions funcionando correctamente.

---

**Todos los resultados mostrados son reales y reproducibles ejecutando el proyecto localmente.**
