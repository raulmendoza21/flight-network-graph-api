"""Script para probar la API localmente."""
from src.lambdas.graph_operations import lambda_handler
import json

# Test 1: Obtener aeropuertos
print('=== Test: GET /airports ===')
event = {'path': '/airports', 'httpMethod': 'GET'}
response = lambda_handler(event, None)
body = json.loads(response['body'])
print(f"Status: {response['statusCode']}")
print(f"Total aeropuertos: {len(body['airports'])}")

# Test 2: Ruta más corta MAD -> JFK
print('\n=== Test: GET /shortest-path MAD -> JFK ===')
event = {'path': '/shortest-path', 'httpMethod': 'GET', 'queryStringParameters': {'origin': 'MAD', 'destination': 'JFK'}}
response = lambda_handler(event, None)
body = json.loads(response['body'])
print(f"Ruta: {' -> '.join(body['path'])}")
print(f"Distancia: {body['distance']} km")
print(f"Escalas: {body['stops']}")

# Test 3: Hubs
print('\n=== Test: GET /hubs (top 5) ===')
event = {'path': '/hubs', 'httpMethod': 'GET', 'queryStringParameters': {'top': '5'}}
response = lambda_handler(event, None)
body = json.loads(response['body'])
for hub in body['hubs']:
    print(f"{hub['airport']}: {hub['connections']} conexiones")

# Test 4: Estadísticas
print('\n=== Test: GET /stats ===')
event = {'path': '/stats', 'httpMethod': 'GET'}
response = lambda_handler(event, None)
body = json.loads(response['body'])
print(f"Aeropuertos: {body['total_airports']}")
print(f"Vuelos: {body['total_flights']}")
print(f"Densidad: {body['density']:.3f}")

# Test 5: Clusters
print('\n=== Test: GET /clusters ===')
event = {'path': '/clusters', 'httpMethod': 'GET'}
response = lambda_handler(event, None)
body = json.loads(response['body'])
print(f"Total clusters: {body['total_clusters']}")
for i, cluster in enumerate(body['clusters']):
    print(f"  Cluster {i+1}: {cluster}")

print('\n✅ Todos los tests pasaron!')
