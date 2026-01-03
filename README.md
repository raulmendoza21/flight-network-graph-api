# ✈️ Flight Network Graph API

API REST y frontend para analizar una red de vuelos usando grafos (NetworkX), con despliegue serverless (SAM), entorno local con Flask y LocalStack, pruebas automáticas y CI/CD en GitHub Actions.

## 🔗 Repositorio
https://github.com/raulmendoza21/flight-network-graph-api

## 🧭 Características
- Modelo de grafo: aeropuertos como nodos, vuelos como aristas con peso distancia.
- Endpoints para rutas, hubs, clusters, conexiones y estadísticas.
- Frontend web simple servido por Flask para probar la API.
- Infraestructura como código con AWS SAM + LocalStack para desarrollo local.
- CI/CD con GitHub Actions (18 tests pasando).

## 🗺️ Arquitectura

```
Cliente (Frontend)
   │
   ▼
API Gateway (LocalStack/AWS) ──► Lambda (graph_operations.py)
                                   │
                                   ├─ Lee datos JSON (S3 o local)
                                   └─ FlightGraph (NetworkX)
```

## 🚀 Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /airports | Lista todos los aeropuertos |
| GET | /stats | Estadísticas del grafo |
| GET | /shortest-path?origin=X&destination=Y | Ruta más corta |
| GET | /all-paths?origin=X&destination=Y | Todos los caminos |
| GET | /hubs?top=N | Aeropuertos más conectados |
| GET | /isolated | Aeropuertos sin conexiones |
| GET | /connections?airport=X | Conexiones directas de un aeropuerto |
| GET | /by-degree?degree=N | Aeropuertos con N conexiones |
| GET | /clusters | Detección de comunidades |
| GET | /longest-path?origin=X&destination=Y | Camino simple más largo |

## 🛠️ Puesta en marcha (local)

```bash
# 1) Clonar
git clone https://github.com/raulmendoza21/flight-network-graph-api.git
cd flight-network-graph-api

# 2) Entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 3) Dependencias
pip install -r requirements.txt

# 4) Servidor local Flask (API + frontend)
python app.py
# Abre http://localhost:5000
```

### Opción: LocalStack (Docker)
```bash
docker-compose up -d
# Verifica: docker ps
```

## 🧪 Tests y CI/CD

```bash
pytest tests/ -v
```

- 18 tests pasan (modelo y API). Pipeline GitHub Actions: lint + tests.
- Informe: [docs/INFORME_PRUEBAS_CICD.md](docs/INFORME_PRUEBAS_CICD.md)

## 🗂️ Datos
- [data/airports.json](data/airports.json)
- [data/flights.json](data/flights.json)

## 📄 Documentación
- Memoria LaTeX: [docs/memoria.tex](docs/memoria.tex)
- Arquitectura: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Demo con salidas reales: [docs/DEMO.md](docs/DEMO.md)
- Guía de proyecto: [docs/GUIA_PROYECTO.md](docs/GUIA_PROYECTO.md)

## 📁 Estructura

```
flight-network-graph-api/
├── app.py                  # Servidor Flask local
├── frontend/               # Interfaz web
├── src/
│   ├── lambdas/graph_operations.py
│   ├── models/graph.py
│   └── utils/helpers.py
├── data/                   # Datos de aeropuertos y vuelos
├── tests/                  # Tests API y modelo
├── infrastructure/
│   ├── aws/template.yaml   # SAM template
│   └── localstack/setup.sh
├── docs/                   # Memoria, demo, informes, capturas
└── .github/workflows/ci-cd.yml
```

## 👤 Autor
Raúl Mendoza — Tecnologías de Servicios para Ciencia de Datos (ULPGC)