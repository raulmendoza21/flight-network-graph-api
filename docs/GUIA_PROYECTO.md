# 🎓 Guía Completa del Proyecto Flight Network Graph API

**Tecnologías de Servicios para Ciencia de Datos**  
**Universidad de Las Palmas de Gran Canaria**  
**Curso 2024-2025**

---

## 1. ¿Qué es este proyecto?

Es una **API** (un programa que responde a peticiones web) que trabaja con un **grafo de vuelos**.

**Imagina un mapa** donde:
- Cada **aeropuerto** es un punto (nodo)
- Cada **vuelo** es una línea que conecta dos puntos (arista)

```
    Madrid -------- Barcelona
       |     \
       |      \---- París
       |
    Londres ------- Nueva York
```

La API te permite preguntar cosas como:
- ¿Cuál es la ruta más corta de Madrid a Nueva York?
- ¿Qué aeropuerto tiene más conexiones?
- ¿Hay aeropuertos sin vuelos?

---

## 2. Estructura del Proyecto

```
TF/
├── data/                    → LOS DATOS
│   ├── airports.json        → Lista de aeropuertos
│   └── flights.json         → Lista de vuelos
│
├── src/                     → EL CÓDIGO
│   ├── models/
│   │   └── graph.py         → La clase del grafo (la lógica principal)
│   ├── lambdas/
│   │   └── graph_operations.py  → El servidor que recibe peticiones
│   └── utils/
│       └── helpers.py       → Funciones auxiliares
│
├── tests/                   → LOS TESTS
│   ├── test_graph.py        → Pruebas del grafo
│   └── test_api.py          → Pruebas de la API
│
├── infrastructure/          → CONFIGURACIÓN CLOUD
│   ├── localstack/          → Para probar en tu PC
│   └── aws/                 → Para desplegar en Amazon
│
├── .github/workflows/       → CI/CD (automatización)
│   └── ci-cd.yml            → Ejecuta tests automáticamente
│
├── docker-compose.yml       → Levanta LocalStack
├── requirements.txt         → Librerías necesarias
├── test_local.py            → Script para probar rápido
└── README.md                → Documentación
```

---

## 3. ¿Cómo funciona el código?

### 3.1 Los datos (airports.json y flights.json)

**airports.json** - Lista de aeropuertos:
```json
[
  {"code": "MAD", "name": "Madrid-Barajas", "city": "Madrid", "country": "Spain"},
  {"code": "JFK", "name": "John F. Kennedy", "city": "New York", "country": "USA"}
]
```

**flights.json** - Lista de vuelos (conexiones):
```json
[
  {"origin": "MAD", "destination": "JFK", "distance": 5768}
]
```

### 3.2 El modelo del grafo (graph.py)

Esta clase carga los datos y hace los cálculos:

```python
class FlightGraph:
    def __init__(self):
        self.graph = nx.Graph()  # Usamos NetworkX (librería de grafos)
    
    def shortest_path(self, origen, destino):
        # Usa el algoritmo de Dijkstra para encontrar la ruta más corta
        return nx.shortest_path(self.graph, origen, destino)
    
    def get_hubs(self):
        # Devuelve los aeropuertos con más conexiones
        return sorted(self.graph.degree(), key=lambda x: x[1], reverse=True)
```

### 3.3 La API (graph_operations.py)

Recibe peticiones HTTP y llama al grafo:

```python
def lambda_handler(event, context):
    # Mira qué URL pidió el usuario
    path = event.get('path')  # Ejemplo: "/shortest-path"
    
    if path == '/shortest-path':
        origen = query_params.get('origin')  # MAD
        destino = query_params.get('destination')  # JFK
        
        # Llama al grafo para calcular
        ruta = graph.shortest_path(origen, destino)
        
        # Devuelve el resultado como JSON
        return {'statusCode': 200, 'body': json.dumps({'path': ruta})}
```

---

## 4. ¿Cómo ejecutarlo?

### Opción A: Probar rápido (sin Docker)

```bash
# 1. Abre terminal en la carpeta del proyecto
cd "c:\Users\raule\Documents\Universidad\4ºGCID\1 cuatri\TSCD\TF"

# 2. Activa el entorno virtual
.venv\Scripts\activate

# 3. Ejecuta el script de prueba
python test_local.py
```

**Resultado esperado:**
```
=== Test: GET /airports ===
Total aeropuertos: 15

=== Test: GET /shortest-path MAD -> JFK ===
Ruta: MAD -> JFK
Distancia: 5768 km

=== Test: GET /hubs (top 5) ===
MAD: 8 conexiones
LHR: 6 conexiones
...

✅ Todos los tests pasaron!
```

### Opción B: Ejecutar tests automáticos

```bash
# Ejecuta todos los tests
python -m pytest tests/ -v
```

**Resultado esperado:**
```
tests/test_graph.py::test_shortest_path PASSED
tests/test_api.py::test_get_airports PASSED
... 18 passed ✅
```

### Opción C: Con Docker + LocalStack (simula AWS)

```bash
# 1. Inicia Docker Desktop

# 2. Levanta LocalStack
docker-compose up -d

# 3. Verifica que está corriendo
docker ps

# 4. Para pararlo
docker-compose down
```

---

## 5. Los 10 Endpoints de la API

| Endpoint | ¿Qué hace? | Ejemplo |
|----------|------------|---------|
| `/airports` | Lista todos los aeropuertos | GET /airports |
| `/stats` | Estadísticas del grafo | GET /stats |
| `/shortest-path` | Ruta más corta entre A y B | GET /shortest-path?origin=MAD&destination=JFK |
| `/all-paths` | Todas las rutas posibles | GET /all-paths?origin=MAD&destination=JFK |
| `/hubs` | Aeropuertos más conectados | GET /hubs?top=5 |
| `/isolated` | Aeropuertos sin conexiones | GET /isolated |
| `/connections` | Vuelos directos de un aeropuerto | GET /connections?airport=MAD |
| `/by-degree` | Aeropuertos con X conexiones | GET /by-degree?degree=3 |
| `/clusters` | Detecta regiones/grupos | GET /clusters |
| `/longest-path` | Camino más largo | GET /longest-path?origin=MAD&destination=LAX |

---

## 6. ¿Qué es Lambda y API Gateway?

### AWS Lambda
- Es una **función** que se ejecuta en la nube
- Solo pagas cuando se usa (no tienes servidor encendido 24/7)
- Tu código `graph_operations.py` es la Lambda

### API Gateway
- Es la **puerta de entrada** a tu Lambda
- Recibe las peticiones HTTP (GET /airports)
- Las envía a Lambda
- Devuelve la respuesta al usuario

**Flujo completo:**
```
Usuario → API Gateway → Lambda → Ejecuta código → Devuelve JSON
```

### LocalStack
- Es una **simulación de AWS** en tu PC
- Puedes probar sin pagar ni crear cuenta de Amazon
- Se levanta con Docker

---

## 7. ¿Qué es CI/CD?

Es **automatización** del proceso de desarrollo:

1. **Tú haces push** a GitHub
2. **GitHub Actions** detecta el cambio
3. **Automáticamente**:
   - Instala dependencias
   - Ejecuta los 18 tests
   - Si pasan, despliega a AWS

**Flujo visual:**
```
Push → GitHub → Actions → Tests → Deploy
```

El archivo de configuración está en `.github/workflows/ci-cd.yml`

---

## 8. Tecnologías Utilizadas

| Tecnología | Versión | Para qué se usa |
|------------|---------|-----------------|
| Python | 3.11 | Lenguaje de programación |
| NetworkX | 3.2.1 | Algoritmos de grafos |
| Boto3 | 1.34.0 | Conexión con AWS |
| Pytest | 7.4.3 | Tests automáticos |
| Docker | - | Contenedores |
| LocalStack | latest | Simular AWS localmente |
| GitHub Actions | - | CI/CD |
| AWS Lambda | - | Ejecutar código en la nube |
| AWS API Gateway | - | Exponer endpoints HTTP |
| AWS S3 | - | Almacenar datos |

---

## 9. Resumen de Archivos

| Archivo | Para qué sirve |
|---------|----------------|
| `graph.py` | La lógica del grafo (algoritmos) |
| `graph_operations.py` | Recibe peticiones HTTP |
| `airports.json` | Datos de aeropuertos (15) |
| `flights.json` | Datos de vuelos (27) |
| `test_local.py` | Probar rápido todo |
| `test_graph.py` | Tests del modelo |
| `test_api.py` | Tests de la API |
| `docker-compose.yml` | Configuración LocalStack |
| `template.yaml` | Configuración AWS SAM |
| `ci-cd.yml` | Pipeline CI/CD |
| `ARCHITECTURE.md` | Documentación técnica |

---

## 10. Comandos Más Útiles

```bash
# Activar entorno virtual
.venv\Scripts\activate

# Probar rápido
python test_local.py

# Ejecutar tests
python -m pytest tests/ -v

# Levantar LocalStack
docker-compose up -d

# Parar LocalStack
docker-compose down

# Ver estado git
git status

# Subir cambios
git add .
git commit -m "mensaje"
git push
```

---

## 11. Resultados de las Pruebas

Al ejecutar `python test_local.py`:

```
=== Test: GET /airports ===
Status: 200
Total aeropuertos: 15

=== Test: GET /shortest-path MAD -> JFK ===
Ruta: MAD -> JFK
Distancia: 5768 km
Escalas: 0

=== Test: GET /hubs (top 5) ===
MAD: 8 conexiones
LHR: 6 conexiones
CDG: 5 conexiones
JFK: 5 conexiones
BCN: 4 conexiones

=== Test: GET /stats ===
Aeropuertos: 15
Vuelos: 27
Densidad: 0.257

=== Test: GET /clusters ===
Total clusters: 3
  Cluster 1: ['BCN', 'TFN', 'MAD', 'CDG', 'FCO', 'LPA']
  Cluster 2: ['FRA', 'SIN', 'AMS', 'IST', 'DXB', 'LHR']
  Cluster 3: ['LAX', 'JFK', 'MIA']

✅ Todos los tests pasaron!
```

---

## 12. Repositorio

**GitHub:** https://github.com/raulmendoza21/flight-network-graph-api

---

*Documento generado para el proyecto de Tecnologías de Servicios para Ciencia de Datos - ULPGC*
