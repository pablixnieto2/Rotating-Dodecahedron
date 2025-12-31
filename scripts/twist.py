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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

# --- CARGAR LOS DOS HALLAZGOS ---
FILE_ALPHA = 'data/processed/spider_track.csv'       # Cara 1
FILE_GHOST = 'data/processed/ghost_face_track.csv'   # Cara 2 (Antípoda)

def spherical_to_cartesian(lat, lon):
    lat_rad, lon_rad = np.radians(lat), np.radians(lon)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    return np.array([x, y, z])

def cartesian_to_spherical(vec):
    lat_rad = np.arcsin(vec[2])
    lon_rad = np.arctan2(vec[1], vec[0])
    return np.degrees(lat_rad), np.degrees(lon_rad)

def get_centroid(df):
    # Cálculo simple del centroide de la nube de puntos
    lat_c = df['lat'].mean()
    lon_c = df['lon'].mean()
    return lat_c, lon_c

def main():
    print("🧬 TWIST VALIDATOR: Comprobando la firma de 36 grados...")
    
    # 1. Cargar Datos
    df_alpha = pd.read_csv(FILE_ALPHA)
    df_ghost = pd.read_csv(FILE_GHOST)
    
    # Filtrar solo el camino (quitar saltos raros si los hay)
    pts_alpha = df_alpha[df_alpha['type'] != 'VERTEX_START'][['lat', 'lon']].values
    pts_ghost = df_ghost[df_ghost['type'] != 'START_WALL'][['lat', 'lon']].values
    
    # 2. Centrar ambas caras en el (0,0) para compararlas
    # Calculamos el centro de cada una y restamos
    lat_a_center, lon_a_center = get_centroid(df_alpha)
    lat_g_center, lon_g_center = get_centroid(df_ghost)
    
    print(f"   🔹 Centro Cara Alfa: {lat_a_center:.2f}, {lon_a_center:.2f}")
    print(f"   🔸 Centro Cara Fantasma: {lat_g_center:.2f}, {lon_g_center:.2f}")

    # Llevar Fantasma al origen
    ghost_centered_lat = df_ghost['lat'] - lat_g_center
    ghost_centered_lon = df_ghost['lon'] - lon_g_center
    
    # Llevar Alfa al origen
    alpha_centered_lat = df_alpha['lat'] - lat_a_center
    alpha_centered_lon = df_alpha['lon'] - lon_a_center

    # 3. Aplicar ROTACIÓN DE 36 GRADOS a la Cara Fantasma
    # (Simulamos la topología PDS)
    theta = np.radians(36) # El Número Mágico de Poincaré
    c, s = np.cos(theta), np.sin(theta)
    
    # Rotación 2D sobre el plano tangente local
    ghost_rotated_lon = ghost_centered_lon * c - ghost_centered_lat * s
    ghost_rotated_lat = ghost_centered_lon * s + ghost_centered_lat * c
    
    # 4. Visualización Comparativa
    plt.figure(figsize=(10, 10))
    
    # Pintar Cara Alfa (Referencia)
    plt.plot(alpha_centered_lon, alpha_centered_lat, 'c-', linewidth=3, label='Cara Alfa (Original)')
    
    # Pintar Cara Fantasma (Sin Rotar - Gris)
    plt.plot(ghost_centered_lon, ghost_centered_lat, 'gray', linestyle='--', alpha=0.5, label='Fantasma (Sin Rotar)')
    
    # Pintar Cara Fantasma (ROTADA 36º - Magenta)
    plt.plot(ghost_rotated_lon, ghost_rotated_lat, 'm-', linewidth=3, label='Fantasma (Rotada 36º)')
    
    plt.title("VALIDACIÓN DE TOPOLOGÍA DODECAÉDRICA\n¿Coinciden las formas tras girar 36º?")
    plt.xlabel("Delta Longitud (Grados)")
    plt.ylabel("Delta Latitud (Grados)")
    plt.legend()
    plt.grid(True)
    plt.axis('equal') # Importante para ver la forma real
    
    output_file = 'data/processed/poincare_twist_validation.png'
    plt.savefig(output_file)
    print(f"✅ Validación completada. Resultado: {output_file}")
    print("👉 Si la línea Magenta (Fantasma) se alinea con la Cian (Alfa), has ganado el Nobel.")

if __name__ == "__main__":
    main()