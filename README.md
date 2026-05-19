# 📊 PetLytics — Retail Pricing Intelligence

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Pipeline-Activo%20·%20Diario-22c55e)

Plataforma analítica *end-to-end* que monitorea, normaliza y visualiza datos de precios del mercado de alimentos para mascotas en Argentina. El proyecto implementa un pipeline ELT productivo con actualización diaria, almacenamiento cloud y un dashboard de inteligencia de precios orientado a decisiones de negocio.

🌍 **[Ver Dashboard en Vivo →](https://petlytics.streamlit.app/)**

---

## 🎯 Problema de Negocio

El mercado minorista de alimentos para mascotas presenta tres fricciones analíticas concretas:

| Problema | Impacto |
|---|---|
| Alta dispersión de precios entre retailers para el mismo producto | El consumidor paga hasta un **18% más** por no comparar canales |
| Penalidad por fraccionamiento oculta | Las bolsas chicas (≤3 kg) cuestan hasta un **60% más por kg** que el volumen (≥15 kg) |
| Datos no estructurados e inconsistentes entre fuentes | Imposibilidad de comparar "manzanas con manzanas" sin normalización previa |

**PetLytics resuelve los tres problemas** consolidando datos de múltiples retailers en un modelo analítico único, normalizado y actualizado diariamente.

---

## 🏗️ Arquitectura del Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        MODERN DATA STACK                        │
├──────────────┬──────────────────┬──────────────┬───────────────┤
│   EXTRACT    │    TRANSFORM     │     LOAD     │    PRESENT    │
│              │                  │              │               │
│  Python      │  Pandas · NumPy  │  PostgreSQL  │  Streamlit    │
│  Scraper     │  Regex · Rules   │  Neon DB     │  Plotly       │
│              │                  │  (Cloud)     │               │
│  ┌────────┐  │  ┌────────────┐  │  ┌────────┐  │  ┌─────────┐ │
│  │MercadoL│  │  │Normalizar  │  │  │historico│  │  │Dashboard│ │
│  │Puppis  │─►│  │peso/precio │─►│  │_precios│─►│  │KPIs     │ │
│  │NatLife │  │  │Clasificar  │  │  │        │  │  │Vitrina  │ │
│  │...     │  │  │Deal Score  │  │  │        │  │  │Heatmap  │ │
│  └────────┘  │  └────────────┘  │  └────────┘  │  └─────────┘ │
└──────────────┴──────────────────┴──────────────┴───────────────┘
                        ↑ corre diariamente ↑
```

### Detalle por capa

**1. Extract — Ingesta asíncrona**
Scripts en Python que capturan datos crudos de los principales retailers, resolviendo barreras de seguridad (TLS/Cloudflare). Cada corrida genera un snapshot diario con timestamp de extracción.

**2. Transform — Data Quality & Normalización**
- **Parsing de pesos:** extracción de valores numéricos (kg/g) desde texto libre con RegEx
- **Resolución de multipacks:** descomposición de promociones "3x1" al precio unitario real
- **Clasificación heurística:** reglas condicionales para corregir categorías mal etiquetadas en origen (ej. relación peso > 7.5 kg + ausencia de keyword "gato" → clasificar como perro)
- **Deal Score:** comparación del precio actual vs. promedio histórico del mismo producto para detectar ofertas reales

**3. Load — Storage cloud**
Modelo relacional persistente en PostgreSQL serverless (Neon DB). El historial acumulado de snapshots es lo que hace posible el análisis temporal y el cálculo del Deal Score.

**4. Present — Capa semántica**
Dashboard interactivo que traduce el modelo analítico a KPIs de negocio accionables para usuarios no técnicos.

---

## 💡 Features del Dashboard

### 📈 Business Insights (Dashboard)
- **9 KPIs** organizados en 3 filas: precio promedio, brecha entre retailers, sobreprecio por fraccionamiento, inflación acumulada del período, tendencia de 7 días, ahorro máximo posible, vendedores monitoreados, diferencia tienda oficial vs. terceros y mejor canal del día
- **Insight automático** en lenguaje natural: detecta el retailer más eficiente y calcula el ahorro concreto vs. el más caro
- **Gráfico de barras** por retailer con codificación de color (verde = más barato, rojo = más caro)
- **Line chart** de evolución de precios por segmento de calidad (Premium / Estándar / Económico)
- **Box plot por marca:** visualiza la dispersión de precios entre canales — cajas anchas indican alta variabilidad, lo que señala dónde conviene comparar antes de comprar
- **Heatmap marca × retailer:** matriz de precio promedio por kg — permite identificar de un vistazo en qué tienda comprar cada marca específica
- **Scatter plot** peso vs. precio/kg con línea de tendencia (LOWESS) para visualizar la eficiencia de comprar en volumen

### 🛒 Vitrina de Ofertas
- Buscador multipalabra en tiempo real
- Ordenamiento por mayor descuento, menor precio/kg o menor precio total
- Slider de descuento mínimo (umbral configurable por el usuario)
- Toggle "Solo tienda oficial" usando la columna `es_tienda_oficial`
- Badge 🔥 con porcentaje de descuento vs. precio histórico
- Precio histórico tachado visible para contextualizar la oferta
- Indicador de vendedor y badge "✓ Oficial" por card
- Contador dinámico: productos mostrados, total disponible y cantidad de ofertas reales detectadas

### ⚙️ Exportación
Descarga del modelo analítico filtrado en CSV para análisis externo.

---

## 🚀 Stack Tecnológico

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Extracción | Requests, BeautifulSoup |
| Transformación | Pandas, NumPy, Regex |
| Base de datos | PostgreSQL · SQLAlchemy |
| Cloud storage | Neon DB (serverless) |
| Visualización | Streamlit, Plotly Express |
| Despliegue | Streamlit Community Cloud |

---

## 📁 Estructura del Proyecto

```
petlytics/
├── app.py                  # Dashboard principal (Streamlit)
├── scraper/
│   └── extractor.py        # Scripts de ingesta por retailer
├── pipeline/
│   └── transform.py        # Lógica de normalización y Deal Score
├── requirements.txt
└── .streamlit/
    └── secrets.toml        # Credenciales (no versionado)
```

---

## 🛠️ Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/ACMansor26/petlytics-dashboard.git
cd petlytics-dashboard

# 2. Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar credenciales
mkdir .streamlit
```

Crear `.streamlit/secrets.toml` con el siguiente contenido:

```toml
[database]
url = "postgresql://usuario:password@host/db?sslmode=require"
```

```bash
# 4. Ejecutar
streamlit run app.py
```

> ⚠️ El dashboard en producción usa una base de datos con datos reales en Neon DB. En local podés apuntar a tu propia instancia de PostgreSQL con el mismo esquema de tabla (`historico_precios`).

---

## 🗄️ Esquema de la Base de Datos

```sql
CREATE TABLE historico_precios (
    id_publicacion    TEXT,
    fecha_extraccion  DATE,
    plataforma        TEXT,
    marca             TEXT,
    gama              TEXT,          -- Premium / Estándar / Económico
    titulo_original   TEXT,
    precio_total      NUMERIC,
    peso_kg           NUMERIC,
    precio_por_kg     NUMERIC,       -- métrica normalizada central
    vendedor          TEXT,
    es_tienda_oficial BOOLEAN,
    url               TEXT,
    imagen_url        TEXT,
    categoria         TEXT           -- perro / gato
);
```

---

## 👤 Autor

**Amir Mansor** — Analytics Engineer  
🔗 [LinkedIn](https://www.linkedin.com/in/amir-mansor25/) · 🐙 [GitHub](https://github.com/ACMansor26)
