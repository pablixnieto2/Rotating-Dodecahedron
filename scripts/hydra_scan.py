# ==============================================================================
#  The Geometry of the Echo: PMN-01 Model Source Code
#  ----------------------------------------------------------------------------
#  (c) 2025 Pablo Miguel Nieto Muñoz
#  License: MIT (See LICENSE file for details)
#  
#  Scientific Citation:
#  Nieto Muñoz, P. M. (2025). "The Geometry of the Echo: Observational 
#  Confirmation of the Chiral Dodecahedral Universe". 
#  Zenodo.
# ==============================================================================

import numpy as np
import healpy as hp
import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import os

# --- CONFIGURACIÓN DE MISIÓN ---
INPUT_FILE = 'data/raw/COM_CMB_IQU-sevem_2048_R4.00.fits'
START_LAT, START_LON = -41.81, 354.38 # Vértice 647
STEP_SIZE = 0.1     # Precisión milimétrica requerida
MAX_STEPS = 200     # Exploración inicial por rama
SCAN_STEP = 0.1     # Resolución de búsqueda angular
THRESHOLD = 0.035   # Sensibilidad

def get_corr(lat, lon, angle, map_I, map_P, nside):
    # Genera un vector de prueba a 0.5 grados de distancia
    dist = 0.5
    lat_r, lon_r = np.radians(lat), np.radians(lon)
    ang_r, dist_r = np.radians(angle), np.radians(dist)
    
    nl_r = np.arcsin(np.sin(lat_r)*np.cos(dist_r) + np.cos(lat_r)*np.sin(dist_r)*np.cos(ang_r))
    nlo_r = lon_r + np.arctan2(np.sin(ang_r)*np.sin(dist_r)*np.cos(lat_r), np.cos(dist_r)-np.sin(lat_r)*np.sin(nl_r))
    
    pix = hp.ang2pix(nside, np.pi/2 - nl_r, nlo_r)
    # Correlación simplificada rápida para el escaneo
    return map_I[pix] * map_P[pix] # Proxy de correlación para el "olfato"

def main():
    print(f"🐶 --- HYDRA TRACER V5: MODO INTELIGENTE ---")
    if not os.path.exists('data/processed'): os.makedirs('data/processed')

    print("🛰️ Cargando mapas...")
    maps = hp.read_map(INPUT_FILE, field=[0,1,2], verbose=False)
    map_I, map_P = maps[0], np.sqrt(maps[1]**2 + maps[2]**2)
    nside = hp.get_nside(map_I)

    # 1. ESCANEO DEL VÉRTICE (360º a 0.1º)
    print(f"🔎 Escaneando Vértice 647 a resolución de {SCAN_STEP}º...")
    scan = []
    for a in np.arange(0, 360, SCAN_STEP):
        v = get_corr(START_LAT, START_LON, a, map_I, map_P, nside)
        scan.append((a, v))
    
    # Encontrar las 3 direcciones dominantes (separadas por ~90-120º)
    scan = sorted(scan, key=lambda x: abs(x[1]), reverse=True)
    branches = []
    for ang, val in scan:
        if not any(abs(ang - b) < 60 for b in branches):
            branches.append(ang)
        if len(branches) == 3: break

    print(f"✅ ¡Ramas detectadas! Direcciones: {[round(b,1) for b in branches]}")

    # 2. RASTREO DE CADA RAMA
    fig = plt.figure(figsize=(12, 6))
    plt.title("Hydra Tracer: Escaneo de Ramas desde Vértice 647")

    for i, start_angle in enumerate(branches):
        print(f"🚀 Siguiendo Rama {i+1} (Rumbo {start_angle}º)...")
        path = []
        curr_lat, curr_lon = START_LAT, START_LON
        curr_ang = start_angle
        
        for s in range(MAX_STEPS):
            path.append({'lat': curr_lat, 'lon': curr_lon})
            # Paso de 0.1º
            lat_r, lon_r = np.radians(curr_lat), np.radians(curr_lon)
            d_r, a_r = np.radians(STEP_SIZE), np.radians(curr_ang)
            
            curr_lat = np.degrees(np.arcsin(np.sin(lat_r)*np.cos(d_r) + np.cos(lat_r)*np.sin(d_r)*np.cos(a_r)))
            curr_lon = np.degrees(lon_rad := lon_r + np.arctan2(np.sin(a_r)*np.sin(d_r)*np.cos(lat_r), np.cos(d_r)-np.sin(lat_r)*np.sin(np.radians(curr_lat))))
            
        df = pd.DataFrame(path)
        csv_name = f'data/processed/branch_{i+1}.csv'
        df.to_csv(csv_name, index=False)
        plt.plot(df['lon'], df['lat'], label=f'Rama {i+1} ({start_angle}º)')
        print(f"   💾 Guardado: {csv_name}")

    # 3. GENERAR IMAGEN DE DIAGNÓSTICO
    plt.scatter([START_LON], [START_LAT], color='red', marker='X', s=100, label='Vértice 647')
    plt.legend()
    plt.grid(True)
    plt.savefig('data/processed/hydra_scan_result.png')
    print(f"🖼️ Mapa de diagnóstico guardado: data/processed/hydra_scan_result.png")

if __name__ == "__main__":
    main()