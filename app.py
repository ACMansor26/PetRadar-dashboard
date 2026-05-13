import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="PetLytics | Pricing Analytics", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: transparent; }
    
    /* TARJETAS DE MÉTRICAS (KPIs) */
    [data-testid="stMetric"] {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--secondary-background-color); 
        background-color: var(--background-color); 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        height: 145px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    [data-testid="stMetricLabel"] { font-weight: 600 !important; }
    [data-testid="stMetricValue"] { font-size: 32px !important; }

    /* Estilo para bajas de precio (Verde) - Usamos inverse para inflación */
    [data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaIcon-Down"] { color: #15803d !important; }
    [data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaIcon-Down"] + div { color: #15803d !important; font-weight: 700 !important; }
    
    /* UI/UX VITRINA */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #3b82f6 !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.2) !important;
        transform: translateY(-5px) !important;
    }
    div[data-testid="stLinkButton"] a {
        background-color: #3b82f6 !important;
        border-color: #3b82f6 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def cargar_datos_neon():
    try:
        # En producción usa st.secrets. Para pruebas locales podés dejar tu string.
        DATABASE_URL = "postgresql://neondb_owner:npg_dZ6hozpYA0ut@ep-little-flower-acv5xn2k.sa-east-1.aws.neon.tech/neondb?sslmode=require"
        engine = create_engine(DATABASE_URL)
        
        # Filtramos directamente en SQL los últimos 30 días para escalabilidad
        query = """
            SELECT * FROM historico_precios 
            WHERE fecha_extraccion >= CURRENT_DATE - INTERVAL '30 days'
        """
        df = pd.read_sql(query, engine)
        df['fecha_extraccion'] = pd.to_datetime(df['fecha_extraccion']).dt.date
        df['gama'] = df['gama'].replace('Estandar', 'Estándar') 
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

def main():
    df = cargar_datos_neon()
    if df.empty: return

    # --- BARRA LATERAL (BRANDING PERSONAL) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120) 
        st.markdown("### Hecho por:")
        st.markdown("**Amir Mansor**")
        st.markdown("🚀 *Analytics Engineer*")
        st.divider()
        st.markdown("Conectemos:")
        st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/amir-mansor25/)")
        st.markdown("🐙 [GitHub](https://github.com/ACMansor26)")
        st.divider()
        st.caption("Modelo analítico alimentado mediante un pipeline ELT desde PostgreSQL.")

    # --- BLOQUE 1: TÍTULO Y FILTROS GLOBALES ---
    col_t, col_f = st.columns([2, 1])
    with col_t:
        st.title("📊 PetLytics | Retail Data Hub")
        st.markdown("##### Motor de inteligencia competitiva para el mercado de mascotas.")
        
        st.markdown("""
        Esta herramienta consolida datos no estructurados de los principales canales de *retail* para neutralizar la asimetría de precios. Su arquitectura en la nube permite detectar ofertas reales mediante promedios móviles, monitorear la inflación por segmento y cuantificar el sobreprecio por fraccionamiento.
        
        **Instrucciones:** Utilizá los filtros y descubrí oportunidades de mercado en tiempo real.
        """)

    with col_f:
        with st.container(border=True):
            f1, f2 = st.columns(2)
            with f1:
                mascota = st.selectbox("Mascota", ["Ambas"] + sorted(list(df['categoria'].unique())))
                marcas_seleccionadas = st.multiselect("Marca", options=sorted(list(df['marca'].unique())), placeholder="Elegí una o varias")
            with f2:
                gama = st.selectbox("Calidad", ["Todas"] + sorted(list(df['gama'].unique())))
                tienda = st.selectbox("Tienda", ["Todas"] + sorted(list(df['plataforma'].unique())))

    # Filtrado Dinámico
    df_f = df.copy()
    if mascota != "Ambas": df_f = df_f[df_f['categoria'] == mascota]
    if marcas_seleccionadas: df_f = df_f[df_f['marca'].isin(marcas_seleccionadas)]
    if gama != "Todas": df_f = df_f[df_f['gama'] == gama]
    if tienda != "Todas": df_f = df_f[df_f['plataforma'] == tienda]

    # Cálculos globales
    fechas = sorted(df_f['fecha_extraccion'].unique(), reverse=True)
    avg_total = df_f['precio_por_kg'].mean()
    brecha_marca = df_f.groupby('marca')['precio_por_kg'].agg(lambda x: x.max() - x.min()).mean()
    
    # 1. Macroeconomía: Índice Pet-Flación (Nuevo)
    pet_flacion = 0
    dias_periodo = 0
    tendencia = 0
    dif_pesos = 0
    if len(fechas) > 1:
        # Variación diaria
        p_actual = df_f[df_f['fecha_extraccion'] == fechas[0]]['precio_por_kg'].mean()
        p_prev = df_f[df_f['fecha_extraccion'] == fechas[1]]['precio_por_kg'].mean()
        if p_prev > 0:
            tendencia = (p_actual - p_prev) / p_prev
            dif_pesos = p_actual - p_prev
            
        # Variación Acumulada (Pet-Flación)
        fecha_reciente = fechas[0]
        fecha_antigua = fechas[-1]
        p_base = df_f[df_f['fecha_extraccion'] == fecha_antigua]['precio_por_kg'].mean()
        if p_base > 0:
            pet_flacion = (p_actual - p_base) / p_base
        dias_periodo = (fecha_reciente - fecha_antigua).days

    p_volumen = 0
    p_chicas = df_f[df_f['peso_kg'] <= 3]['precio_por_kg'].mean()
    p_grandes = df_f[df_f['peso_kg'] >= 15]['precio_por_kg'].mean()
    if p_chicas > 0 and p_grandes > 0: p_volumen = (p_chicas - p_grandes) / p_chicas

    # --- CREACIÓN DE PESTAÑAS (TABS) ---
    tab_dashboard, tab_vitrina, tab_tecnica = st.tabs([
        "📈 Business Insights", 
        "🛒 Vitrina de ofertas", 
        "⚙️ Arquitectura ELT"
    ])

    # ==========================================
    # PESTAÑA 1: DASHBOARD
    # ==========================================
    with tab_dashboard:
        df_bar_data = df_f.groupby('plataforma')['precio_por_kg'].mean().sort_values().reset_index()
        if not df_bar_data.empty and len(df_bar_data) >= 2:
            t_min = df_bar_data.iloc[0]['plataforma']
            t_max = df_bar_data.iloc[-1]['plataforma']
            st.info(f"💡 **Insight Macro:** En los últimos {dias_periodo} días, la cohorte analizada registró una inflación acumulada del **{pet_flacion:+.1%}**. Operativamente, migrar la compra del canal más costoso (*{t_max}*) al más eficiente (*{t_min}*) neutraliza este impacto de mercado.")

        # Reorganizamos en 2 filas de 3 KPIs para mejor lectura
        k1, k2, k3 = st.columns(3)
        k1.metric("Costo promedio (Kg)", f"${avg_total:,.0f}", help="Costo promedio por kilogramo ponderado sobre el set de datos actual.")
        k2.metric("Spread Promedio (Max-Min)", f"${brecha_marca:,.0f}", help="Dispersión detectada para un mismo producto entre canales.")
        k3.metric("Costo de Fraccionamiento", f"{p_volumen:.1%}", help="Sobreprecio asumido al adquirir formatos <=3kg vs volumen (15kg+).")

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        k4, k5, k6 = st.columns(3)
        k4.metric("Inflación Acumulada (Periodo)", f"{pet_flacion:+.1%}", delta=f"{pet_flacion:+.2%}", delta_color="inverse", help=f"Índice Base 100 de la variación de precios en los últimos {dias_periodo} días.")
        k5.metric("Variación Marginal (Ayer)", f"${abs(dif_pesos):,.0f}", delta=f"{tendencia:+.2%}", delta_color="inverse", help="Ajuste de precio detectado en la última corrida del pipeline.")
        k6.metric("Eficiencia Máxima de Canal", f"{( (df_bar_data.iloc[-1]['precio_por_kg'] - df_bar_data.iloc[0]['precio_por_kg']) / df_bar_data.iloc[-1]['precio_por_kg'] ):.1%}" if not df_bar_data.empty else "0%", help="Ahorro posible entre el retailer más caro y el más barato del día.")

        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            with st.container(border=True):
                st.markdown("**Promedio de costos por tienda**")
                n = len(df_bar_data)
                colores = ['#22c55e'] + ['#3b82f6'] * (n - 2) + ['#ef4444'] if n > 2 else ['#22c55e', '#ef4444']
                df_bar_data['texto'] = df_bar_data['precio_por_kg'].apply(lambda x: f"${x:,.0f}")
                fig1 = px.bar(df_bar_data, x="plataforma", y="precio_por_kg", text="texto")
                fig1.update_traces(marker_color=colores, textposition='inside')
                fig1.update_layout(height=300, showlegend=False, xaxis_title=None, yaxis_title=None, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig1, use_container_width=True)

        with g2:
            with st.container(border=True):
                st.markdown("**Curva de precios por segmento**")
                df_line = df_f.groupby(['fecha_extraccion', 'gama'])['precio_por_kg'].mean().reset_index()
                fig2 = px.line(df_line, x="fecha_extraccion", y="precio_por_kg", color="gama", markers=True)
                fig2.update_layout(height=300, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=None), margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                fig2.update_xaxes(tickformat="%d %b")
                st.plotly_chart(fig2, use_container_width=True)

    # ==========================================
    # PESTAÑA 2: VITRINA CON DEAL SCORE
    # ==========================================
    with tab_vitrina:
        st.subheader("🛒 Detección de Oportunidades")
        busqueda = st.text_input("Buscador de oportunidades (Ej: Pro Plan Adulto)", placeholder="Parámetros de búsqueda...")
        
        if len(fechas) > 0:
            # 1. Calculamos el promedio histórico de cada producto en todo el DF
            hist_avg = df_f.groupby('titulo_original')['precio_por_kg'].mean().reset_index()
            hist_avg.rename(columns={'precio_por_kg': 'precio_hist_promedio'}, inplace=True)
            
            # 2. Aislamos la foto de hoy
            df_vitrina = df_f[df_f['fecha_extraccion'] == fechas[0]].copy()
            
            # 3. Cruzamos (Join) los datos de hoy con su promedio histórico
            df_vitrina = pd.merge(df_vitrina, hist_avg, on='titulo_original', how='left')
            
            # 4. DEAL SCORE: Calculamos si hoy está más barato que su propia historia
            df_vitrina['descuento_vs_hist'] = (df_vitrina['precio_hist_promedio'] - df_vitrina['precio_por_kg']) / df_vitrina['precio_hist_promedio']
            
            if busqueda:
                for palabra in busqueda.strip().split():
                    df_vitrina = df_vitrina[df_vitrina['titulo_original'].str.contains(palabra, case=False, na=False)]
                df_top = df_vitrina.sort_values('precio_por_kg', ascending=True).head(24)
            else:
                df_top = df_vitrina.sort_values('precio_por_kg').groupby('marca').head(2).head(20)
            
            if df_top.empty:
                st.info("La query no devolvió resultados en el snapshot actual.")
            else:
                cols = st.columns(4)
                for i, row in df_top.reset_index().iterrows():
                    with cols[i % 4]:
                        with st.container(border=True):
                            img = row.get('imagen_url') if pd.notna(row.get('imagen_url')) else 'https://via.placeholder.com/150'
                            
                            # Generación del Badge de Oferta Real (Flotante)
                            oferta_badge = ""
                            if row.get('descuento_vs_hist', 0) >= 0.05: 
                                dcto = row['descuento_vs_hist'] * 100
                                # Agregamos position: absolute y ajustamos los bordes/sombras
                                oferta_badge = f"""<div style="position: absolute; bottom: 8px; left: 8px; background-color: #ef4444; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">🔥 OFERTA REAL (-{dcto:.0f}%)</div>"""

                            # En el div contenedor de la imagen agregamos: position: relative;
                            st.markdown(f"""
                                <div style="background-color: white; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: center; height: 160px; padding: 10px; position: relative;">
                                    <img src="{img}" style="max-height: 100%; object-fit: contain;">
                                    {oferta_badge}
                                </div>
                                <p title='{row['titulo_original']}' style='font-weight: 600; line-height: 1.2; height: 40px; overflow: hidden; margin-bottom: 5px;'>{str(row['titulo_original'])[:40]}...</p>
                                <div style="margin-bottom: 10px;">
                                    <span style="color: #94a3b8; font-size: 0.8rem;">Facturación:</span> <strong style="font-size: 1.2rem; color: #3b82f6;">${row['precio_total']:,.0f}</strong><br>
                                    <span style="color: #94a3b8; font-size: 0.8rem;">Costo/Kg:</span> <strong>${row['precio_por_kg']:,.0f}</strong>
                                </div>
                                <div style="display: flex; gap: 5px; margin-bottom: 10px; flex-wrap: wrap;">
                                    <span style="background-color: rgba(148,163,184,0.1); border: 1px solid rgba(148,163,184,0.2); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">🏢 {row['plataforma']}</span>
                                    <span style="background-color: rgba(148,163,184,0.1); border: 1px solid rgba(148,163,184,0.2); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">⚖️ {row['peso_kg']}kg</span>
                                </div>
                            """, unsafe_allow_html=True)
                            st.link_button("Ir a la publicación", row.get('url', '#'), type="primary", use_container_width=True)

    # ==========================================
    # PESTAÑA 3: ARQUITECTURA
    # ==========================================
    with tab_tecnica:
        st.markdown("### ⚙️ Fundamentos de la Arquitectura de Datos")
        st.markdown("""
        * **1. Extracción (Ingesta):** Recolección automatizada resolviendo barreras de seguridad (TLS/Cloudflare) para garantizar flujo de datos diario.
        * **2. Transformación (ELT & Quality):** Lógica vectorizada en Pandas para unificar monedas, normalizar métricas y aplicar heurísticas de negocio (ej. Deal Scoring mediante media móvil).
        * **3. Persistencia (Storage):** Modelado en esquema relacional y carga en PostgreSQL Cloud (Neon DB).
        * **4. Presentación (Semántica):** Traducción de datos limpios a KPIs financieros auditables en tiempo real, maximizando el *Time-to-Insight*.
        """)
        
        st.divider()
        st.markdown("#### 📥 Democratización de datos")
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Modelo Analítico Filtrado (CSV)",
            data=csv,
            file_name='modelo_analitico_petlytics.csv',
            mime='text/csv',
            type="primary"
        )

    # --- FOOTER PROFESIONAL ---
    st.markdown("""
        <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--secondary-background-color); color: #94a3b8; font-size: 0.85rem;">
            PetLytics Market Monitor v2.0 &copy; 2026<br>
            Construido mediante Analytics Engineering para la neutralización de la asimetría de precios.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
