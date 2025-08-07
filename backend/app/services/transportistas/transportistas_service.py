from math import radians, sin, cos, sqrt, atan2
import math

import requests
from app.schemas.operadores import Ubication


def calcular_velocidad(ubicacion1: Ubication, ubicacion2: Ubication):
    
    # Radio de la Tierra en metros
    R = 6371000

    # Convertir coordenadas de grados a radianes
    phi1 = radians(ubicacion1.latitude)
    phi2 = radians(ubicacion2.latitude)
    delta_phi = radians(ubicacion2.latitude - ubicacion1.latitude)
    delta_lambda = radians(ubicacion2.longitude - ubicacion1.longitude)

    # Fórmula de Haversine para calcular la distancia
    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distancia_metros = R * c

    # Calcular la diferencia de tiempo en segundos
    delta_tiempo_segundos = (ubicacion2.timestamp.replace(tzinfo=None) - ubicacion1.timestamp.replace(tzinfo=None)).total_seconds()

    if delta_tiempo_segundos == 0:
        return 0.0  # Evitar división por cero

    # Calcular velocidad en m/s y convertir a km/h
    velocidad_m_s = distancia_metros / delta_tiempo_segundos
    velocidad_kmh = velocidad_m_s * 3.6

    # Truncar a dos decimales
    return math.trunc(velocidad_kmh * 100) / 100

def chunk_list(lst, size):
    """Divide una lista en bloques del tamaño especificado."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def match_osrm_chunks(gps_coords, timestamps, radiuses, chunk_size=30):
    all_coordinates = []
    all_tracepoints = []

    for gps_chunk, time_chunk, radius_chunk in zip(
        chunk_list(gps_coords, chunk_size),
        chunk_list(timestamps, chunk_size),
        chunk_list(radiuses, chunk_size)
    ):
        str_gps = ';'.join(gps_chunk)
        str_times = ';'.join(time_chunk)
        str_rads = ';'.join(radius_chunk)

        url = f"http://18.116.39.80:5000/match/v1/driving/{str_gps}"
        params = {
            "geometries": "geojson",
            "overview": "full",
            "tidy": "true",
            "gaps": "ignore",
            "timestamps": str_times,
            "radiuses": str_rads
        }

        try:
            resp = requests.get(url, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()

            # Extraer geometry.coordinates del primer matching
            if 'matchings' in data and data['matchings']:
                matching = data['matchings'][0]
                if 'geometry' in matching and 'coordinates' in matching['geometry']:
                    all_coordinates.extend(matching['geometry']['coordinates'])
                else:
                    print("Advertencia: 'geometry' o 'coordinates' no encontrados en matching.")
            else:
                print("Advertencia: 'matchings' vacío o no encontrado.")

            # Extraer tracepoints válidos (no None)
            if 'tracepoints' in data and data['tracepoints']:
                valid_tracepoints = [tp for tp in data['tracepoints'] if tp is not None]
                all_tracepoints.extend(valid_tracepoints)
            else:
                print("Advertencia: 'tracepoints' vacío o no encontrado.")

        except Exception as e:
            print(f"Error en chunk OSRM: {e}")
            raise

    return all_coordinates, all_tracepoints


def nearest_osrm(gps_coords):
    all_coordinates = []
    all_tracepoints = []

    str_gps = ';'.join(gps_coords)


    url = f"http://18.116.39.80:5000/nearest/v1/driving/{str_gps}"

    try:
        resp = requests.get(url,{}, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        
        if 'waypoints' in data and data['waypoints']:
            locationarray = data['waypoints'][0]['location']
            locationitem = data['waypoints'][0]
            all_coordinates.append(locationarray)
            all_tracepoints.append(locationitem)
            

    except Exception as e:
        print(f"Error en nearest OSRM: {e}")

    return all_coordinates, all_tracepoints

