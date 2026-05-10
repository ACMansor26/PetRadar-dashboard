# 📊 PetLytics | Retail Analytics Pipeline & Dashboard

Plataforma analítica integral (*End-to-End*) diseñada para monitorear, normalizar y visualizar datos del mercado de alimentos para mascotas. Este proyecto demuestra la implementación de un pipeline ELT moderno, aplicando capas de *Data Quality* y despliegue en la nube para optimizar decisiones comerciales y de *pricing*.

🌍 **[Ver Dashboard en Vivo]([https://tu-link-de-streamlit.app](https://petlytics.streamlit.app/))

---

## 🎯 Objetivo de Negocio
El mercado minorista (*retail*) de alimentos para mascotas presenta una alta dispersión de precios, descripciones de productos inconsistentes y múltiples formatos de empaque (SKUs). 

El objetivo de este producto de datos es:
1. **Detectar ineficiencias de mercado:** Identificar el canal de compra más eficiente para cada producto.
2. **Analizar la penalidad por fraccionamiento:** Calcular el sobreprecio que asume el consumidor al adquirir presentaciones de bajo volumen.
3. **Estandarizar datos no estructurados:** Limpiar y normalizar el catálogo de múltiples proveedores para permitir comparaciones precisas ("manzanas con manzanas").

---

## 🏗️ Arquitectura de Datos (Modern Data Stack)

El proyecto está diseñado bajo la filosofía de **Analytics Engineering**, separando claramente la extracción, la transformación y la capa semántica.

1. **Ingesta Asíncrona (Extract):** Scripts en Python que capturan datos crudos de los principales *retailers* del mercado (Mercado Libre, Puppis, Natural Life, etc.).
2. **Data Quality & Transformación (ELT):** Procesamiento vectorizado utilizando `Pandas` y `NumPy`.
   * **Parsing avanzado:** Extracción de pesos (Kg) a partir de descripciones de texto y resolución de promociones multipack.
   * **Clasificación Heurística:** Uso de expresiones regulares (RegEx) estrictas y lógica condicional (ej. relación de peso > 7.5kg y ausencia de la palabra 'gato') para inferir y corregir categorías de mascotas mal etiquetadas en origen.
3. **Storage Cloud (Load):** Almacenamiento centralizado y persistente en una instancia relacional de **PostgreSQL (Neon DB)**.
4. **Capa Semántica & BI (Presentation):** Dashboard interactivo construido con **Streamlit** y **Plotly**, diseñado para usuarios de negocio, incluyendo *tooltips* explicativos y generación dinámica de *insights*.

---

## 🚀 Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Transformación de Datos:** Pandas, NumPy, Regex
* **Base de Datos:** PostgreSQL, SQLAlchemy (alojado en Neon)
* **Visualización & UI:** Streamlit, Plotly Express
* **Despliegue:** Streamlit Community Cloud

---

## 💡 Características Principales del Dashboard

* 📈 **Business Insights Automatizados:** Un motor de reglas redacta conclusiones en lenguaje natural sobre las brechas de precio actuales.
* 🧮 **Métricas (KPIs):** Spread de Mercado, Costo Promedio, Variación Temporal y Costo de Fraccionamiento.
* 🛒 **Vitrina Operativa:** Buscador multipalabra de texto libre para encontrar oportunidades de ahorro puntuales, aplicando lógica condicional de diversificación de marcas.
* 📥 **Exportación de Datos:** Permite a los usuarios de negocio descargar el modelo de datos analítico resultante (CSV) afectado por los filtros en pantalla.

---

## 🛠️ Instrucciones de Instalación Local

Si deseás clonar y ejecutar este proyecto en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/petlytics-dashboard.git](https://github.com/tu-usuario/petlytics-dashboard.git)
   cd petlytics-dashboard

2. **Crear un entorno virtual e instalar dependencias:**
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

3. **Configurar las credenciales (Secrets):**
Creá una carpeta oculta llamada .streamlit en la raíz del proyecto.

Dentro de esa carpeta, creá un archivo secrets.toml.

Agregá la cadena de conexión a tu base de datos PostgreSQL
