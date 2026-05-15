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
        padding: 20px 20px 20px 24px;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-left: 4px solid #3b82f6;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(59, 130, 246, 0.02) 100%);
        box-shadow: 0 4px 12px -2px rgba(59, 130, 246, 0.12);
        height: 145px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 8px 20px -4px rgba(59, 130, 246, 0.2);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        color: var(--text-color) !important;
        opacity: 0.65;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        color: var(--text-color) !important;
        opacity: 1 !important;
    }

    /* Verde para bajas de precio */
    [data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaIcon-Down"] { color: #15803d !important; }
    [data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaIcon-Down"] + div { color: #15803d !important; font-weight: 700 !important; }

    /* VITRINA: hover en cards */
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

    /* MEJORA 4: Chips del stack tecnológico */
    .tech-chip {
        display: inline-block;
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.25);
        color: #3b82f6;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 0.72rem;
        font-weight: 600;
        margin: 2px 2px;
    }

    /* MEJORA 1: Botón CTA de contacto en sidebar */
    .cta-contacto {
        display: block;
        width: 100%;
        background-color: #3b82f6;
        color: #ffffff !important;
        text-align: center;
        padding: 10px 0;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        margin-top: 8px;
        transition: background-color 0.2s ease;
    }
    .cta-contacto:hover { background-color: #2563eb; }

    /* MEJORA 2: Cards de impacto en el hero */
    .impact-grid {
        display: flex;
        gap: 12px;
        margin-top: 12px;
    }
    .impact-card {
        flex: 1;
        background-color: rgba(59, 130, 246, 0.06);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
    }
    .impact-num {
        font-size: 1.5rem;
        font-weight: 700;
        color: #3b82f6;
        display: block;
    }
    .impact-label {
        font-size: 0.72rem;
        color: #94a3b8;
        margin-top: 2px;
        display: block;
    }

    /* MEJORA 5: Badge de stack en hero */
    .hero-badge {
        display: inline-block;
        background-color: #dcfce7;
        color: #15803d;
        border-radius: 6px;
        padding: 5px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=600)
def cargar_datos_neon():
    try:
        DATABASE_URL = "postgresql://neondb_owner:npg_dZ6hozpYA0ut@ep-little-flower-acv5xn2k.sa-east-1.aws.neon.tech/neondb?sslmode=require"
        engine = create_engine(DATABASE_URL)
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
    if df.empty:
        return

    # ============================================================
    # MEJORA 1: SIDEBAR PROFESIONAL CON CTA Y STACK TECNOLÓGICO
    # ============================================================
    with st.sidebar:
        # Avatar con iniciales + nombre + rol
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
                <div style="width: 52px; height: 52px; border-radius: 50%; background: rgba(59,130,246,0.12);
                            border: 2px solid #3b82f6; display: flex; align-items: center; justify-content: center;
                            font-size: 1.1rem; font-weight: 700; color: #3b82f6; flex-shrink: 0;">
                    AM
                </div>
                <div>
                    <div style="font-weight: 700; font-size: 1rem;">Amir Mansor</div>
                    <div style="background: rgba(59,130,246,0.1); color: #3b82f6; border-radius: 4px;
                                padding: 2px 8px; font-size: 0.72rem; font-weight: 600; display: inline-block; margin-top: 3px;">
                        Analytics Engineer
                    </div>
                </div>
            </div>
            <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5; margin-top: 8px;">
                Especializado en pipelines ELT, pricing analytics y visualización de datos accionable para negocio.
            </p>
        """, unsafe_allow_html=True)

        st.divider()

        # MEJORA 4: Stack tecnológico visible con chips
        st.markdown("**Stack tecnológico**")
        st.markdown("""
            <div style="margin-top: 4px;">
                <span class="tech-chip">Python</span>
                <span class="tech-chip">PostgreSQL</span>
                <span class="tech-chip">Streamlit</span>
                <span class="tech-chip">Pandas</span>
                <span class="tech-chip">SQLAlchemy</span>
                <span class="tech-chip">Plotly</span>
                <span class="tech-chip">Neon DB</span>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("**Conectemos**")
        st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/amir-mansor25/)")
        st.markdown("🐙 [GitHub](https://github.com/ACMansor26)")

        # MEJORA 1: CTA de contacto prominente
        st.markdown("""
            <a href="https://www.linkedin.com/in/amir-mansor25/" target="_blank" class="cta-contacto">
                📩 Contactarme
            </a>
        """, unsafe_allow_html=True)

        st.divider()
        st.caption("Pipeline ELT activo · Datos actualizados diariamente desde PostgreSQL en la nube.")

    # ============================================================
    # MEJORA 2: HERO CON PROPUESTA DE VALOR E IMPACT NUMBERS
    # ============================================================
    n_retailers = df['plataforma'].nunique()
    n_marcas = df['marca'].nunique()
    n_dias = (df['fecha_extraccion'].max() - df['fecha_extraccion'].min()).days
    n_productos = df['titulo_original'].nunique()

    col_hero, col_filtros = st.columns([2, 1])

    with col_hero:

        st.title("PetLytics — Inteligencia de Precios")
        st.markdown("##### Detectá ofertas reales, monitoreá la inflación por segmento y tomá decisiones de compra basadas en datos.")

        st.markdown(f"""
            <div class="impact-grid">
                <div class="impact-card">
                    <span class="impact-num">{n_retailers}</span>
                    <span class="impact-label">retailers monitoreados</span>
                </div>
                <div class="impact-card">
                    <span class="impact-num">{n_marcas}</span>
                    <span class="impact-label">marcas relevadas</span>
                </div>
                <div class="impact-card">
                    <span class="impact-num">{n_dias}d</span>
                    <span class="impact-label">historial activo</span>
                </div>
                <div class="impact-card">
                    <span class="impact-num">{n_productos}</span>
                    <span class="impact-label">productos relevados</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_filtros:
        with st.container(border=True):
            f1, f2 = st.columns(2)
            with f1:
                mascota = st.selectbox("Mascota", ["Ambas"] + sorted(list(df['categoria'].unique())))
                marcas_seleccionadas = st.multiselect("Marca", options=sorted(list(df['marca'].unique())), placeholder="Todas")
            with f2:
                gama = st.selectbox("Calidad", ["Todas"] + sorted(list(df['gama'].unique())))
                tienda = st.selectbox("Tienda", ["Todas"] + sorted(list(df['plataforma'].unique())))

    # Filtrado dinámico
    df_f = df.copy()
    if mascota != "Ambas":
        df_f = df_f[df_f['categoria'] == mascota]
    if marcas_seleccionadas:
        df_f = df_f[df_f['marca'].isin(marcas_seleccionadas)]
    if gama != "Todas":
        df_f = df_f[df_f['gama'] == gama]
    if tienda != "Todas":
        df_f = df_f[df_f['plataforma'] == tienda]

    # Cálculos globales
    fechas = sorted(df_f['fecha_extraccion'].unique(), reverse=True)
    avg_total = df_f['precio_por_kg'].mean()
    brecha_marca = df_f.groupby('marca')['precio_por_kg'].agg(lambda x: x.max() - x.min()).mean()

    pet_flacion = 0
    dias_periodo = 0
    tendencia = 0
    dif_pesos = 0
    p_actual = 0
    if len(fechas) > 1:
        p_actual = df_f[df_f['fecha_extraccion'] == fechas[0]]['precio_por_kg'].mean()
        p_prev = df_f[df_f['fecha_extraccion'] == fechas[1]]['precio_por_kg'].mean()
        if p_prev > 0:
            tendencia = (p_actual - p_prev) / p_prev
            dif_pesos = p_actual - p_prev
        fecha_reciente = fechas[0]
        fecha_antigua = fechas[-1]
        p_base = df_f[df_f['fecha_extraccion'] == fecha_antigua]['precio_por_kg'].mean()
        if p_base > 0:
            pet_flacion = (p_actual - p_base) / p_base
        dias_periodo = (fecha_reciente - fecha_antigua).days

    p_volumen = 0
    p_chicas = df_f[df_f['peso_kg'] <= 3]['precio_por_kg'].mean()
    p_grandes = df_f[df_f['peso_kg'] >= 15]['precio_por_kg'].mean()
    if p_chicas > 0 and p_grandes > 0:
        p_volumen = (p_chicas - p_grandes) / p_chicas

    # ============================================================
    # MEJORA 5: TABS CON NOMBRES ACCESIBLES PARA TODO PERFIL
    # ============================================================
    tab_dashboard, tab_vitrina, tab_tecnica = st.tabs([
        "📈 Dashboard",
        "🛒 Ofertas del día",
        "⚙️ Cómo funciona"
    ])

    # ==========================================
    # PESTAÑA 1: DASHBOARD
    # ==========================================
    with tab_dashboard:
        df_bar_data = df_f.groupby('plataforma')['precio_por_kg'].mean().sort_values().reset_index()

        # MEJORA 5: Insight orientado a la acción concreta
        if not df_bar_data.empty and len(df_bar_data) >= 2:
            t_min = df_bar_data.iloc[0]['plataforma']
            t_max = df_bar_data.iloc[-1]['plataforma']
            ahorro_pct = (df_bar_data.iloc[-1]['precio_por_kg'] - df_bar_data.iloc[0]['precio_por_kg']) / df_bar_data.iloc[-1]['precio_por_kg']
            st.success(
                f"💰 **Oportunidad detectada:** Comprando en **{t_min}** en lugar de {t_max} podés ahorrar hasta un "
                f"**{ahorro_pct:.1%} por kilo**, compensando la inflación del período ({pet_flacion:+.1%} en {dias_periodo} días). "
                f"Filtrá por marca para ver el impacto exacto en tu categoría."
            )

        # MEJORA 3: KPIs con nombres de negocio claros
        k1, k2, k3 = st.columns(3)
        k1.metric(
            "Precio promedio por kg",
            f"${avg_total:,.0f}",
            help="Costo promedio por kilogramo sobre el set de datos actual."
        )
        k2.metric(
            "Brecha entre retailers",
            f"${brecha_marca:,.0f}",
            help="Diferencia entre el canal más caro y el más barato para un mismo producto."
        )
        k3.metric(
            "Sobreprecio por formato chico",
            f"{p_volumen:.1%}",
            help="Cuánto más pagás comprando bolsas ≤3 kg vs bolsas ≥15 kg."
        )

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

        k4, k5, k6 = st.columns(3)
        k4.metric(
            f"Inflación acumulada ({dias_periodo} días)",
            f"{pet_flacion:+.1%}",
            delta=f"{pet_flacion:+.2%}",
            delta_color="inverse",
            help=f"Variación de precios desde el inicio del período hasta hoy."
        )
        k5.metric(
            "Variación diaria de precio",
            f"${abs(dif_pesos):,.0f}",
            delta=f"{tendencia:+.2%}",
            delta_color="inverse",
            help="Ajuste de precio detectado en la última corrida del pipeline."
        )
        k6.metric(
            "Ahorro máximo posible hoy",
            f"{((df_bar_data.iloc[-1]['precio_por_kg'] - df_bar_data.iloc[0]['precio_por_kg']) / df_bar_data.iloc[-1]['precio_por_kg']):.1%}" if not df_bar_data.empty and len(df_bar_data) >= 2 else "0%",
            help="Porcentaje de ahorro posible eligiendo el retailer más barato vs el más caro hoy."
        )

        st.divider()

        g1, g2 = st.columns(2)
        with g1:
            with st.container(border=True):
                st.markdown("**Precio promedio por tienda**")
                n = len(df_bar_data)
                colores = ['#22c55e'] + ['#3b82f6'] * (n - 2) + ['#ef4444'] if n > 2 else ['#22c55e', '#ef4444']
                df_bar_data['texto'] = df_bar_data['precio_por_kg'].apply(lambda x: f"${x:,.0f}")
                fig1 = px.bar(df_bar_data, x="plataforma", y="precio_por_kg", text="texto")
                fig1.update_traces(marker_color=colores, textposition='inside')
                fig1.update_layout(
                    height=300, showlegend=False, xaxis_title=None, yaxis_title=None,
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig1, use_container_width=True)

        with g2:
            with st.container(border=True):
                st.markdown("**Evolución de precios por segmento de calidad**")
                df_line = df_f.groupby(['fecha_extraccion', 'gama'])['precio_por_kg'].mean().reset_index()
                fig2 = px.line(df_line, x="fecha_extraccion", y="precio_por_kg", color="gama", markers=True, log_y=True)
                fig2.update_layout(
                    height=300,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=None),
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title=None, yaxis_title=None,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                )
                fig2.update_xaxes(tickformat="%d %b")
                fig2.update_yaxes(tickprefix="$")
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Eficiencia de precio según tamaño de bolsa")
        st.caption("Los puntos más bajos en el eje Y representan el mejor costo por kilo. Buscalos para maximizar tu ahorro.")
        with st.container(border=True):
            df_scatter = df_f[df_f['fecha_extraccion'] == fechas[0]].copy()
            fig_scatter = px.scatter(
                df_scatter,
                x="peso_kg",
                y="precio_por_kg",
                color="gama",
                size="precio_total",
                hover_name="titulo_original",
                labels={
                    "peso_kg": "Tamaño de bolsa (kg)",
                    "precio_por_kg": "Costo por kg ($)",
                    "gama": "Segmento"
                },
                template="plotly_white",
                color_discrete_sequence=["#3b82f6", "#22c55e", "#f59e0b", "#ef4444"]
            )
            fig_scatter.update_layout(
                height=450,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # ==========================================
    # PESTAÑA 2: OFERTAS DEL DÍA (antes Vitrina)
    # ==========================================
    with tab_vitrina:
        st.subheader("🛒 Ofertas reales de hoy")
        st.caption("Productos cuyo precio actual está por debajo de su promedio histórico. La insignia 🔥 indica una oferta verificada por el pipeline.")
        busqueda = st.text_input("Buscador de productos (ej: Pro Plan Adulto)", placeholder="Escribí una marca o producto...")

        if len(fechas) > 0:
            hist_avg = df_f.groupby('titulo_original')['precio_por_kg'].mean().reset_index()
            hist_avg.rename(columns={'precio_por_kg': 'precio_hist_promedio'}, inplace=True)

            df_vitrina = df_f[df_f['fecha_extraccion'] == fechas[0]].copy()
            df_vitrina = pd.merge(df_vitrina, hist_avg, on='titulo_original', how='left')
            df_vitrina['descuento_vs_hist'] = (df_vitrina['precio_hist_promedio'] - df_vitrina['precio_por_kg']) / df_vitrina['precio_hist_promedio']

            if busqueda:
                for palabra in busqueda.strip().split():
                    df_vitrina = df_vitrina[df_vitrina['titulo_original'].str.contains(palabra, case=False, na=False)]
                df_top = df_vitrina.sort_values('precio_por_kg', ascending=True).head(24)
            else:
                df_top = df_vitrina.sort_values('precio_por_kg').groupby('marca').head(2).head(20)

            if df_top.empty:
                st.info("No se encontraron productos con esos filtros en el snapshot actual.")
            else:
                cols = st.columns(4)
                for i, row in df_top.reset_index().iterrows():
                    with cols[i % 4]:
                        with st.container(border=True):
                            img = row.get('imagen_url') if pd.notna(row.get('imagen_url')) else 'https://via.placeholder.com/150'
                            oferta_badge = ""
                            if row.get('descuento_vs_hist', 0) >= 0.05:
                                dcto = row['descuento_vs_hist'] * 100
                                oferta_badge = f"""<div style="position: absolute; bottom: 8px; left: 8px; background-color: #ef4444; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">🔥 OFERTA REAL (-{dcto:.0f}%)</div>"""

                            st.markdown(f"""
                                <div style="background-color: white; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: center; height: 160px; padding: 10px; position: relative;">
                                    <img src="{img}" style="max-height: 100%; object-fit: contain;">
                                    {oferta_badge}
                                </div>
                                <p title='{row['titulo_original']}' style='font-weight: 600; line-height: 1.2; height: 40px; overflow: hidden; margin-bottom: 5px;'>{str(row['titulo_original'])[:40]}...</p>
                                <div style="margin-bottom: 10px;">
                                    <span style="color: #94a3b8; font-size: 0.8rem;">Precio total:</span> <strong style="font-size: 1.2rem; color: #3b82f6;">${row['precio_total']:,.0f}</strong><br>
                                    <span style="color: #94a3b8; font-size: 0.8rem;">Costo/kg:</span> <strong>${row['precio_por_kg']:,.0f}</strong>
                                </div>
                                <div style="display: flex; gap: 5px; margin-bottom: 10px; flex-wrap: wrap;">
                                    <span style="background-color: rgba(148,163,184,0.1); border: 1px solid rgba(148,163,184,0.2); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">🏢 {row['plataforma']}</span>
                                    <span style="background-color: rgba(148,163,184,0.1); border: 1px solid rgba(148,163,184,0.2); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">⚖️ {row['peso_kg']}kg</span>
                                </div>
                            """, unsafe_allow_html=True)
                            st.link_button("Ver publicación", row.get('url', '#'), type="primary", use_container_width=True)

    # ==========================================
    # PESTAÑA 3: CÓMO FUNCIONA (antes Arquitectura ELT)
    # ==========================================
    with tab_tecnica:
        st.markdown("### ⚙️ ¿Cómo se construyó PetLytics?")
        st.markdown("""
        PetLytics es un proyecto de **Analytics Engineering end-to-end**: desde la extracción de datos crudos hasta la visualización de KPIs de negocio.
        Cada capa del pipeline está pensada para escalar y para entregar valor real al usuario final.
        """)

        col_a, col_b = st.columns(2)

        with col_a:
            with st.container(border=True):
                st.markdown("**1. Extracción (Ingesta)**")
                st.markdown("""
                Recolección automatizada de precios desde los principales retailers de mascotas.
                El scraper resuelve barreras de seguridad (TLS/Cloudflare) para garantizar
                un flujo de datos estable y diario.
                """)
                st.caption("Stack: Python · Requests · BeautifulSoup")

            with st.container(border=True):
                st.markdown("**2. Transformación (ELT & Calidad)**")
                st.markdown("""
                Lógica vectorizada en Pandas para unificar monedas, normalizar pesos y
                calcular métricas derivadas como el precio por kg y el Deal Score
                (oferta real vs. promedio histórico).
                """)
                st.caption("Stack: Python · Pandas · SQLAlchemy")

        with col_b:
            with st.container(border=True):
                st.markdown("**3. Almacenamiento (Cloud Storage)**")
                st.markdown("""
                Modelo relacional cargado en PostgreSQL serverless en la nube (Neon DB).
                Los datos persisten entre corridas y el historial acumulado alimenta
                los promedios móviles del Deal Score.
                """)
                st.caption("Stack: PostgreSQL · Neon DB (serverless)")

            with st.container(border=True):
                st.markdown("**4. Presentación (Semántica de negocio)**")
                st.markdown("""
                Traducción de datos limpios a KPIs financieros auditables y visualizaciones
                interactivas en tiempo real. El foco está en minimizar el *time-to-insight*
                para cualquier perfil de usuario.
                """)
                st.caption("Stack: Streamlit · Plotly · Python")

        st.divider()
        st.markdown("#### 📥 Exportar datos filtrados")
        st.caption("Descargá el modelo analítico con los filtros aplicados para análisis externo.")
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar datos filtrados (CSV)",
            data=csv,
            file_name='petlytics_modelo_analitico.csv',
            mime='text/csv',
            type="primary"
        )

    # --- FOOTER ---
    st.markdown("""
        <div style="text-align: center; margin-top: 50px; padding-top: 20px;
                    border-top: 1px solid var(--secondary-background-color);
                    color: #94a3b8; font-size: 0.85rem;">
            PetLytics v3.0 &copy; 2026 · Amir Mansor · Analytics Engineer<br>
            Pipeline ELT en producción · Datos actualizados diariamente
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
