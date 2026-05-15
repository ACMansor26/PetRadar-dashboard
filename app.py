import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- CONFIGURACIÓN Y ESTILO ---
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

    /* Chips del stack tecnológico */
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

    /* Botón CTA de contacto en sidebar */
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

    /* Cards de impacto en el hero */
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

    /* Badge verde en hero */
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
    # SIDEBAR PROFESIONAL
    # ============================================================
    with st.sidebar:
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

        st.markdown("""
            <a href="https://www.linkedin.com/in/amir-mansor25/" target="_blank" class="cta-contacto">
                📩 Contactarme
            </a>
        """, unsafe_allow_html=True)

        st.divider()
        st.caption("Pipeline ELT activo · Datos actualizados diariamente desde PostgreSQL en la nube.")

    # ============================================================
    # HERO CON IMPACT NUMBERS
    # ============================================================
    n_retailers  = df['plataforma'].nunique()
    n_marcas     = df['marca'].nunique()
    n_dias       = (df['fecha_extraccion'].max() - df['fecha_extraccion'].min()).days
    n_productos  = df['titulo_original'].nunique()

    col_hero, col_filtros = st.columns([2, 1])

    with col_hero:
        st.markdown('<span class="hero-badge">✅ Pipeline en producción</span>', unsafe_allow_html=True)
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
    if mascota != "Ambas":         df_f = df_f[df_f['categoria'] == mascota]
    if marcas_seleccionadas:       df_f = df_f[df_f['marca'].isin(marcas_seleccionadas)]
    if gama != "Todas":            df_f = df_f[df_f['gama'] == gama]
    if tienda != "Todas":          df_f = df_f[df_f['plataforma'] == tienda]

    # ============================================================
    # CÁLCULOS GLOBALES
    # ============================================================
    fechas      = sorted(df_f['fecha_extraccion'].unique(), reverse=True)
    avg_total   = df_f['precio_por_kg'].mean()
    brecha_marca = df_f.groupby('marca')['precio_por_kg'].agg(lambda x: x.max() - x.min()).mean()

    # Inflación acumulada y variación de 7 días (reemplaza variación diaria)
    pet_flacion  = 0
    dias_periodo = 0
    var_7d       = 0          # NUEVO: promedio de variación diaria en últimos 7 días
    dif_pesos    = 0
    p_actual     = 0

    if len(fechas) > 1:
        p_actual = df_f[df_f['fecha_extraccion'] == fechas[0]]['precio_por_kg'].mean()
        fecha_reciente = fechas[0]
        fecha_antigua  = fechas[-1]
        p_base = df_f[df_f['fecha_extraccion'] == fecha_antigua]['precio_por_kg'].mean()
        if p_base > 0:
            pet_flacion  = (p_actual - p_base) / p_base
        dias_periodo = (fecha_reciente - fecha_antigua).days

        # Variación promedio de los últimos 7 días (más estable que variación diaria)
        fechas_7d = fechas[:min(8, len(fechas))]
        df_7d = df_f[df_f['fecha_extraccion'].isin(fechas_7d)].groupby('fecha_extraccion')['precio_por_kg'].mean().sort_index()
        if len(df_7d) >= 2:
            variaciones_diarias = df_7d.pct_change().dropna()
            var_7d = variaciones_diarias.mean()
            dif_pesos = df_7d.iloc[-1] - df_7d.iloc[0]

    # Sobreprecio por fraccionamiento
    p_volumen = 0
    p_chicas  = df_f[df_f['peso_kg'] <= 3]['precio_por_kg'].mean()
    p_grandes = df_f[df_f['peso_kg'] >= 15]['precio_por_kg'].mean()
    if p_chicas > 0 and p_grandes > 0:
        p_volumen = (p_chicas - p_grandes) / p_chicas

    # NUEVO KPI: Tienda oficial vs terceros
    precio_oficial  = None
    precio_terceros = None
    diff_oficial    = None
    if 'es_tienda_oficial' in df_f.columns:
        grp = df_f.groupby('es_tienda_oficial')['precio_por_kg'].mean()
        precio_oficial  = grp.get(True,  grp.get(1,  None))
        precio_terceros = grp.get(False, grp.get(0,  None))
        if precio_oficial and precio_terceros and precio_terceros > 0:
            diff_oficial = (precio_oficial - precio_terceros) / precio_terceros

    # NUEVO KPI: Vendedores únicos
    n_vendedores = df_f['vendedor'].nunique() if 'vendedor' in df_f.columns else 0

    # Bar chart base para insight
    df_bar_data = df_f.groupby('plataforma')['precio_por_kg'].mean().sort_values().reset_index()

    # ============================================================
    # TABS
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

        # Insight orientado a la acción
        if not df_bar_data.empty and len(df_bar_data) >= 2:
            t_min = df_bar_data.iloc[0]['plataforma']
            t_max = df_bar_data.iloc[-1]['plataforma']
            ahorro_pct = (df_bar_data.iloc[-1]['precio_por_kg'] - df_bar_data.iloc[0]['precio_por_kg']) / df_bar_data.iloc[-1]['precio_por_kg']
            st.success(
                f"💰 **Oportunidad detectada:** Comprando en **{t_min}** en lugar de {t_max} podés ahorrar hasta un "
                f"**{ahorro_pct:.1%} por kilo**, compensando la inflación del período ({pet_flacion:+.1%} en {dias_periodo} días). "
                f"Filtrá por marca para ver el impacto exacto en tu categoría."
            )

        # --- FILA 1 DE KPIs ---
        k1, k2, k3 = st.columns(3)
        k1.metric(
            "Precio promedio por kg",
            f"${avg_total:,.0f}",
            help="Costo promedio por kilogramo."
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

        # --- FILA 2 DE KPIs ---
        k4, k5, k6 = st.columns(3)
        k4.metric(
            f"Inflación acumulada ({dias_periodo} días)",
            f"{pet_flacion:+.1%}",
            delta=f"{pet_flacion:+.2%}",
            delta_color="inverse",
            help="Variación de precios desde el inicio del período hasta hoy."
        )
        # MODIFICADO: variación promedio 7 días en lugar de variación diaria (más estable)
        k5.metric(
            "Tendencia (últimos 7 días)",
            f"{var_7d:+.2%}",
            delta="por día en promedio",
            delta_color="inverse",
            help="Variación diaria promedio de los últimos 7 días."
        )
        k6.metric(
            "Ahorro máximo posible hoy",
            f"{((df_bar_data.iloc[-1]['precio_por_kg'] - df_bar_data.iloc[0]['precio_por_kg']) / df_bar_data.iloc[-1]['precio_por_kg']):.1%}" if not df_bar_data.empty and len(df_bar_data) >= 2 else "0%",
            help="Porcentaje de ahorro eligiendo el retailer más barato vs el más caro hoy."
        )

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

        # --- FILA 3 DE KPIs (NUEVOS) ---
        k7, k8, k9 = st.columns(3)

        # NUEVO: Vendedores únicos monitoreados
        k7.metric(
            "Vendedores monitoreados",
            f"{n_vendedores}",
            help="Total de vendedores únicos detectados en el dataset filtrado."
        )

        # NUEVO: Precio oficial vs terceros
        if diff_oficial is not None:
            label_diff = "más caro que terceros" if diff_oficial > 0 else "más barato que terceros"
            k8.metric(
                "Tienda oficial vs terceros",
                f"{abs(diff_oficial):.1%}",
                delta=label_diff,
                delta_color="inverse" if diff_oficial > 0 else "normal",
                help=f"Precio promedio oficial: ${precio_oficial:,.0f}/kg · Terceros: ${precio_terceros:,.0f}/kg"
            )
        else:
            k8.metric("Tienda oficial vs terceros", "Sin datos", help="No hay datos de es_tienda_oficial en el filtro actual.")

        # Precio medio tienda más barata (dato contextual)
        if not df_bar_data.empty:
            k9.metric(
                f"Mejor precio hoy ({df_bar_data.iloc[0]['plataforma']})",
                f"${df_bar_data.iloc[0]['precio_por_kg']:,.0f}/kg",
                help=f"Retailer con el precio por kg más bajo en el snapshot de hoy."
            )

        st.divider()

        # --- GRÁFICOS FILA 1 ---
        g1, g2 = st.columns(2)

        with g1:
            with st.container(border=True):
                st.markdown("**Precio promedio por tienda**")
                st.caption("Verde = más barato · Rojo = más caro en el snapshot de hoy.")
                n = len(df_bar_data)
                colores = ['#22c55e'] + ['#3b82f6'] * (n - 2) + ['#ef4444'] if n > 2 else ['#22c55e', '#ef4444']
                df_bar_data['texto'] = df_bar_data['precio_por_kg'].apply(lambda x: f"${x:,.0f}")
                fig1 = px.bar(df_bar_data, x="plataforma", y="precio_por_kg", text="texto")
                fig1.update_traces(marker_color=colores, textposition='inside')
                fig1.update_layout(
                    height=280, showlegend=False, xaxis_title=None, yaxis_title=None,
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig1, use_container_width=True)

        with g2:
            with st.container(border=True):
                st.markdown("**Evolución de precios por segmento de calidad**")
                st.caption("Escala lineal. Las diferencias entre segmentos reflejan el precio real de mercado.")
                df_line = df_f.groupby(['fecha_extraccion', 'gama'])['precio_por_kg'].mean().reset_index()
                fig2 = px.line(df_line, x="fecha_extraccion", y="precio_por_kg", color="gama", markers=True)
                fig2.update_layout(
                    height=280,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=None),
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title=None, yaxis_title=None,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                )
                fig2.update_xaxes(tickformat="%d %b")
                fig2.update_yaxes(tickprefix="$")
                st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # --- GRÁFICOS FILA 2 (NUEVOS) ---
        g3, g4 = st.columns(2)

        # NUEVO: Box plot — dispersión de precios por marca
        with g3:
            with st.container(border=True):
                st.markdown("**Variabilidad de precio por marca**")
                st.caption("Cada caja muestra cuánto varía el precio de una marca entre retailers. Cajas anchas = más diferencia entre canales.")
                # Filtramos las marcas con más registros para no saturar el gráfico
                top_marcas = df_f['marca'].value_counts().head(10).index
                df_box = df_f[df_f['marca'].isin(top_marcas)]
                fig_box = px.box(
                    df_box,
                    x="marca",
                    y="precio_por_kg",
                    color="marca",
                    labels={"marca": "Marca", "precio_por_kg": "Precio por kg ($)"},
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_box.update_layout(
                    height=350,
                    showlegend=False,
                    xaxis_title=None, yaxis_title=None,
                    xaxis_tickangle=-30,
                    margin=dict(l=0, r=0, t=10, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                )
                fig_box.update_yaxes(tickprefix="$")
                st.plotly_chart(fig_box, use_container_width=True)

        # NUEVO: Heatmap marca × plataforma
        with g4:
            with st.container(border=True):
                st.markdown("**¿En qué tienda comprar cada marca?**")
                st.caption("Verde = precio más bajo. Rojo = precio más alto. Leé por fila para elegir el mejor canal por marca.")
                top_marcas_hm = df_f['marca'].value_counts().head(12).index
                df_hm = df_f[df_f['marca'].isin(top_marcas_hm)]
                pivot = df_hm.groupby(['marca', 'plataforma'])['precio_por_kg'].mean().reset_index()
                pivot_table = pivot.pivot(index='marca', columns='plataforma', values='precio_por_kg')
                fig_hm = px.imshow(
                    pivot_table,
                    color_continuous_scale="RdYlGn_r",
                    text_auto=".0f",
                    labels=dict(x="Tienda", y="Marca", color="$/kg"),
                    aspect="auto"
                )
                fig_hm.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=10, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    coloraxis_showscale=False
                )
                fig_hm.update_traces(textfont_size=11)
                st.plotly_chart(fig_hm, use_container_width=True)

        st.divider()

        # --- SCATTER CON TRENDLINE ---
        st.markdown("### Eficiencia de precio según tamaño de bolsa")
        st.caption("Los puntos más bajos en el eje Y son el mejor costo por kilo. La línea de tendencia muestra si comprar en volumen realmente conviene.")
        with st.container(border=True):
            df_scatter = df_f[df_f['fecha_extraccion'] == fechas[0]].copy()
            # MODIFICADO: agregada trendline OLS para mostrar correlación precio/kg vs tamaño
            fig_scatter = px.scatter(
                df_scatter,
                x="peso_kg",
                y="precio_por_kg",
                color="gama",
                size="precio_total",
                hover_name="titulo_original",
                trendline="lowess",
                trendline_scope="overall",
                trendline_color_override="#94a3b8",
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
    # PESTAÑA 2: OFERTAS DEL DÍA
    # ==========================================
    with tab_vitrina:
        st.subheader("🛒 Ofertas reales de hoy")
        st.caption("Productos cuyo precio actual está por debajo de su promedio histórico. La insignia 🔥 indica una oferta verificada por el pipeline.")

        # --- CONTROLES DE LA VITRINA ---
        ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([2, 1, 1, 1])
        with ctrl1:
            busqueda = st.text_input("Buscar", placeholder="Ej: Pro Plan Adulto, Royal Canin...", label_visibility="collapsed")
        with ctrl2:
            orden = st.selectbox("Ordenar por", [
                "Mayor descuento",
                "Menor precio/kg",
                "Menor precio total",
            ], label_visibility="collapsed")
        with ctrl3:
            umbral_pct = st.slider("Descuento mínimo", min_value=0, max_value=30, value=0, step=5, format="%d%%")
        with ctrl4:
            solo_oficial = st.toggle("Solo tienda oficial", value=False)

        if len(fechas) > 0:
            # --- DEAL SCORE ---
            hist_avg = df_f.groupby("titulo_original")["precio_por_kg"].mean().reset_index()
            hist_avg.rename(columns={"precio_por_kg": "precio_hist_promedio"}, inplace=True)

            df_vitrina = df_f[df_f["fecha_extraccion"] == fechas[0]].copy()
            df_vitrina = pd.merge(df_vitrina, hist_avg, on="titulo_original", how="left")
            df_vitrina["descuento_vs_hist"] = (
                (df_vitrina["precio_hist_promedio"] - df_vitrina["precio_por_kg"])
                / df_vitrina["precio_hist_promedio"]
            ).fillna(0)

            # --- APLICAR FILTROS ---
            if busqueda:
                for palabra in busqueda.strip().split():
                    df_vitrina = df_vitrina[df_vitrina["titulo_original"].str.contains(palabra, case=False, na=False)]

            if umbral_pct > 0:
                df_vitrina = df_vitrina[df_vitrina["descuento_vs_hist"] >= umbral_pct / 100]

            if solo_oficial and "es_tienda_oficial" in df_vitrina.columns:
                df_vitrina = df_vitrina[df_vitrina["es_tienda_oficial"].isin([True, 1])]

            # --- ORDEN ---
            orden_map = {
                "Mayor descuento":    ("descuento_vs_hist", False),
                "Menor precio/kg":    ("precio_por_kg",     True),
                "Menor precio total": ("precio_total",       True),
            }
            col_orden, asc_orden = orden_map[orden]
            df_vitrina = df_vitrina.sort_values(col_orden, ascending=asc_orden)

            if not busqueda and umbral_pct == 0:
                df_top = df_vitrina.groupby("marca").head(2).head(24)
            else:
                df_top = df_vitrina.head(24)

            # --- CONTADOR ---
            n_ofertas  = int((df_vitrina["descuento_vs_hist"] >= 0.05).sum())
            total_snap = len(df_vitrina)
            st.markdown(
                f"<div style='font-size:0.82rem;color:#94a3b8;margin:8px 0 12px;'>"
                f"Mostrando <strong style='color:var(--text-color)'>{len(df_top)}</strong> de "
                f"<strong style='color:var(--text-color)'>{total_snap}</strong> productos · "
                f"<span style='color:#ef4444;font-weight:600;'>🔥 {n_ofertas} ofertas reales detectadas</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            if df_top.empty:
                st.info("No se encontraron productos con esos filtros en el snapshot actual.")
            else:
                cols = st.columns(4)
                for i, row in df_top.reset_index(drop=True).iterrows():
                    es_oferta   = row.get("descuento_vs_hist", 0) >= 0.05
                    es_oficial  = row.get("es_tienda_oficial", False) in [True, 1]
                    dcto        = row.get("descuento_vs_hist", 0) * 100
                    hist_precio = row.get("precio_hist_promedio", None)
                    vendedor_v  = row.get("vendedor", "")
                    vendedor_nom = str(vendedor_v)[:22] if pd.notna(vendedor_v) and str(vendedor_v).strip() else ""
                    img_url     = row.get("imagen_url") if pd.notna(row.get("imagen_url")) else "https://via.placeholder.com/150"
                    titulo_safe = str(row["titulo_original"]).replace("'", "")

                    # Estilos condicionales
                    card_border  = "border:1.5px solid rgba(239,68,68,0.45);box-shadow:0 0 12px rgba(239,68,68,0.12);" if es_oferta else ""

                    oferta_badge = ""
                    if es_oferta:
                        oferta_badge = (
                            f'<div style="position:absolute;bottom:8px;left:8px;background:#ef4444;'
                            f'color:white;padding:3px 8px;border-radius:4px;font-size:0.68rem;'
                            f'font-weight:700;box-shadow:0 2px 5px rgba(0,0,0,0.25);">'
                            f'🔥 -{dcto:.0f}% vs hist.</div>'
                        )

                    oficial_badge = ""
                    if es_oficial:
                        oficial_badge = (
                            '<span style="background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.3);'
                            'color:#16a34a;padding:2px 6px;border-radius:4px;font-size:0.68rem;font-weight:600;">'
                            '✓ Oficial</span>'
                        )

                    hist_html = ""
                    if es_oferta and hist_precio and not pd.isna(hist_precio):
                        hist_html = f'<span style="color:#94a3b8;font-size:0.75rem;text-decoration:line-through;">${hist_precio:,.0f}/kg</span> '

                    vendedor_html = ""
                    if vendedor_nom:
                        vendedor_html = f'<div style="font-size:0.7rem;color:#94a3b8;margin-bottom:6px;">Vendedor: {vendedor_nom}</div>'

                    with cols[i % 4]:
                        with st.container(border=True):
                            # Franja superior de color para ofertas reales
                            if es_oferta:
                                st.markdown(
                                    f'<div style="margin:-12px -12px 10px -12px;height:4px;'
                                    f'background:linear-gradient(90deg,#ef4444,#f97316);border-radius:8px 8px 0 0;"></div>',
                                    unsafe_allow_html=True
                                )
                            # Imagen
                            st.markdown(
                                f'<div style="background:rgba(128,128,128,0.08);border-radius:8px;margin-bottom:10px;' +
                                f'display:flex;justify-content:center;align-items:center;' +
                                f'height:155px;padding:10px;position:relative;">' +
                                f'<img src="{img_url}" style="max-height:100%;max-width:100%;object-fit:contain;">' +
                                oferta_badge +
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            # Contenido con padding horizontal
                            st.markdown(
                                f'<div style="padding:0 4px;">' +
                                f'<p style="font-weight:600;font-size:0.82rem;line-height:1.3;' +
                                f'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;' +
                                f'overflow:hidden;margin-bottom:8px;min-height:2.6em;" title="{titulo_safe}">' +
                                f'{row["titulo_original"]}</p>' +
                                f'<div style="margin-bottom:8px;">' +
                                f'<div style="margin-bottom:2px;">' +
                                hist_html +
                                f'<strong style="font-size:1.15rem;color:#3b82f6;">${row["precio_por_kg"]:,.0f}' +
                                f'<span style="font-size:0.75rem;font-weight:400;color:#94a3b8;">/kg</span></strong></div>' +
                                f'<div style="color:#94a3b8;font-size:0.78rem;">Total: ' +
                                f'<strong style="color:var(--text-color);">${row["precio_total"]:,.0f}</strong></div></div>' +
                                f'<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px;align-items:center;">' +
                                f'<span style="background:rgba(148,163,184,0.1);border:1px solid rgba(148,163,184,0.2);' +
                                f'padding:2px 6px;border-radius:4px;font-size:0.68rem;">🏢 {row["plataforma"]}</span>' +
                                f'<span style="background:rgba(148,163,184,0.1);border:1px solid rgba(148,163,184,0.2);' +
                                f'padding:2px 6px;border-radius:4px;font-size:0.68rem;">⚖️ {row["peso_kg"]}kg</span>' +
                                oficial_badge +
                                f'</div>' +
                                vendedor_html +
                                f'</div>',
                                unsafe_allow_html=True
                            )
                            btn_label = f"🔥 Ver oferta (−{dcto:.0f}%)" if es_oferta else "Ver publicación"
                            st.link_button(btn_label, row.get("url", "#"), type="primary", use_container_width=True)
    # ==========================================
    # PESTAÑA 3: CÓMO FUNCIONA
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
                interactivas en tiempo real. El foco está en minimizar el time-to-insight
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
            PetLytics v4.0 &copy; 2026 · Amir Mansor · Analytics Engineer<br>
            Pipeline ELT en producción · Datos actualizados diariamente
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
