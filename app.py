import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="PetLytics | Monitor de Mercado", page_icon="🐾", layout="wide")

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

    /* Estilo para bajas de precio (Verde) */
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
    DATABASE_URL = st.secrets["DATABASE_URL"] 
    try:
        engine = create_engine(DATABASE_URL)
        
        # EL UPGRADE: Pushdown computation con ventana móvil de 30 días
        query = """
            SELECT * FROM historico_precios 
            WHERE fecha_extraccion >= CURRENT_DATE - INTERVAL '30 days'
        """
        
        df = pd.read_sql(query, engine)
        df['fecha_extraccion'] = pd.to_datetime(df['fecha_extraccion'])
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
        st.markdown("### Creado por")
        st.markdown("**Amir Mansor**")
        st.markdown("🚀 *Analytics Engineer*")
        st.divider()
        st.markdown("Conectemos:")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/amir-mansor25/)")
        st.markdown("[GitHub](https://github.com/ACMansor26)")
        st.divider()
        st.caption("Los precios de esta web se actualizan automáticamente Martes y Viernes buscando las mejores ofertas.")

    # --- BLOQUE 1: TÍTULO Y FILTROS GLOBALES ---
    col_t, col_f = st.columns([2, 1])
    with col_t:
        st.title("🐾 PetLytics | Monitor de Mercado")
        st.markdown("##### Comparador automático de precios y oportunidades de ahorro.")
        
        st.markdown("""
        Bienvenido al buscador inteligente de alimento para mascotas. Dos veces por semana, nuestro sistema recorre las principales tiendas (Mercado Libre, Puppis, Natural Life y Catycan) para ayudarte a encontrar el alimento de tu mascota al **mejor precio real (por kilo)**.
        
        👉 **¿Cómo funciona?** Usá los filtros de la derecha para elegir lo que buscás, y navegá por las pestañas de abajo para ver el resumen del mercado o ir directo a la vitrina de ofertas.
        """)

    with col_f:
        with st.container(border=True):
            f1, f2 = st.columns(2)
            with f1:
                mascota = st.selectbox("Mascota", ["Ambas"] + sorted(list(df['categoria'].unique())))
                marcas_seleccionadas = st.multiselect(
                    "Marca(s)", 
                    options=sorted(list(df['marca'].unique())), 
                    placeholder="Elegí una o varias (Vacío = Todas)"
                )
            with f2:
                gama = st.selectbox("Calidad", ["Todas"] + sorted(list(df['gama'].unique())))
                tienda = st.selectbox("Tienda", ["Todas"] + sorted(list(df['plataforma'].unique())))

    # Filtrado del DataFrame
    df_f = df.copy()
    if mascota != "Ambas": df_f = df_f[df_f['categoria'] == mascota]
    if marcas_seleccionadas: df_f = df_f[df_f['marca'].isin(marcas_seleccionadas)]
    if gama != "Todas": df_f = df_f[df_f['gama'] == gama]
    if tienda != "Todas": df_f = df_f[df_f['plataforma'] == tienda]

    # Cálculos globales
    fechas = sorted(df_f['fecha_extraccion'].unique(), reverse=True)
    avg_total = df_f['precio_por_kg'].mean()
    brecha_marca = df_f.groupby('marca')['precio_por_kg'].agg(lambda x: x.max() - x.min()).mean()
    
    tendencia, dif_pesos = 0, 0
    if len(fechas) > 1:
        p_actual = df_f[df_f['fecha_extraccion'] == fechas[0]]['precio_por_kg'].mean()
        p_prev = df_f[df_f['fecha_extraccion'] == fechas[1]]['precio_por_kg'].mean()
        if p_prev > 0:
            tendencia = (p_actual - p_prev) / p_prev
            dif_pesos = p_actual - p_prev

    p_volumen = 0
    p_chicas = df_f[df_f['peso_kg'] <= 3]['precio_por_kg'].mean()
    p_grandes = df_f[df_f['peso_kg'] >= 15]['precio_por_kg'].mean()
    if p_chicas > 0 and p_grandes > 0: p_volumen = (p_chicas - p_grandes) / p_chicas

    # --- CREACIÓN DE PESTAÑAS (TABS) ---
    tab_dashboard, tab_vitrina, tab_tecnica = st.tabs([
        "📈 Resumen del mercado", 
        "🛒 Vitrina de ofertas", 
        "🛠️ ¿Cómo se hizo esto?"
    ])

    # ==========================================
    # PESTAÑA 1: DASHBOARD
    # ==========================================
    with tab_dashboard:
        df_bar_data = df_f.groupby('plataforma')['precio_por_kg'].mean().sort_values().reset_index()
        if not df_bar_data.empty and len(df_bar_data) >= 2:
            t_min, p_min = df_bar_data.iloc[0]['plataforma'], df_bar_data.iloc[0]['precio_por_kg']
            t_max, p_max = df_bar_data.iloc[-1]['plataforma'], df_bar_data.iloc[-1]['precio_por_kg']
            ahorro = (p_max - p_min) / p_max
            st.info(f"💡 **El resumen de hoy:** Actualmente, la tienda más barata en promedio es **{t_min}**. Comprar acá en lugar de *{t_max}* te puede ahorrar hasta un **{ahorro:.1%}**. Además, si comprás bolsas grandes (más de 15kg), te ahorrás un **{p_volumen:.1%}** extra frente a las bolsas chicas.")

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Diferencia de Precios", f"${brecha_marca:,.0f}", help="Es la diferencia promedio en pesos que hay entre la tienda más cara y la más barata para un mismo alimento.")
        k2.metric("Precio Promedio (Kg)", f"${avg_total:,.0f}", help="El precio promedio por kilo de todo lo que estás viendo en pantalla.")
        k3.metric("Variación vs Ayer", f"${abs(dif_pesos):,.0f}", delta=f"{tendencia:+.2%}", delta_color="inverse", help="Muestra si los precios subieron o bajaron comparado con nuestra última revisión.")
        k4.metric("Ahorro por Bolsa Grande", f"{p_volumen:.1%}", help="El porcentaje de plata que te ahorrás por kilo al comprar bolsas de más de 15kg en lugar de bolsas pequeñas.")
        k5.metric("Ahorro Máximo Posible", f"{abs(ahorro):.1%}" if 'ahorro' in locals() else "0%", help="La diferencia de precio entre la opción más barata y la más cara del mercado.")

        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            with st.container(border=True):
                st.markdown("**💰 Precio Promedio por Tienda**")
                n = len(df_bar_data)
                colores = ['#22c55e'] + ['#3b82f6'] * (n - 2) + ['#ef4444'] if n > 2 else ['#22c55e', '#ef4444']
                df_bar_data['texto'] = df_bar_data['precio_por_kg'].apply(lambda x: f"${x:,.0f}")
                fig1 = px.bar(df_bar_data, x="plataforma", y="precio_por_kg", text="texto")
                fig1.update_traces(marker_color=colores, textposition='inside')
                fig1.update_layout(height=300, showlegend=False, xaxis_title=None, yaxis_title=None, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig1, use_container_width=True)

        with g2:
            with st.container(border=True):
                st.markdown("**📈 Evolución de precios (Por calidad)**")
                df_line = df_f.groupby(['fecha_extraccion', 'gama'])['precio_por_kg'].mean().reset_index()
                fig2 = px.line(df_line, x="fecha_extraccion", y="precio_por_kg", color="gama", markers=True)
                fig2.update_layout(height=300, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=None), margin=dict(l=0,r=0,t=0,b=0), xaxis_title=None, yaxis_title=None, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                fig2.update_xaxes(tickformat="%d %b")
                st.plotly_chart(fig2, use_container_width=True)

        df_f['max_fecha_tienda'] = df_f.groupby('plataforma')['fecha_extraccion'].transform('max')
        df_hoy = df_f[df_f['fecha_extraccion'] == df_f['max_fecha_tienda']].copy()
        st.markdown("### 🎯 Comparador: Tamaño de Bolsa vs Precio")
        with st.container(border=True):
            fig_s = px.scatter(df_hoy, x="peso_kg", y="precio_por_kg", color="gama", hover_name="titulo_original", hover_data={"gama":False, "precio_total":False, "marca":True, "plataforma":True, "precio_por_kg":":.0f"}, opacity=0.8, color_discrete_sequence=["#3b82f6", "#22c55e", "#f59e0b", "#ef4444"])
            fig_s.update_layout(height=400, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None), margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_s, use_container_width=True)

    # ==========================================
    # PESTAÑA 2: VITRINA
    # ==========================================
    with tab_vitrina:
        st.subheader("🛒 Encontrá el mejor precio para tu mascota")
        busqueda = st.text_input(
            "Buscá tu alimento (Ej: Adulto Pequeña Salmón...)", 
            placeholder="Escribí acá las palabras clave..."
        )
        
        if len(fechas) > 0:
            df_vitrina = df_f[df_f['fecha_extraccion'] == fechas[0]].copy()
            
            if busqueda:
                for palabra in busqueda.strip().split():
                    df_vitrina = df_vitrina[df_vitrina['titulo_original'].str.contains(palabra, case=False, na=False)]
            
            if busqueda:
                df_top = df_vitrina.sort_values('precio_por_kg', ascending=True).head(24)
            else:
                df_top = df_vitrina.sort_values('precio_por_kg').groupby('marca').head(2).head(20)
            
            if df_top.empty:
                st.info("No encontramos ningún alimento que coincida con esa búsqueda. ¡Probá con otras palabras!")
            else:
                cols = st.columns(4)
                for i, row in df_top.reset_index().iterrows():
                    with cols[i % 4]:
                        with st.container(border=True):
                            img = row.get('imagen_url') if pd.notna(row.get('imagen_url')) else 'https://via.placeholder.com/150'
                            st.markdown(f"""
                                <div style="background-color: white; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: center; height: 160px; padding: 10px;">
                                    <img src="{img}" style="max-height: 100%; object-fit: contain;">
                                </div>
                                <p title='{row['titulo_original']}' style='font-weight: 600; line-height: 1.2; height: 40px; overflow: hidden;'>{str(row['titulo_original'])[:45]}...</p>
                                <div style="margin-bottom: 10px;">
                                    <span style="color: #94a3b8; font-size: 0.8rem;">Total:</span> <strong style="font-size: 1.2rem; color: #3b82f6;">${row['precio_total']:,.0f}</strong><br>
                                    <span style="color: #94a3b8; font-size: 0.8rem;">Por Kg:</span> <strong>${row['precio_por_kg']:,.0f}</strong>
                                </div>
                                <div style="display: flex; gap: 5px; margin-bottom: 10px; flex-wrap: wrap;">
                                    <span style="background-color: rgba(148,163,184,0.1); border: 1px solid rgba(148,163,184,0.2); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">🏪 {row['plataforma']}</span>
                                    <span style="background-color: rgba(148,163,184,0.1); border: 1px solid rgba(148,163,184,0.2); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">⚖️ {row['peso_kg']}kg</span>
                                </div>
                            """, unsafe_allow_html=True)
                            st.link_button("Ir a la tienda", row.get('url_publicacion', '#'), type="primary", use_container_width=True)

    # ==========================================
    # PESTAÑA 3: ARQUITECTURA
    # ==========================================
    with tab_tecnica:
        st.markdown("### 🛠️ ¿Cómo funciona esta página por detrás?")
        st.markdown("""
        Detrás de esta pantalla hay un motor de datos (Data Pipeline) trabajando todos los días para traerte esta información de forma automática:
        
        * **1. Recolección automática:** Un programa (scraper) visita diariamente las webs de las tiendas de mascotas más grandes y anota todos sus precios y ofertas.
        * **2. Limpieza Inteligente:** Un algoritmo revisa los títulos de cada alimento, arregla los errores que cometen los vendedores, calcula el precio exacto por kilo y separa automáticamente si es alimento para perro o para gato.
        * **3. Almacenamiento:** Todos esos datos limpios se guardan de forma segura en una base de datos en la nube (PostgreSQL).
        * **4. Este tablero:** Finalmente, esta web lee esos datos y arma los gráficos para que cualquier persona pueda entender fácilmente dónde le conviene comprar.
        """)
        
        st.divider()
        st.markdown("#### 📥 Llevate los datos")
        st.markdown("Si querés ver el detalle o hacer tus propios cálculos en Excel, podés descargar toda la tabla de precios limpios haciendo clic en el botón de abajo.")
        
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar listado de precios (CSV)",
            data=csv,
            file_name='precios_mascotas.csv',
            mime='text/csv',
            type="primary"
        )

    # --- FOOTER PROFESIONAL ---
    st.markdown("""
        <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--secondary-background-color); color: #94a3b8; font-size: 0.85rem;">
            Pet Intelligence Dashboard v1.0 &copy; 2026<br>
            Hecho para ayudar a los dueños de mascotas a cuidar su bolsillo con el poder de los datos.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
