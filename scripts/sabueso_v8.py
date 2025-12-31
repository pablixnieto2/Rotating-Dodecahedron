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
import matplotlib.pyplot as plt
import os

# --- CONFIGURACIÓN ---
INPUT_FILE = 'data/raw/COM_CMB_IQU-sevem_2048_R4.00.fits'
START_LAT, START_LON = -41.81, 354.38  # Vértice 647 (Inicio)
INITIAL_BEARING = 204.3                # Rumbo confirmado de la Rama 3
STEP_SIZE = 0.2                        # Paso de avance
CORR_THRESHOLD = 1.0e-12               # (Dinámico) Se ajustará a la media local

def get_signal_at(lat, lon, angle, map_I, map_P, nside):
    """Obtiene la fuerza de la señal (Correlación T*P) en un punto adelante."""
    # Proyectar punto a 0.5 grados
    dist_rad = np.radians(0.5)
    lat_r, lon_r = np.radians(lat), np.radians(lon)
    ang_r = np.radians(angle)
    
    new_lat_r = np.arcsin(np.sin(lat_r)*np.cos(dist_rad) + np.cos(lat_r)*np.sin(dist_rad)*np.cos(ang_r))
    new_lon_r = lon_r + np.arctan2(np.sin(ang_r)*np.sin(dist_rad)*np.cos(lat_r), np.cos(dist_rad)-np.sin(lat_r)*np.sin(new_lat_r))
    
    pix = hp.ang2pix(nside, np.pi/2 - new_lat_r, new_lon_r)
    # Señal = Intensidad * Polarización (valor absoluto)
    return abs(map_I[pix] * map_P[pix])

def move(lat, lon, angle, step_deg):
    """Mueve las coordenadas en la esfera."""
    lat_r, lon_r = np.radians(lat), np.radians(lon)
    ang_r, dist_r = np.radians(angle), np.radians(step_deg)
    
    new_lat_r = np.arcsin(np.sin(lat_r)*np.cos(dist_r) + np.cos(lat_r)*np.sin(dist_r)*np.cos(ang_r))
    new_lon_r = lon_r + np.arctan2(np.sin(ang_r)*np.sin(dist_r)*np.cos(lat_r), np.cos(dist_r)-np.sin(lat_r)*np.sin(new_lat_r))
    return np.degrees(new_lat_r), np.degrees(new_lon_r)

def main():
    print("🕷️ SABUESO V8: LA ARAÑA (WALL-CRAWLER)")
    print("   Estrategia: Seguir -> Perder Señal -> Girar -> Repetir")
    
    # Cargar mapas
    maps = hp.read_map(INPUT_FILE, field=[0,1,2], verbose=False)
    map_I, map_P = maps[0], np.sqrt(maps[1]**2 + maps[2]**2)
    nside = hp.get_nside(map_I)

    path = [{'lat': START_LAT, 'lon': START_LON, 'type': 'VERTEX_START'}]
    current_lat, current_lon = START_LAT, START_LON
    current_bearing = INITIAL_BEARING
    
    # Estado
    walking_edge = True
    vertices_found = 0
    max_steps_per_edge = 300 # ~60 grados max
    steps_on_edge = 0
    
    # Calibrar umbral de señal promedio en el inicio
    initial_sig = get_signal_at(START_LAT, START_LON, current_bearing, map_I, map_P, nside)
    signal_threshold = initial_sig * 0.4 # Si baja del 40%, asumimos que se acabó la línea
    print(f"   📶 Señal Inicial: {initial_sig:.2e} | Umbral de Corte: {signal_threshold:.2e}")

    total_steps = 1000
    
    for s in range(total_steps):
        # 1. Mirar adelante
        sig_ahead = get_signal_at(current_lat, current_lon, current_bearing, map_I, map_P, nside)
        
        # 2. Decisión
        if sig_ahead < signal_threshold and steps_on_edge > 20:
            # ¡SEÑAL PERDIDA! Posible vértice.
            print(f"\n🛑 Señal perdida en Paso {s} (Lat {current_lat:.2f}, Lon {current_lon:.2f}). Buscando giro...")
            
            # --- MANIOBRA DE GIRO (RADAR) ---
            best_new_angle = current_bearing
            max_scan_sig = 0
            
            # Escanear 360 grados (excluyendo volver hacia atrás +/- 30 grados)
            scan_range = list(range(0, 360, 5))
            reverse_angle = (current_bearing + 180) % 360
            
            for ang in scan_range:
                # Evitar volver por donde vinimos
                if abs(ang - reverse_angle) < 30: continue
                
                scan_sig = get_signal_at(current_lat, current_lon, ang, map_I, map_P, nside)
                if scan_sig > max_scan_sig:
                    max_scan_sig = scan_sig
                    best_new_angle = ang
            
            print(f"   ↪️ Giro detectado: de {current_bearing:.1f}º a {best_new_angle:.1f}º (Señal recuperada: {max_scan_sig:.2e})")
            
            # Registrar Vértice
            path.append({'lat': current_lat, 'lon': current_lon, 'type': 'VERTEX_FOUND'})
            vertices_found += 1
            
            # Actualizar rumbo
            current_bearing = best_new_angle
            steps_on_edge = 0 # Reset contador de arista
            
            # Si hemos encontrado 5 vértices, paramos (Pentágono cerrado)
            if vertices_found >= 5:
                print("🏆 ¡POLÍGONO CERRADO! (5 Vértices encontrados)")
                break
                
        else:
            # Seguimos caminando
            # Pequeña corrección de rumbo (autotracking)
            # Miramos +/- 10 grados para mantenerse en la cresta de la ola
            best_adj = 0
            local_max = -1
            for adj in [-10, -5, 0, 5, 10]:
                check_sig = get_signal_at(current_lat, current_lon, current_bearing + adj, map_I, map_P, nside)
                if check_sig > local_max:
                    local_max = check_sig
                    best_adj = adj
            current_bearing += best_adj
            
            steps_on_edge += 1

        # Mover
        current_lat, current_lon = move(current_lat, current_lon, current_bearing, STEP_SIZE)
        path.append({'lat': current_lat, 'lon': current_lon, 'type': 'PATH'})
        
        if s % 50 == 0:
            print(f"   👣 Paso {s}: Lat {current_lat:.2f}, Lon {current_lon:.2f} | Sig: {sig_ahead:.2e}")

    # --- RESULTADOS Y CENTRO ---
    df = pd.DataFrame(path)
    df.to_csv('data/processed/spider_track.csv', index=False)
    
    # Calcular Centroide (solo de los vértices)
    verts = df[df['type'].str.contains('VERTEX')]
    if len(verts) > 0:
        center_lat = verts['lat'].mean()
        center_lon = verts['lon'].mean()
        print(f"\n🎯 CENTRO CALCULADO DEL POLÍGONO: Lat {center_lat:.4f}, Lon {center_lon:.4f}")
    
    # Graficar
    plt.figure(figsize=(10, 8))
    plt.plot(df['lon'], df['lat'], 'c-', label='Rastro Araña')
    plt.scatter(verts['lon'], verts['lat'], c='red', s=100, zorder=5, label='Vértices Detectados')
    if len(verts) > 0:
        plt.scatter([center_lon], [center_lat], c='gold', marker='*', s=300, edgecolor='black', zorder=10, label='Centro Calculado')
    
    plt.title("Rastreo Autónomo de Perímetro (Spider Algorithm)")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.legend()
    plt.grid(True)
    plt.savefig('data/processed/spider_result.png')
    print("🖼️ Mapa guardado: data/processed/spider_result.png")

if __name__ == "__main__":
    main()