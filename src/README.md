# 🌫️ Simulación de Montecarlo para Análisis de Calidad del Aire en Lima — HPC

> **Curso:** Computación de Alto Desempeño y Cloud Computing — 2026-I  
> **Universidad:** Universidad del Pacífico  
> **Docente:** MSc Juan Carlos Tovar Galarreta  

---

## 👥 Integrantes

| Nombre completo | Rol en el proyecto |
|---|---|
| Apellido, Nombre 1 | Introducción y contexto |
| Apellido, Nombre 2 | Estado del arte |
| Apellido, Nombre 3 | Dataset y exploración |
| Scarpati, Gianfranco | Metodología y arquitectura |

---

## 📌 Descripción del Proyecto

Este proyecto aplica **simulación de Montecarlo paralelizada** para analizar los niveles de contaminantes del aire en Lima Metropolitana. Mediante técnicas de **Computación de Alto Desempeño (HPC)** y **Cloud Computing**, se busca reducir el tiempo de simulación y modelar distribuciones de probabilidad de concentraciones de contaminantes como PM2.5, PM10, NO₂ y O₃.

El dataset utilizado proviene del Servicio Nacional de Meteorología e Hidrología del Perú (SENAMHI), disponible en la Plataforma Nacional de Datos Abiertos.

---

## 🗂️ Estructura del Repositorio

```
proyecto-montecarlo-hpc/
│
├── README.md                        ← Este archivo
├── LICENSE                          ← Licencia MIT
│
├── data/
│   └── README.md                    ← Instrucciones para descargar el dataset
│
├── notebooks/
│   └── avance_parcial.ipynb         ← Cuadernillo principal (carga → limpieza → simulación)
│
├── src/                             ← Scripts Python modulares (informe final)
│   ├── preprocessing.py
│   └── montecarlo.py
│
└── informe/
    ├── informe_parcial.tex          ← Fuente LaTeX
    └── informe_parcial.pdf          ← PDF compilado para entrega
```

---

## 📊 Dataset

**Nombre:** Datos Horarios de Contaminantes del Aire en Lima Metropolitana  
**Fuente:** SENAMHI / Plataforma Nacional de Datos Abiertos del Perú  
**URL:** https://www.datosabiertos.gob.pe/dataset/datos-horarios-de-contanimantes-del-aire-en-limametropolitana-servicio-nacional-de  
**Registros:** > 30,000 observaciones horarias  
**Variables principales:** fecha_hora, estacion, PM2.5, PM10, NO₂, O₃, CO, SO₂, temperatura, humedad  

> ⚠️ El archivo de datos no está incluido en este repositorio por su tamaño.  
> Descárgalo desde la URL de arriba y colócalo en la carpeta `data/`.

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/[USUARIO]/proyecto-montecarlo-hpc.git
cd proyecto-montecarlo-hpc
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Descargar el dataset
Descarga el dataset desde la URL indicada arriba y guárdalo como:
```
data/contaminantes_lima.csv
```

### 4. Ejecutar el cuadernillo
Abre el cuadernillo en Jupyter o Google Colab:
```bash
jupyter notebook notebooks/avance_parcial.ipynb
```

---

## 🛠️ Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| Pandas | Carga y limpieza de datos |
| NumPy | Operaciones numéricas y muestreo |
| Dask / multiprocessing | Paralelización de simulaciones |
| Matplotlib / Seaborn | Visualización |
| Google Colab / [Cloud] | Entorno de ejecución en la nube |
| LaTeX (Overleaf) | Redacción del informe |

---

## 📈 Métricas de rendimiento evaluadas

- **Speedup** (S_p = T_1 / T_p)
- **Eficiencia** (E = S_p / p)
- **Escalabilidad** según número de núcleos y tamaño del problema

---


## 📚 Referencias

Las referencias completas están en el informe (`informe/informe_parcial.pdf`).  
Papers principales consultados:
- [Referencia 1 — completar]
- [Referencia 2 — completar]
- [Referencia 3 — completar]
