import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Energy Production Dashboard",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #1f2937;
    padding: 16px;
    border-radius: 14px;
}

h1, h2, h3 {
    letter-spacing: 0.3px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATA
# ---------------------------------------------------
records = [
    # Ελλάδα
    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-20", "energy": 510, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-20", "energy": 390, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-20", "energy": 305, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-20", "energy": 280, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-20", "energy": 455, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-20", "energy": 470, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-21", "energy": 520, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-21", "energy": 405, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-21", "energy": 310, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-21", "energy": 285, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-21", "energy": 460, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-21", "energy": 475, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-22", "energy": 530, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-22", "energy": 395, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-22", "energy": 320, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-22", "energy": 295, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-22", "energy": 465, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-22", "energy": 485, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-23", "energy": 515, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-23", "energy": 400, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-23", "energy": 330, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-23", "energy": 300, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-23", "energy": 470, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-23", "energy": 490, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-24", "energy": 540, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-24", "energy": 410, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-24", "energy": 325, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-24", "energy": 305, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-24", "energy": 480, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-24", "energy": 500, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-25", "energy": 500, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-25", "energy": 380, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-25", "energy": 290, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-25", "energy": 270, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-25", "energy": 450, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-25", "energy": 495, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-26", "energy": 510, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-26", "energy": 400, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-26", "energy": 300, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-26", "energy": 275, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-26", "energy": 460, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-26", "energy": 505, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-27", "energy": 530, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-27", "energy": 405, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-27", "energy": 310, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-27", "energy": 285, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-27", "energy": 470, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-27", "energy": 515, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-28", "energy": 520, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-28", "energy": 410, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-28", "energy": 305, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-28", "energy": 280, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-28", "energy": 480, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-28", "energy": 520, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-29", "energy": 540, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-29", "energy": 390, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-29", "energy": 330, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-29", "energy": 295, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-29", "energy": 490, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-29", "energy": 530, "type": "Lignite"},

    {"plant": "Agios Dimitrios", "country": "GR", "date": "2026-03-30", "energy": 545, "type": "Lignite"},
    {"plant": "Megalopoli", "country": "GR", "date": "2026-03-30", "energy": 415, "type": "Lignite"},
    {"plant": "Lavrio", "country": "GR", "date": "2026-03-30", "energy": 335, "type": "Natural Gas"},
    {"plant": "Komotini", "country": "GR", "date": "2026-03-30", "energy": 305, "type": "Natural Gas"},
    {"plant": "Amyntaio", "country": "GR", "date": "2026-03-30", "energy": 495, "type": "Lignite"},
    {"plant": "Ptolemaida", "country": "GR", "date": "2026-03-30", "energy": 540, "type": "Lignite"},

    # Γειτονικές χώρες
    {"plant": "Sofia Plant", "country": "BG", "date": "2026-03-20", "energy": 420, "type": "Coal"},
    {"plant": "Skopje Plant", "country": "MK", "date": "2026-03-20", "energy": 240, "type": "Hydro"},
    {"plant": "Tirana Plant", "country": "AL", "date": "2026-03-20", "energy": 180, "type": "Hydro"},

    {"plant": "Sofia Plant", "country": "BG", "date": "2026-03-25", "energy": 430, "type": "Coal"},
    {"plant": "Skopje Plant", "country": "MK", "date": "2026-03-25", "energy": 250, "type": "Hydro"},
    {"plant": "Tirana Plant", "country": "AL", "date": "2026-03-25", "energy": 190, "type": "Hydro"},

    {"plant": "Sofia Plant", "country": "BG", "date": "2026-03-30", "energy": 440, "type": "Coal"},
    {"plant": "Skopje Plant", "country": "MK", "date": "2026-03-30", "energy": 270, "type": "Hydro"},
    {"plant": "Tirana Plant", "country": "AL", "date": "2026-03-30", "energy": 205, "type": "Hydro"},
]

df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date"])

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("⚡ Energy Production Dashboard")
st.markdown("### Interactive analysis of power plants, energy types and neighboring countries")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("Filters")

gr_plants = sorted(df[df["country"] == "GR"]["plant"].unique().tolist())
all_types = sorted(df["type"].unique().tolist())

selected_plants = st.sidebar.multiselect(
    "Select plants",
    options=gr_plants,
    default=gr_plants[:2]
)

date_range = st.sidebar.date_input(
    "Select date range",
    value=(df["date"].min().date(), df["date"].max().date()),
    min_value=df["date"].min().date(),
    max_value=df["date"].max().date()
)

selected_types = st.sidebar.multiselect(
    "Energy type",
    options=all_types,
    default=all_types
)

# ---------------------------------------------------
# INPUT SAFETY
# ---------------------------------------------------
if len(selected_plants) == 0:
    st.warning("Επίλεξε τουλάχιστον ένα εργοστάσιο από το sidebar.")
    st.stop()

if len(date_range) != 2:
    st.warning("Επίλεξε σωστό εύρος ημερομηνιών.")
    st.stop()

start_date, end_date = date_range

# ---------------------------------------------------
# FILTERED DATA
# ---------------------------------------------------
filtered = df[
    (df["plant"].isin(selected_plants)) &
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date) &
    (df["type"].isin(selected_types))
].copy()

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------
st.markdown("## Key Metrics")
c1, c2, c3, c4 = st.columns(4)

total_energy = int(filtered["energy"].sum()) if not filtered.empty else 0
avg_energy = round(filtered["energy"].mean(), 2) if not filtered.empty else 0
max_energy = int(filtered["energy"].max()) if not filtered.empty else 0
records_count = int(len(filtered))

c1.metric("Total Energy", f"{total_energy} MWh")
c2.metric("Average Energy", f"{avg_energy} MWh")
c3.metric("Max Energy", f"{max_energy} MWh")
c4.metric("Records", records_count)

# ---------------------------------------------------
# MAIN CHARTS
# ---------------------------------------------------
left, right = st.columns(2)

with left:
    st.markdown("## Energy Over Time")
    if filtered.empty:
        st.info("Δεν υπάρχουν δεδομένα για το συγκεκριμένο φίλτρο.")
    else:
        fig_line = px.line(
            filtered.sort_values("date"),
            x="date",
            y="energy",
            color="plant",
            markers=True,
            template="plotly_dark"
        )
        fig_line.update_layout(
            xaxis_title="Date",
            yaxis_title="Energy (MWh)",
            legend_title="Plant",
            height=430
        )
        st.plotly_chart(fig_line, use_container_width=True)

with right:
    st.markdown("## Energy Distribution by Type")
    if filtered.empty:
        st.info("Δεν υπάρχουν δεδομένα για κατανομή ενέργειας.")
    else:
        pie_data = filtered.groupby("type", as_index=False)["energy"].sum()
        fig_pie = px.pie(
            pie_data,
            values="energy",
            names="type",
            hole=0.45,
            template="plotly_dark"
        )
        fig_pie.update_layout(height=430)
        st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------
# COUNTRY COMPARISON
# ---------------------------------------------------
st.markdown("## Country Comparison")

comparison_countries = ["GR", "BG", "MK", "AL"]
comparison_df = df[
    (df["country"].isin(comparison_countries)) &
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date)
].copy()

country_totals = comparison_df.groupby("country", as_index=False)["energy"].sum()

if country_totals.empty:
    st.info("Δεν υπάρχουν δεδομένα για σύγκριση χωρών.")
else:
    fig_bar = px.bar(
        country_totals,
        x="country",
        y="energy",
        color="country",
        template="plotly_dark",
        text_auto=True
    )
    fig_bar.update_layout(
        xaxis_title="Country",
        yaxis_title="Total Energy (MWh)",
        height=420,
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------
# MAX / MIN TABLE
# ---------------------------------------------------
st.markdown("## Max / Min per Plant")

gr_only = df[df["country"] == "GR"].copy()

stats_df = (
    gr_only.groupby("plant")["energy"]
    .agg(max="max", min="min")
    .reset_index()
)

stats_df = stats_df.rename(columns={
    "plant": "Plant",
    "max": "Max Energy (MWh)",
    "min": "Min Energy (MWh)"
})

st.dataframe(stats_df, use_container_width=True)

# ---------------------------------------------------
# RAW DATA TABLE
# ---------------------------------------------------
st.markdown("## Filtered Data Table")
st.dataframe(filtered, use_container_width=True)

# ---------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------
csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered data as CSV",
    data=csv_data,
    file_name="filtered_energy_data.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Demo dashboard with sample data. Next step: integration with ENTSO-E API.")