"""
Funciones auxiliares para el proyecto.
"""
import json
import os
from typing import List, Dict


def load_json_file(file_path: str) -> List[Dict]:
    """Carga datos desde un archivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_data_path(filename: str) -> str:
    """Obtiene la ruta absoluta a un archivo de datos."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, 'data', filename)


def format_response(status_code: int, body: dict) -> dict:
    """Formatea la respuesta para API Gateway."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }


def parse_request_body(event: dict) -> dict:
    """Parsea el body de una petición de API Gateway."""
    body = event.get('body', '{}')
    if isinstance(body, str):
        return json.loads(body)
    return body