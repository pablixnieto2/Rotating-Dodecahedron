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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform import Rotation as R
import pandas as pd
import os

# --- CONFIGURACIÓN ---
ALPHA_LAT = -43.3116
ALPHA_LON = 348.6708
CSV_FILE = 'data/processed/dodecahedron_faces_coordinates.csv'
OUTPUT_DIR = 'FINAL_PMN/src/20_EL_UNIVERSO_HOLOGRAFICO/images'

def get_face_status():
    if not os.path.exists(CSV_FILE):
        print(f"⚠️ No se encontró {CSV_FILE}. Generando dummy data.")
        return [1] * 12
    
    df = pd.read_csv(CSV_FILE)
    status_list = []
    for _, row in df.iterrows():
        s = row['status']
        if "RUIDO" in s:
            status_list.append(0)
        else:
            status_list.append(1)
    return status_list

def get_dodecahedron_geometry():
    phi = (1 + np.sqrt(5)) / 2
    vertices = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            for k in [-1, 1]:
                vertices.append([i, j, k])
    inv_phi = 1 / phi
    for i in [-1, 1]:
        for j in [-1, 1]:
            vertices.append([0, i*phi, j*inv_phi])
            vertices.append([j*inv_phi, 0, i*phi])
            vertices.append([i*phi, j*inv_phi, 0])
    vertices = np.array(vertices)
    vertices = vertices / np.linalg.norm(vertices[0])
    return vertices

def get_faces(verts):
    faces = []
    centers = []
    phi = (1 + np.sqrt(5)) / 2
    ico_verts = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            ico_verts.append([0, i, j*phi])
            ico_verts.append([j*phi, 0, i])
            ico_verts.append([i, j*phi, 0])
    ico_verts = np.array(ico_verts)
    ico_verts /= np.linalg.norm(ico_verts, axis=1, keepdims=True)
    
    for center in ico_verts:
        dists = np.linalg.norm(verts - center, axis=1)
        idx = np.argsort(dists)[:5]
        face_verts = verts[idx]
        v_centered = face_verts - center
        z_axis = center
        x_axis = np.cross(np.array([0,0,1]), z_axis)
        if np.linalg.norm(x_axis) < 0.1: x_axis = np.array([1,0,0])
        x_axis /= np.linalg.norm(x_axis)
        y_axis = np.cross(z_axis, x_axis)
        angles = np.arctan2(np.dot(v_centered, y_axis), np.dot(v_centered, x_axis))
        sort_order = np.argsort(angles)
        faces.append(face_verts[sort_order])
        centers.append(center)
    return faces, np.array(centers)

def get_rotation_to_target(source_vec, target_lat, target_lon):
    t_lat_r, t_lon_r = np.radians(target_lat), np.radians(target_lon)
    target_vec = np.array([
        np.cos(t_lat_r) * np.cos(t_lon_r),
        np.cos(t_lat_r) * np.sin(t_lon_r),
        np.sin(t_lat_r)
    ])
    axis = np.cross(source_vec, target_vec)
    axis_norm = np.linalg.norm(axis)
    if axis_norm < 1e-6: return R.identity()
    axis = axis / axis_norm
    angle = np.arccos(np.dot(source_vec, target_vec))
    return R.from_rotvec(axis * angle)

def main():
    print("💎 GENERANDO HOLOGRAMA DE BITS (CAPITULO 20)...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    face_status = get_face_status()
    verts = get_dodecahedron_geometry()
    faces_raw, centers_raw = get_faces(verts)
    
    rot = get_rotation_to_target(centers_raw[0], ALPHA_LAT, ALPHA_LON)
    rotated_faces = []
    for face in faces_raw:
        rotated_faces.append(rot.apply(face))
        
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Estilo Holográfico: Cyan, Transparente, Wireframe brillante
    for i, poly in enumerate(rotated_faces):
        status = face_status[i] if i < len(face_status) else 1
        
        if status == 1:
            color = '#00FFFF' # Cyan
            edge = '#00FFFF'
            alpha = 0.1 # Muy transparente
            lw = 0.5
        else:
            color = '#FF0000' 
            edge = '#FF0000'
            alpha = 0.1
            lw = 0.5
        
        poly3d = Poly3DCollection([poly], alpha=alpha, linewidths=lw)
        poly3d.set_facecolor(color)
        poly3d.set_edgecolor(edge)
        ax.add_collection3d(poly3d)
        
        # Puntos en los vértices (Bits)
        ax.scatter(poly[:,0], poly[:,1], poly[:,2], color='white', s=5, alpha=0.8)

        # Texto
        center = np.mean(poly, axis=0) * 1.15
        ax.text(center[0], center[1], center[2], f"{i+1}", color=edge, fontsize=10, ha='center')

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_axis_off()
    
    plt.title("HOLOGRAPHIC SURFACE DENSITY\nMeasured L = 3.27e26 m", color='white')
    
    # Guardar solo la vista frontal
    ax.view_init(elev=30, azim=0)
    filename = f'{OUTPUT_DIR}/hologram_universe_bits.png'
    plt.savefig(filename, facecolor='black', dpi=150)
    print(f"📸 Holograma guardado: {filename}")

if __name__ == "__main__":
    main()
