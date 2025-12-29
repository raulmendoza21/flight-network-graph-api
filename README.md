# ✈️ Flight Network Graph API

API REST para gestionar y analizar una red de vuelos usando grafos.

## 📋 Descripción

Sistema que modela aeropuertos como nodos y vuelos como aristas, permitiendo operaciones de análisis de grafos como búsqueda de rutas, detección de hubs y clusters.

## 🏗️ Arquitectura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Cliente   │────▶│ API Gateway │────▶│   Lambda    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────┐
                    ▼                          ▼              ▼
             ┌─────────────┐           ┌─────────────┐  ┌──────────┐
             │  DynamoDB   │           │     S3      │  │ NetworkX │
             └─────────────┘           └─────────────┘  └──────────┘
```

## 🚀 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/airports` | Lista todos los aeropuertos |
| GET | `/stats` | Estadísticas del grafo |
| GET | `/shortest-path?origin=X&destination=Y` | Ruta más corta |
| GET | `/all-paths?origin=X&destination=Y` | Todos los caminos |
| GET | `/hubs?top=N` | Aeropuertos más conectados |
| GET | `/isolated` | Aeropuertos sin conexiones |
| GET | `/connections?airport=X` | Conexiones de un aeropuerto |
| GET | `/by-degree?degree=N` | Filtrar por nº conexiones |
| GET | `/clusters` | Detectar comunidades |
| GET | `/longest-path?origin=X&destination=Y` | Camino más largo |

## 🛠️ Instalación Local

```bash
# Clonar repositorio
git clone <repo-url>
cd TF

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest tests/ -v
```

## 🐳 LocalStack

```bash
# Levantar LocalStack
docker-compose up -d

# Verificar servicios
curl http://localhost:4566/_localstack/health
```

## 📊 Ejemplo de Uso

```bash
# Obtener ruta más corta Madrid → New York
curl "http://localhost:4566/restapis/.../shortest-path?origin=MAD&destination=JFK"

# Respuesta
{
  "origin": "MAD",
  "destination": "JFK", 
  "path": ["MAD", "JFK"],
  "distance": 5768,
  "stops": 0
}
```

## 🧪 Tests

```bash
pytest tests/ -v
```

## 📁 Estructura

```
TF/
├── src/
│   ├── lambdas/         # Funciones Lambda
│   ├── models/          # Modelo del grafo
│   └── utils/           # Helpers
├── data/                # Datos JSON
├── tests/               # Tests
├── infrastructure/      # AWS/LocalStack config
└── .github/workflows/   # CI/CD
```

## 👤 Autor

Tecnologías de Servicios para Ciencia de Datos - ULPGC