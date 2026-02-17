import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(page_title="Fixed Income CFA", layout="wide")

# ===============================
# TABS
# ===============================
tab1, tab2 = st.tabs([
    "🧠 Simulador Buy Side",
    "📘 Theory"
])

# ==========================================================
# ======================= TAB 1 =============================
# ==========================================================
with tab1:

    st.title("📊 Fixed Income Core Trainer — Buy Side Style")
    st.caption("Datos pequeños, lógica grande. El reto es saber QUÉ fórmula usar.")

    # ---------- SEMILLA (solo al refresh) ----------
    if "seed" not in st.session_state:
        st.session_state.seed = np.random.randint(0, 10000)

    np.random.seed(st.session_state.seed)

    # ===============================
    # DATOS BASE
    # ===============================
    face = 100
    coupon = np.random.randint(3, 7)
    spot_rates = np.array([
        np.random.randint(2, 5) / 100,
        np.random.randint(3, 6) / 100,
        np.random.randint(4, 7) / 100
    ])
    
    cash_flows = np.array([coupon, coupon, coupon + face])
    
    answers = {}
    
    # ===============================
    # 1️⃣ BOND PRICING WITH SPOT RATES
    # ===============================
    st.header("1️⃣ Bond Pricing with Spot Rates (DCF real)")
    
    price_spot = sum(
        cash_flows[t] / (1 + spot_rates[t]) ** (t + 1)
        for t in range(3)
    )
    
    st.write("**Datos:**")
    st.write("Cash Flows:", cash_flows)
    st.write("Spot Rates:", spot_rates)
    st.write(f"📌 **Precio del bono:** `{price_spot:.2f}`")
    
    answers[1] = st.radio(
        "¿Qué metodología es correcta para valorizar este bono?",
        [
            "Usar un único YTM para todos los flujos",
            "Descontar cada flujo con su spot rate correspondiente",
            "Ignorar la estructura temporal"
        ],
        key="q1"
    )
    
    # ===============================
    # 2️⃣ Z-SPREAD
    # ===============================
    st.header("2️⃣ Z-Spread")
    
    market_price = price_spot - np.random.randint(1, 4)
    
    def price_z(z):
        return sum(
            cash_flows[t] / (1 + spot_rates[t] + z) ** (t + 1)
            for t in range(3)
        )
    
    z_grid = np.linspace(0, 0.03, 200)
    prices = [price_z(z) for z in z_grid]
    z_spread = z_grid[np.argmin(np.abs(np.array(prices) - market_price))]
    
    st.write(f"Precio de mercado observado: `{market_price:.2f}`")
    st.write(f"📌 **Z-Spread aproximado:** `{z_spread*10000:.0f} bps`")
    
    answers[2] = st.radio(
        "¿Qué representa el Z-spread?",
        [
            "Un spread distinto para cada flujo",
            "Un spread constante sobre toda la curva spot",
            "Un spread ajustado por opciones"
        ],
        key="q2"
    )
    
    # ===============================
    # 3️⃣ PRICE–YIELD RELATIONSHIP 📊
    # ===============================
    st.header("3️⃣ Price–Yield Relationship")
    
    yields = np.linspace(0.01, 0.10, 50)
    prices_py = [
        sum(cash_flows[t] / (1 + y) ** (t + 1) for t in range(3))
        for y in yields
    ]
    
    fig, ax = plt.subplots()
    ax.plot(yields * 100, prices_py)
    ax.set_xlabel("Yield (%)")
    ax.set_ylabel("Precio")
    ax.set_title("Relación inversa Precio–Yield")
    ax.grid()
    st.pyplot(fig)
    
    answers[3] = st.radio(
        "Si el yield sube, ¿qué ocurre con el precio?",
        [
            "Sube",
            "Baja",
            "Permanece constante"
        ],
        key="q3"
    )
    
    # ===============================
    # 4️⃣ MODIFIED vs EFFECTIVE DURATION 📊
    # ===============================
    st.header("4️⃣ Modified vs Effective Duration")
    
    y0 = 0.05
    dy = 0.01
    
    p0 = sum(cash_flows[t] / (1 + y0) ** (t + 1) for t in range(3))
    p_up = sum(cash_flows[t] / (1 + y0 + dy) ** (t + 1) for t in range(3))
    p_down = sum(cash_flows[t] / (1 + y0 - dy) ** (t + 1) for t in range(3))
    
    mod_dur = (p_down - p_up) / (2 * p0 * dy)
    
    st.write(f"📌 **Modified Duration:** `{mod_dur:.2f}`")
    
    fig, ax = plt.subplots()
    ax.plot(yields * 100, prices_py)
    ax.scatter([y0 * 100], [p0])
    ax.set_title("Aproximación lineal vs curva real")
    st.pyplot(fig)
    
    answers[4] = st.radio(
        "¿Qué duración usarías para un bono con opción call?",
        [
            "Macaulay Duration",
            "Modified Duration",
            "Effective Duration"
        ],
        key="q4"
    )
    
    # ===============================
    # 5️⃣ CONVEXITY 📊
    # ===============================
    st.header("5️⃣ Convexity")
    
    convexity = (p_up + p_down - 2 * p0) / (p0 * dy ** 2)
    
    st.write(f"📌 **Convexity:** `{convexity:.2f}`")
    st.write("Caídas de yield generan mayor ganancia que pérdidas simétricas.")
    
    answers[5] = st.radio(
        "La convexidad positiva implica que:",
        [
            "Las pérdidas por subidas de tasas son mayores",
            "Las ganancias por caídas de tasas son mayores",
            "El precio cambia linealmente"
        ],
        key="q5"
    )
    
    # ===============================
    # 6️⃣ OPTION-EMBEDDED BOND 📊
    # ===============================
    st.header("6️⃣ Option-Embedded Bond (Callable)")
    
    call_price = np.random.randint(101, 104)
    callable_prices = [min(p, call_price) for p in prices_py]
    
    fig, ax = plt.subplots()
    ax.plot(yields * 100, prices_py, label="Sin opción")
    ax.plot(yields * 100, callable_prices, label="Callable")
    ax.legend()
    ax.set_title("Precio capado por opción call")
    st.pyplot(fig)
    
    answers[6] = st.radio(
        "¿Por qué el Z-spread es engañoso aquí?",
        [
            "Porque ignora la curva",
            "Porque no ajusta por el valor de la opción",
            "Porque depende del cupón"
        ],
        key="q6"
    )
    
    # ===============================
    # 7️⃣ COUPON EFFECT 📊
    # ===============================
    st.header("7️⃣ Coupon Effect")
    
    low_coupon = [2, 2, 102]
    high_coupon = [8, 8, 108]
    
    def bond_price(cf, y):
        return sum(cf[t] / (1 + y) ** (t + 1) for t in range(len(cf)))
    
    prices_low = [bond_price(low_coupon, y) for y in yields]
    prices_high = [bond_price(high_coupon, y) for y in yields]
    
    fig, ax = plt.subplots()
    ax.plot(yields * 100, prices_low, label="Low Coupon")
    ax.plot(yields * 100, prices_high, label="High Coupon")
    ax.legend()
    ax.set_title("Sensibilidad distinta por cupón")
    st.pyplot(fig)
    
    answers[7] = st.radio(
        "¿Qué bono es más sensible a cambios en tasas?",
        [
            "Mayor cupón",
            "Menor cupón",
            "Ambos igual"
        ],
        key="q7"
    )
    
    # ===============================
    # 8️⃣ MATURITY EFFECT 📊
    # ===============================
    st.header("8️⃣ Maturity Effect")
    
    short_cf = [5, 105]
    long_cf = [5] * 9 + [105]
    
    prices_short = [bond_price(short_cf, y) for y in yields]
    prices_long = [bond_price(long_cf, y) for y in yields]
    
    fig, ax = plt.subplots()
    ax.plot(yields * 100, prices_short, label="2Y Bond")
    ax.plot(yields * 100, prices_long, label="10Y Bond")
    ax.legend()
    ax.set_title("Efecto madurez en sensibilidad")
    st.pyplot(fig)
    
    answers[8] = st.radio(
        "¿Qué bono es más sensible a tasas?",
        [
            "Menor madurez",
            "Mayor madurez",
            "Ambos igual"
        ],
        key="q8"
    )
    
    # ===============================
    # 9️⃣ CURVE DURATION 📊
    # ===============================
    st.header("9️⃣ Curve Duration")
    
    parallel = spot_rates + 0.01
    steepener = spot_rates + np.array([0.02, 0.01, 0.00])
    
    price_parallel = sum(
        cash_flows[t] / (1 + parallel[t]) ** (t + 1)
        for t in range(3)
    )
    
    price_steep = sum(
        cash_flows[t] / (1 + steepener[t]) ** (t + 1)
        for t in range(3)
    )
    
    st.write(f"Precio con shift paralelo: `{price_parallel:.2f}`")
    st.write(f"Precio con steepener: `{price_steep:.2f}`")
    
    answers[9] = st.radio(
        "¿Qué captura la curve duration?",
        [
            "Solo cambios paralelos",
            "Cambios no paralelos",
            "Solo el YTM"
        ],
        key="q9"
    )
    
    # ===============================
    # FINALIZAR
    # ===============================
    if st.button("✅ Finalizar"):
        correct = {
            1: "Descontar cada flujo con su spot rate correspondiente",
            2: "Un spread constante sobre toda la curva spot",
            3: "Baja",
            4: "Effective Duration",
            5: "Las ganancias por caídas de tasas son mayores",
            6: "Porque no ajusta por el valor de la opción",
            7: "Menor cupón",
            8: "Mayor madurez",
            9: "Cambios no paralelos"
        }
    
        score = sum(answers[i] == correct[i] for i in correct)
    
        st.subheader("📈 Resultado Final")
        st.write(f"**Score:** {score} / 9")
    
        if score >= 8:
            st.success("Nivel Buy Side sólido.")
        elif score >= 6:
            st.warning("Buen nivel, aún con brechas.")
        else:
            st.error("Reforzar core de renta fija.")


# ==========================================================
# ======================= TAB 2 =============================
# ==========================================================
with tab2:

    st.title("📊 Fixed Income – Core CFA Topics (Buy Side Research)")
    st.caption("Organizador gráfico conceptual | Enfoque CFA Level I–II")

    topics = [
        {
            "title": "Bond pricing con spot rates y YTM",
            "what": "Spot rates descuentan cada flujo con su tasa específica. YTM es una tasa única que iguala el valor presente de todos los flujos al precio del bono.",
            "understand": "Los spot rates reflejan correctamente la estructura temporal de tasas. El YTM es un promedio implícito y no una tasa de descuento real para cada flujo.",
            "limit": "El YTM asume reinversión a la misma tasa y no captura cambios en la forma de la curva."
        },
        {
            "title": "Relación precio–yield",
            "what": "Existe una relación inversa entre el precio del bono y su yield.",
            "understand": "La relación es no lineal; caídas de tasas aumentan el precio más que lo que lo reducen subidas equivalentes.",
            "limit": "La aproximación lineal solo es válida para cambios pequeños en el yield."
        },
        {
            "title": "Bonos bullet, cupón fijo y FRN",
            "what": "Bonos bullet pagan principal al vencimiento; cupones fijos pagan flujos constantes; FRN ajustan su cupón a una tasa de referencia.",
            "understand": "Los FRN tienen baja duración; los bonos fijos concentran riesgo de tasa.",
            "limit": "Los FRN no eliminan riesgo de spread ni riesgo de crédito."
        },
        {
            "title": "G-spread e I-spread",
            "what": "G-spread mide el diferencial frente a bonos gobierno; I-spread frente a tasas swap.",
            "understand": "Sirven para comparación rápida entre instrumentos.",
            "limit": "No consideran la forma completa de la curva de rendimientos."
        },
        {
            "title": "Z-spread",
            "what": "Spread constante que se suma a cada spot rate para igualar el precio del bono.",
            "understand": "Permite aislar mejor el riesgo de crédito y liquidez.",
            "limit": "No es adecuado para bonos con opciones embebidas."
        },
        {
            "title": "OAS (Option-Adjusted Spread)",
            "what": "Z-spread ajustado por el valor de la opción embebida.",
            "understand": "Permite comparar bonos con y sin opciones bajo un mismo marco.",
            "limit": "Depende del modelo de tasas y supuestos de volatilidad."
        },
        {
            "title": "Duración (Macaulay y Modified)",
            "what": "Macaulay mide el tiempo promedio de recuperación del capital; Modified mide sensibilidad del precio al yield.",
            "understand": "Es la medida base del riesgo de tasa de interés.",
            "limit": "Asume cambios paralelos en la curva y falla con opciones."
        },
        {
            "title": "Effective Duration",
            "what": "Duración calculada revalorizando el bono ante cambios en la curva.",
            "understand": "Captura efectos no lineales y es clave para bonos con opciones.",
            "limit": "Depende fuertemente de los supuestos del modelo."
        },
        {
            "title": "Convexidad",
            "what": "Mide la curvatura de la relación precio–yield.",
            "understand": "Corrige el error de la duración y mejora la estimación de cambios de precio.",
            "limit": "Puede ser negativa en bonos callable."
        },
        {
            "title": "Shifts de curva",
            "what": "Movimientos paralelos o no paralelos en la curva de tasas.",
            "understand": "La mayoría de movimientos reales no son paralelos.",
            "limit": "La duración tradicional no captura bien estos efectos."
        },
        {
            "title": "DCF aplicado a bonos",
            "what": "Valor presente de flujos contractuales descontados a tasas apropiadas.",
            "understand": "El riesgo proviene de la tasa y del spread, no del flujo.",
            "limit": "Altamente sensible a la estimación del spread."
        },
        {
            "title": "Relación descuento–spread–riesgo",
            "what": "Mayor riesgo implica mayor spread, mayor tasa y menor precio.",
            "understand": "Los spreads explican gran parte del movimiento de precios en crédito.",
            "limit": "El spread mezcla crédito, liquidez y factores técnicos."
        },
        {
            "title": "Componentes del yield corporativo",
            "what": "El yield incluye tasa real, inflación, prima por plazo, liquidez y crédito.",
            "understand": "Permite explicar diferencias de rendimiento entre emisores.",
            "limit": "Los componentes no son directamente observables."
        },
        {
            "title": "Four C’s of Credit",
            "what": "Capacidad, colateral, covenants y carácter del emisor.",
            "understand": "Framework cualitativo para análisis rápido de crédito.",
            "limit": "No genera métricas cuantitativas directas."
        },
        {
            "title": "Bloomberg – funciones clave",
            "what": "Herramientas para análisis de bonos, spreads, portafolios y alternativas.",
            "understand": "Facilitan análisis, comparación y automatización.",
            "limit": "Los resultados dependen de supuestos y calidad del input."
        }
    ]

    for topic in topics:
        st.subheader(f"📌 {topic['title']}")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Qué es**")
            st.write(topic["what"])

        with col2:
            st.markdown("**Qué debes entender**")
            st.write(topic["understand"])

        with col3:
            st.markdown("**Limitación (CFA)**")
            st.write(topic["limit"])

        st.divider()
