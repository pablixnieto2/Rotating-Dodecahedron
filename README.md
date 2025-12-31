# Toolkit: The Reader's Laboratory / El Laboratorio del Lector

---
## 🇬🇧 ENGLISH VERSION

> **WARNING:** This document is purely technical. It provides instructions to reproduce the scientific findings using the provided Python scripts.

To replicate the discoveries of this project, you will need to set up your own "Digital Observatory". No telescope required, just a computer and Python.

### 1. Raw Data: Planck Satellite Maps

All our research is based on public data from the ESA Planck Mission.
*   **Official Source:** Planck Legacy Archive (PLA) - [https://pla.esac.esa.int/#maps](https://pla.esac.esa.int/#maps)
*   **Recommended File:** 2018 Release (PR3), Intensity Map:
    *   `COM_CMB_IQU-sevem_2048_R4.00.fits`

### 2. Tools: Scripts and Algorithms

The source code is open. We have released the scripts used to detect the Dodecahedron, measure dark energy, and hunt for galactic clones.

#### Quick Setup
1.  **Unzip the archive:**
    Extract the contents of the downloaded file.
    ```bash
    cd CCC_Fractal_Analysis
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Execution Guide

*   **macOS / Linux:** Use the Terminal. Activate a virtual environment (`python3 -m venv venv`) and run the scripts (e.g., `python src/scripts/main_fractal.py`).
*   **Windows:** We highly recommend using **WSL (Windows Subsystem for Linux)** for better compatibility with `healpy`.

### 4. Project Structure
*   `src/`: Contains source code organized by chapter/topic.
*   `data/`: Place your downloaded `.fits` files here.
*   `images/`: Output graphics will appear here.

---
## 🇪🇸 VERSIÓN EN ESPAÑOL

> **AVISO:** Este documento es puramente técnico. Si solo te interesa la narrativa del descubrimiento, puedes saltar directamente al Capítulo 1 del libro. Si quieres ensuciarte las manos con el código y verificar los hallazgos por ti mismo, este es tu lugar.

Para replicar los descubrimientos de este libro, necesitarás montar tu propio "Observatorio Digital". No necesitas un telescopio, solo un ordenador y una conexión a internet.

### 1. La Materia Prima: Datos del Satélite Planck

Toda nuestra investigación se basa en los datos públicos de la misión Planck de la Agencia Espacial Europea (ESA). Estos archivos contienen el mapa de temperatura del universo más preciso jamás creado.

*   **Fuente Oficial:** Planck Legacy Archive (PLA)
*   **URL:** [https://pla.esac.esa.int/#maps](https://pla.esac.esa.int/#maps)
*   **Archivo Recomendado:** Busca los mapas de la release 2018 (PR3). El archivo principal que usamos es el mapa de intensidad completa:
    *   `COM_CMB_IQU-sevem_2048_R4.00.fits`

### 2. Las Herramientas: Scripts y Algoritmos

El código fuente de este proyecto es abierto. Hemos liberado los scripts que usamos para detectar el Dodecaedro, medir la energía oscura y buscar clones galácticos.

#### Instalación Rápida

1.  **Descomprime el archivo:**
    Extrae el contenido del archivo descargado.
    ```bash
    cd CCC_Fractal_Analysis
    ```

2.  **Instala las dependencias:**
    El proyecto usa Python 3. Necesitarás librerías científicas estándar (`numpy`, `matplotlib`, `astropy`) y la librería especializada de la NASA para mapas esféricos (`healpy`).
    ```bash
    pip install -r requirements.txt
    ```

### 3. Guía de Ejecución por Sistema Operativo

*   **macOS (Terminal):** Mac es ideal para esto ya que es UNIX. Crea un entorno virtual (`python3 -m venv venv`) y ejecuta los scripts.
*   **Linux (Ubuntu/Debian):** El entorno nativo de la ciencia de datos.
*   **Windows:** Recomendamos **WSL (Windows Subsystem for Linux)**. `healpy` suele funcionar mucho mejor y más rápido en este entorno.

### 4. Estructura del Proyecto

Cada capítulo del libro tiene su correspondencia en las carpetas del código:
*   `src/`: Contiene el código fuente numerado por capítulos.
*   `data/`: Aquí debes poner los archivos `.fits` que descargues de la ESA.
*   `images/`: Aquí aparecerán las gráficas que generes.
