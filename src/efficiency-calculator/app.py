# app.py
import streamlit as st

st.set_page_config(
    page_title="Wind Turbine Return Calculator",
    page_icon="🌀",
    layout="centered",
)

# ----------------------------
# Fluent-light, flat, industrial styling
# Palette (from your image):
#  #37514E #6B9294 #B7CBCD #C14A11 #D9DBD9 #929292
# ----------------------------
st.markdown(
    """
<style>
:root{
  --p1: #37514E; /* deep teal */
  --p2: #6B9294; /* mid teal */
  --p3: #B7CBCD; /* light teal */
  --p4: #C14A11; /* oxide accent */
  --p5: #D9DBD9; /* off-white */
  --p6: #929292; /* neutral */

  /* Fluent-like roles */
  --bg: #ffffff;
  --surface: #ffffff;
  --surface2: #f7f8f8;
  --text: #0f1414;
  --muted: #5f6a6a;

  --border: rgba(55,81,78,0.16);     /* derived from p1 */
  --border2: rgba(55,81,78,0.10);
  --hairline: rgba(146,146,146,0.28);

  --accent: var(--p4);              /* oxide */
  --accent2: rgba(193,74,17,0.10);  /* accent tint */

  --radius: 16px;
  --radius2: 14px;

  --shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* App background */
html, body, [data-testid="stAppViewContainer"]{
  background: var(--bg) !important;
  color: var(--text) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"]{ background: transparent !important; }
.block-container{ padding-top: 1.7rem; padding-bottom: 2.2rem; max-width: 920px; }

/* Title bar (flat, fluent) */
.titlebar{
  display:flex; align-items:center; justify-content:space-between;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
}
.titlebar h1{
  margin:0;
  font-size: 1.05rem;
  letter-spacing: 0.12em;
  font-weight: 750;
  text-transform: uppercase;
  color: var(--p1);
}
.badge{
  padding: 6px 10px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface2);
  color: var(--muted);
  font-size: 0.78rem;
}

/* Section headings */
.section-title{
  margin-top: 18px;
  font-size: 2.2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text);
}
.section-sub{
  margin-top: 6px;
  color: var(--muted);
  font-size: 0.98rem;
}

/* Panels are flat "cards" */
.panel{
  margin-top: 14px;
  padding: 16px;
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
}

/* Hairline divider (very subtle) */
.divider{
  height: 1px;
  width: 100%;
  background: var(--hairline);
  margin: 18px 0;
}

/* Inputs: fluent-ish */
label{
  color: var(--muted) !important;
  font-size: 0.90rem !important;
}
div[data-baseweb="input"]{
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius2) !important;
}
div[data-baseweb="input"]:focus-within{
  border-color: rgba(193,74,17,0.55) !important;
  box-shadow: 0 0 0 2px rgba(193,74,17,0.12) !important; /* subtle focus ring */
}

/* Remove +/- steppers from number inputs */
div[data-testid="stNumberInput"] button{ display:none !important; }
div[data-baseweb="input"] button{ display:none !important; }

/* Primary action button: START / GO */
.stButton > button{
  width:100%;
  border-radius: var(--radius2);
  border: 1px solid rgba(107,146,148,0.65); /* #6B9294 */
  background: #6B9294;
  color: #ffffff;
  padding: 0.72rem 1rem;
  font-weight: 750;
}
.stButton > button:hover{
  background: #5f8587;
}
.stButton > button:active{
  background: #54797b;
}

/* Metrics: flat cards, no gradients */
div[data-testid="stMetric"]{
  background: var(--surface);
  border: 1px solid var(--border2);
  padding: 14px 14px;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
div[data-testid="stMetric"] label{
  color: var(--muted) !important;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.72rem !important;
}
div[data-testid="stMetric"] div{
  color: var(--text) !important;
}

/* Empty state */
.empty{
  padding: 12px 14px;
  border: 1px dashed rgba(55,81,78,0.22);
  border-radius: var(--radius);
  background: var(--surface2);
  color: var(--muted);
}

/* Minor text */
.stCaption, small{ color: var(--muted) !important; }

/* Reduce Streamlit default spacers slightly */
div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMetric"]){
  margin-top: 0.2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Header
# ----------------------------
st.markdown(
    """
<div class="titlebar">
  <h1>Wind Turbine Return Calculator</h1>
  <div class="badge">Industrial • Fluent • Light</div>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Fake compute (swap for your real pipeline)
# ----------------------------
def run_calculation(lat: float, lon: float):
    return {
        "energy_kwh": 17_431_012.99,
        "avg_power_w": 1_989_841.67,
        "min_wind": 0.30,
        "max_wind": 10.98,
        "avg_wind": 3.7521917808219176,
        "height_m": 2.0,
        "days": 365,
    }

if "result" not in st.session_state:
    st.session_state.result = None

# ----------------------------
# Inputs
# ----------------------------
st.markdown('<div class="section-title">Site Coordinates</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Enter latitude and longitude, then run the calculation.</div>', unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=50.4501, format="%.6f")
with c2:
    lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=30.5234, format="%.6f")

run = st.button("Run calculation", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ----------------------------
# Report
# ----------------------------
st.markdown('<div class="section-title">Report</div>', unsafe_allow_html=True)

if run:
    st.session_state.result = run_calculation(lat, lon)

res = st.session_state.result
st.markdown('<div class="panel">', unsafe_allow_html=True)

if not res:
    st.markdown(
        """
        <div class="empty">
          Run a calculation to see energy, power, and wind statistics for the selected location.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Primary KPIs
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Energy production", f"{res['energy_kwh']:,.2f} kWh")
    with m2:
        st.metric("Average power", f"{res['avg_power_w']:,.2f} W")

    st.markdown('<div class="divider" style="margin:14px 0;"></div>', unsafe_allow_html=True)

    # Secondary KPIs
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Min wind speed", f"{res['min_wind']:.2f} m/s")
    with s2:
        st.metric("Avg wind speed", f"{res['avg_wind']:.2f} m/s")
    with s3:
        st.metric("Max wind speed", f"{res['max_wind']:.2f} m/s")

    st.markdown('<div class="divider" style="margin:14px 0;"></div>', unsafe_allow_html=True)

    # Details (compact)
    d1, d2, d3 = st.columns(3)
    with d1:
        st.caption("Reference height")
        st.write(f"**{res['height_m']:.1f} m**")
    with d2:
        st.caption("Time window")
        st.write(f"**{int(res['days'])} days**")
    with d3:
        st.caption("Location")
        st.write(f"**{lat:.4f}, {lon:.4f}**")

st.markdown("</div>", unsafe_allow_html=True)
