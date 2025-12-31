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
from mpl_toolkits.mplot3d import Axes3D

# --- ARCHIVOS DE RASTROS ---
FILE_ALPHA = 'data/processed/spider_track.csv'
FILE_GHOST = 'data/processed/ghost_face_track.csv'
FILE_NEIGHBOR = 'data/processed/neighbor1_track.csv'

def load_track(filename):
    try:
        df = pd.read_csv(filename)
        # Filtrar solo puntos de camino y vértices
        return df[df['type'].isin(['PATH', 'VERTEX', 'VERTEX_FOUND'])]
    except FileNotFoundError:
        print(f"⚠️ Aviso: No se encontró {filename}")
        return None

def spherical_to_cartesian(lat, lon):
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    return x, y, z

def get_dodecahedron_wireframe():
    # Generar aristas teóricas para referencia de fondo
    phi = (1 + np.sqrt(5)) / 2
    verts = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            verts.append([0, i, j*phi])
            verts.append([j*phi, 0, i])
            verts.append([i, j*phi, 0])
    verts = np.array(verts)
    verts /= np.linalg.norm(verts, axis=1, keepdims=True)
    
    # Conectar vértices cercanos (aristas)
    edges = []
    for i in range(len(verts)):
        for j in range(i+1, len(verts)):
            dist = np.linalg.norm(verts[i] - verts[j])
            if np.isclose(dist, 0.7136, atol=0.05): # Distancia de arista en esfera unitaria
                edges.append((verts[i], verts[j]))
    return edges

def main():
    print("🌍 GENERANDO MOSAICO GLOBAL 3D...")
    
    # 1. Cargar Datos
    df_alpha = load_track(FILE_ALPHA)
    df_ghost = load_track(FILE_GHOST)
    df_neigh = load_track(FILE_NEIGHBOR)
    
    # 2. Configurar Plot 3D
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Dibujar Esfera Base (Fantasma visual)
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = 0.98 * np.cos(u)*np.sin(v)
    y = 0.98 * np.sin(u)*np.sin(v)
    z = 0.98 * np.cos(v)
    ax.plot_wireframe(x, y, z, color="gray", alpha=0.1)

    # 3. Dibujar Jaula Teórica (Gris punteado)
    # Nota: Esta es la jaula "perfecta", no rotada. Solo para escala.
    edges = get_dodecahedron_wireframe()
    for p1, p2 in edges:
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'k:', alpha=0.2, linewidth=0.5)

    # 4. Dibujar Nuestros Hallazgos
    
    # CARA ALFA (ROJO) - La Zona Cero
    if df_alpha is not None:
        xa, ya, za = spherical_to_cartesian(df_alpha['lat'], df_alpha['lon'])
        ax.plot(xa, ya, za, 'r-', linewidth=3, label='Cara Alfa (Origen)')
        # Vértices
        v_alpha = df_alpha[df_alpha['type'].str.contains('VERTEX')]
        vx, vy, vz = spherical_to_cartesian(v_alpha['lat'], v_alpha['lon'])
        ax.scatter(vx, vy, vz, c='red', s=50, depthshade=False)

    # CARA FANTASMA (MAGENTA) - El Antípoda
    if df_ghost is not None:
        xg, yg, zg = spherical_to_cartesian(df_ghost['lat'], df_ghost['lon'])
        ax.plot(xg, yg, zg, 'm-', linewidth=2, label='Cara Fantasma (Antípoda)')
        v_ghost = df_ghost[df_ghost['type'] == 'VERTEX']
        vx, vy, vz = spherical_to_cartesian(v_ghost['lat'], v_ghost['lon'])
        ax.scatter(vx, vy, vz, c='magenta', s=50, depthshade=False)

    # VECINO 1 (VERDE) - La Nueva Frontera
    if df_neigh is not None:
        xn, yn, zn = spherical_to_cartesian(df_neigh['lat'], df_neigh['lon'])
        ax.plot(xn, yn, zn, 'g-', linewidth=3, label='Vecino 1 (Deformado)')
        v_neigh = df_neigh[df_neigh['type'] == 'VERTEX']
        vx, vy, vz = spherical_to_cartesian(v_neigh['lat'], v_neigh['lon'])
        ax.scatter(vx, vy, vz, c='lime', s=60, marker='^', depthshade=False)

    # Decoración
    ax.set_title("EL MAPA DEL UNIVERSO\nTres Piezas del Puzle Dodecaédrico", fontsize=15)
    ax.legend()
    ax.set_axis_off() # Quitar ejes para que parezca un planeta flotando
    
    # Generar Vistas (Frente, Espalda, Lado)
    views = [(30, 45), (30, 225), (80, 0)]
    view_names = ['front', 'back', 'top']
    
    for (elev, azim), name in zip(views, view_names):
        ax.view_init(elev=elev, azim=azim)
        output = f'data/processed/global_mosaic_{name}.png'
        plt.savefig(output, dpi=150, bbox_inches='tight')
        print(f"📸 Foto tomada desde ángulo {name}: {output}")

if __name__ == "__main__":
    main()