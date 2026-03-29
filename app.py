import streamlit as st
import pandas as pd
import plotly.express as px
import random

# ---------------------------------------------------
# ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ
# ---------------------------------------------------
st.set_page_config(
    page_title="Σύστημα Παρακολούθησης Ενέργειας",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------
# ΣΤΥΛ
# ---------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-size: 1.08rem;
    color: #cbd5e1;
    margin-bottom: 1rem;
}

.section-box {
    background: linear-gradient(135deg, rgba(30,41,59,0.96), rgba(15,23,42,0.96));
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,0.14);
    box-shadow: 0 8px 24px rgba(0,0,0,0.20);
    margin-bottom: 18px;
}

.insight-box {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-left: 5px solid #38bdf8;
    padding: 16px;
    border-radius: 14px;
    margin-top: 8px;
    margin-bottom: 16px;
    color: #e2e8f0;
    font-size: 1rem;
}

.compare-box {
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 1px solid rgba(148,163,184,0.14);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 14px;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 1px solid rgba(148,163,184,0.14);
    padding: 16px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# ΔΗΜΙΟΥΡΓΙΑ ΔΕΔΟΜΕΝΩΝ
# ---------------------------------------------------
random.seed(42)

greek_plants_info = {
    "Άγιος Δημήτριος": {"country": "Ελλάδα", "type": "Λιγνίτης", "base": 520},
    "Μεγαλόπολη": {"country": "Ελλάδα", "type": "Λιγνίτης", "base": 400},
    "Λαύριο": {"country": "Ελλάδα", "type": "Φυσικό Αέριο", "base": 320},
    "Κομοτηνή": {"country": "Ελλάδα", "type": "Φυσικό Αέριο", "base": 290},
    "Αμύνταιο": {"country": "Ελλάδα", "type": "Λιγνίτης", "base": 470},
    "Πτολεμαΐδα": {"country": "Ελλάδα", "type": "Λιγνίτης", "base": 510},
}

other_countries_info = {
    "Σόφια": {"country": "Βουλγαρία", "type": "Άνθρακας", "base": 430},
    "Σκόπια": {"country": "Βόρεια Μακεδονία", "type": "Υδροηλεκτρική", "base": 255},
    "Τίρανα": {"country": "Αλβανία", "type": "Υδροηλεκτρική", "base": 195},
    "Κωνσταντινούπολη": {"country": "Τουρκία", "type": "Φυσικό Αέριο", "base": 620},
    "Ρώμη": {"country": "Ιταλία", "type": "Φυσικό Αέριο", "base": 590},
    "Λευκωσία": {"country": "Κύπρος", "type": "Φυσικό Αέριο", "base": 220},
}

all_plants_info = {}
all_plants_info.update(greek_plants_info)
all_plants_info.update(other_countries_info)

dates = pd.date_range(start="2026-01-01", end="2026-12-31", freq="D")

records = []

for date in dates:
    month_factor = 1 + ((date.month - 6) / 50)
    weekday_factor = 1.05 if date.weekday() < 5 else 0.95

    for plant, info in all_plants_info.items():
        random_noise = random.randint(-25, 25)
        energy = int(info["base"] * month_factor * weekday_factor + random_noise)

        if energy < 50:
            energy = 50

        records.append({
            "plant": plant,
            "country": info["country"],
            "date": date,
            "energy": energy,
            "type": info["type"]
        })

df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date"])

# Ελληνικές χρονικές στήλες
days_map = {
    0: "Δευτέρα",
    1: "Τρίτη",
    2: "Τετάρτη",
    3: "Πέμπτη",
    4: "Παρασκευή",
    5: "Σάββατο",
    6: "Κυριακή"
}

months_map = {
    1: "Ιανουάριος",
    2: "Φεβρουάριος",
    3: "Μάρτιος",
    4: "Απρίλιος",
    5: "Μάιος",
    6: "Ιούνιος",
    7: "Ιούλιος",
    8: "Αύγουστος",
    9: "Σεπτέμβριος",
    10: "Οκτώβριος",
    11: "Νοέμβριος",
    12: "Δεκέμβριος"
}

df["Ημέρα Εβδομάδας"] = df["date"].dt.weekday.map(days_map)
df["Αριθμός Εβδομάδας"] = df["date"].dt.isocalendar().week.astype(int)
df["Μήνας"] = df["date"].dt.month.map(months_map)
df["Αριθμός Μήνα"] = df["date"].dt.month
df["Έτος"] = df["date"].dt.year

# ---------------------------------------------------
# ΕΠΙΚΕΦΑΛΙΔΑ
# ---------------------------------------------------
st.markdown('<div class="main-title">⚡ Σύστημα Παρακολούθησης Παραγωγής Ενέργειας</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Ανάλυση εργοστασίων, τύπων ενέργειας, γειτονικών χωρών και χρονικής εξέλιξης παραγωγής.</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("🎛️ Επιλογές")

available_dates = sorted(df["date"].dt.date.unique().tolist())
greek_plants = sorted(df[df["country"] == "Ελλάδα"]["plant"].unique().tolist())
energy_types = sorted(df["type"].unique().tolist())

selected_date = st.sidebar.selectbox(
    "Επίλεξε ημερομηνία",
    options=available_dates,
    index=len(available_dates) - 1
)

selected_plants = st.sidebar.multiselect(
    "Επίλεξε εργοστάσια",
    options=greek_plants,
    default=greek_plants[:3]
)

selected_types = st.sidebar.multiselect(
    "Επίλεξε τύπους ενέργειας",
    options=energy_types,
    default=energy_types
)

plant_a = st.sidebar.selectbox("Σύγκριση - Εργοστάσιο Α", greek_plants, index=0)
plant_b = st.sidebar.selectbox("Σύγκριση - Εργοστάσιο Β", greek_plants, index=1)

timeline_plant = st.sidebar.selectbox("Χρονική ανάλυση εργοστασίου", greek_plants, index=0)

if not selected_plants:
    st.warning("Επίλεξε τουλάχιστον ένα εργοστάσιο.")
    st.stop()

# ---------------------------------------------------
# ΔΕΔΟΜΕΝΑ ΗΜΕΡΑΣ
# ---------------------------------------------------
day_df = df[df["date"].dt.date == selected_date].copy()

filtered = day_df[
    (day_df["plant"].isin(selected_plants)) &
    (day_df["type"].isin(selected_types))
].copy()

# ---------------------------------------------------
# ΒΑΣΙΚΟΙ ΔΕΙΚΤΕΣ
# ---------------------------------------------------
st.markdown("### 📊 Βασικοί Δείκτες")

m1, m2, m3, m4 = st.columns(4)

total_energy = int(filtered["energy"].sum()) if not filtered.empty else 0
avg_energy = round(filtered["energy"].mean(), 2) if not filtered.empty else 0
max_energy = int(filtered["energy"].max()) if not filtered.empty else 0
plants_count = len(filtered["plant"].unique()) if not filtered.empty else 0

m1.metric("Συνολική Ενέργεια", f"{total_energy} MWh")
m2.metric("Μέση Ενέργεια", f"{avg_energy} MWh")
m3.metric("Μέγιστη Παραγωγή", f"{max_energy} MWh")
m4.metric("Επιλεγμένα Εργοστάσια", plants_count)

# ---------------------------------------------------
# ΣΥΜΠΕΡΑΣΜΑΤΑ
# ---------------------------------------------------
if not filtered.empty:
    top_plant = filtered.loc[filtered["energy"].idxmax(), "plant"]
    low_plant = filtered.loc[filtered["energy"].idxmin(), "plant"]
    dominant_type = filtered.groupby("type")["energy"].sum().idxmax()

    st.markdown(
        f"""
        <div class="insight-box">
        <b>Συμπεράσματα για την {selected_date}</b><br><br>
        • Το εργοστάσιο με τη μεγαλύτερη παραγωγή είναι το <b>{top_plant}</b>.<br>
        • Το εργοστάσιο με τη μικρότερη παραγωγή είναι το <b>{low_plant}</b>.<br>
        • Ο κυρίαρχος τύπος ενέργειας είναι ο <b>{dominant_type}</b>.<br>
        • Η συνολική παραγωγή των επιλεγμένων εργοστασίων είναι <b>{total_energy} MWh</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Επισκόπηση",
    "📈 Γραφήματα Ημέρας",
    "⚖️ Σύγκριση Εργοστασίων",
    "🌍 Χώρες και Στατιστικά",
    "🕒 Χρονική Ανάλυση"
])

# ---------------------------------------------------
# TAB 1
# ---------------------------------------------------
with tab1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Δεδομένα Επιλεγμένης Ημέρας")

    if filtered.empty:
        st.info("Δεν υπάρχουν δεδομένα για τα φίλτρα που επέλεξες.")
    else:
        display_df = filtered.rename(columns={
            "plant": "Εργοστάσιο",
            "country": "Χώρα",
            "date": "Ημερομηνία",
            "energy": "Ενέργεια (MWh)",
            "type": "Τύπος Ενέργειας"
        })
        st.dataframe(display_df[["Εργοστάσιο", "Χώρα", "Ημερομηνία", "Ενέργεια (MWh)", "Τύπος Ενέργειας"]], use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# TAB 2
# ---------------------------------------------------
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("Σύγκριση Επιλεγμένων Εργοστασίων")

        if filtered.empty:
            st.info("Δεν υπάρχουν δεδομένα για το γράφημα.")
        else:
            chart_df = filtered.rename(columns={
                "plant": "Εργοστάσιο",
                "energy": "Ενέργεια (MWh)"
            })

            fig_bar = px.bar(
                chart_df.sort_values("Ενέργεια (MWh)", ascending=False),
                x="Εργοστάσιο",
                y="Ενέργεια (MWh)",
                color="Εργοστάσιο",
                text_auto=True,
                template="plotly_dark"
            )
            fig_bar.update_layout(
                xaxis_title="Εργοστάσιο",
                yaxis_title="Ενέργεια (MWh)",
                showlegend=False,
                height=430
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("Κατανομή ανά Τύπο Ενέργειας")

        if filtered.empty:
            st.info("Δεν υπάρχουν δεδομένα για την κατανομή.")
        else:
            pie_data = filtered.groupby("type", as_index=False)["energy"].sum()
            pie_data = pie_data.rename(columns={
                "type": "Τύπος Ενέργειας",
                "energy": "Ενέργεια (MWh)"
            })

            fig_pie = px.pie(
                pie_data,
                values="Ενέργεια (MWh)",
                names="Τύπος Ενέργειας",
                hole=0.45,
                template="plotly_dark"
            )
            fig_pie.update_layout(height=430)
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# TAB 3
# ---------------------------------------------------
with tab3:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Άμεση Σύγκριση Δύο Εργοστασίων")

    compare_df = day_df[day_df["plant"].isin([plant_a, plant_b])].copy()

    if selected_types:
        compare_df = compare_df[compare_df["type"].isin(selected_types)]

    if compare_df.empty:
        st.info("Δεν υπάρχουν δεδομένα για τη συγκεκριμένη σύγκριση.")
    else:
        a_data = compare_df[compare_df["plant"] == plant_a]
        b_data = compare_df[compare_df["plant"] == plant_b]

        a_energy = int(a_data["energy"].sum()) if not a_data.empty else 0
        b_energy = int(b_data["energy"].sum()) if not b_data.empty else 0

        cc1, cc2 = st.columns(2)

        with cc1:
            st.markdown(
                f"""
                <div class="compare-box">
                <h4>{plant_a}</h4>
                <p><b>Παραγωγή:</b> {a_energy} MWh</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with cc2:
            st.markdown(
                f"""
                <div class="compare-box">
                <h4>{plant_b}</h4>
                <p><b>Παραγωγή:</b> {b_energy} MWh</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        if a_energy > b_energy:
            st.success(f"Το εργοστάσιο {plant_a} έχει μεγαλύτερη παραγωγή από το {plant_b}.")
        elif b_energy > a_energy:
            st.success(f"Το εργοστάσιο {plant_b} έχει μεγαλύτερη παραγωγή από το {plant_a}.")
        else:
            st.info("Τα δύο εργοστάσια έχουν ίδια παραγωγή.")

        compare_chart_df = compare_df.rename(columns={
            "plant": "Εργοστάσιο",
            "energy": "Ενέργεια (MWh)"
        })

        fig_compare = px.bar(
            compare_chart_df,
            x="Εργοστάσιο",
            y="Ενέργεια (MWh)",
            color="Εργοστάσιο",
            text_auto=True,
            template="plotly_dark"
        )
        fig_compare.update_layout(
            xaxis_title="Εργοστάσιο",
            yaxis_title="Ενέργεια (MWh)",
            showlegend=False,
            height=430
        )
        st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# TAB 4
# ---------------------------------------------------
with tab4:
    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("Σύγκριση με Γειτονικές Χώρες")

        comparison_df = day_df[
            day_df["country"].isin([
                "Ελλάδα",
                "Βουλγαρία",
                "Βόρεια Μακεδονία",
                "Αλβανία",
                "Τουρκία",
                "Ιταλία",
                "Κύπρος"
            ])
        ].copy()

        country_totals = comparison_df.groupby("country", as_index=False)["energy"].sum()
        country_totals = country_totals.rename(columns={
            "country": "Χώρα",
            "energy": "Ενέργεια (MWh)"
        })

        if country_totals.empty:
            st.info("Δεν υπάρχουν δεδομένα για σύγκριση χωρών.")
        else:
            fig_country = px.bar(
                country_totals,
                x="Χώρα",
                y="Ενέργεια (MWh)",
                color="Χώρα",
                text_auto=True,
                template="plotly_dark",
                hover_data={"Χώρα": True, "Ενέργεια (MWh)": True}
            )
            fig_country.update_layout(
                xaxis_title="Χώρα",
                yaxis_title="Συνολική Ενέργεια (MWh)",
                showlegend=False,
                height=430
            )
            st.plotly_chart(fig_country, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("Μέγιστη και Ελάχιστη Ενέργεια Ημέρας")

        gr_day = day_df[day_df["country"] == "Ελλάδα"].copy()

        if selected_types:
            gr_day = gr_day[gr_day["type"].isin(selected_types)]

        stats_df = gr_day[["plant", "energy"]].copy()
        stats_df = stats_df.rename(columns={
            "plant": "Εργοστάσιο",
            "energy": "Ενέργεια (MWh)"
        })

        if stats_df.empty:
            st.info("Δεν υπάρχουν διαθέσιμα στατιστικά.")
        else:
            max_row = stats_df.loc[stats_df["Ενέργεια (MWh)"].idxmax()]
            min_row = stats_df.loc[stats_df["Ενέργεια (MWh)"].idxmin()]

            s1, s2 = st.columns(2)
            s1.success(f"Μέγιστη τιμή: {max_row['Εργοστάσιο']} — {max_row['Ενέργεια (MWh)']} MWh")
            s2.error(f"Ελάχιστη τιμή: {min_row['Εργοστάσιο']} — {min_row['Ενέργεια (MWh)']} MWh")

            st.dataframe(
                stats_df.sort_values("Ενέργεια (MWh)", ascending=False),
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# TAB 5 - ΧΡΟΝΙΚΗ ΑΝΑΛΥΣΗ
# ---------------------------------------------------
with tab5:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader(f"Χρονική Εξέλιξη για το Εργοστάσιο: {timeline_plant}")

    plant_time_df = df[df["plant"] == timeline_plant].copy()

    # -------------------------------
    # 1. Ανάλυση ανά Ημέρα
    # -------------------------------
    st.markdown("#### Ανάλυση ανά Ημέρα")

    daily_df = plant_time_df.rename(columns={
        "date": "Ημερομηνία",
        "energy": "Ενέργεια (MWh)"
    })

    fig_daily = px.line(
        daily_df,
        x="Ημερομηνία",
        y="Ενέργεια (MWh)",
        template="plotly_dark"
    )
    fig_daily.update_layout(
        xaxis_title="Ημερομηνία",
        yaxis_title="Ενέργεια (MWh)",
        height=420
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    # -------------------------------
    # 2. Ανάλυση ανά Εβδομάδα / Μήνα
    # -------------------------------
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Ανάλυση ανά Εβδομάδα")

        week_df = (
            plant_time_df.groupby("Αριθμός Εβδομάδας", as_index=False)["energy"]
            .mean()
            .rename(columns={
                "Αριθμός Εβδομάδας": "Εβδομάδα",
                "energy": "Μέση Ενέργεια (MWh)"
            })
        )

        fig_week = px.line(
            week_df,
            x="Εβδομάδα",
            y="Μέση Ενέργεια (MWh)",
            markers=True,
            template="plotly_dark"
        )
        fig_week.update_layout(
            xaxis_title="Εβδομάδα Έτους",
            yaxis_title="Μέση Ενέργεια (MWh)",
            height=350
        )
        st.plotly_chart(fig_week, use_container_width=True)

    with c2:
        st.markdown("#### Ανάλυση ανά Μήνα")

        month_order = [
            "Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος",
            "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"
        ]

        month_df = (
            plant_time_df.groupby(["Αριθμός Μήνα", "Μήνας"], as_index=False)["energy"]
            .mean()
            .rename(columns={"energy": "Μέση Ενέργεια (MWh)"})
            .sort_values("Αριθμός Μήνα")
        )

        month_df["Μήνας"] = pd.Categorical(
            month_df["Μήνας"],
            categories=month_order,
            ordered=True
        )
        month_df = month_df.sort_values("Αριθμός Μήνα")

        fig_month = px.bar(
            month_df,
            x="Μήνας",
            y="Μέση Ενέργεια (MWh)",
            color="Μήνας",
            template="plotly_dark"
        )
        fig_month.update_layout(
            xaxis_title="Μήνας",
            yaxis_title="Μέση Ενέργεια (MWh)",
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig_month, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# DOWNLOAD CSV
# ---------------------------------------------------
csv_df = filtered.rename(columns={
    "plant": "Εργοστάσιο",
    "country": "Χώρα",
    "date": "Ημερομηνία",
    "energy": "Ενέργεια (MWh)",
    "type": "Τύπος Ενέργειας"
})

csv_data = csv_df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="⬇️ Λήψη δεδομένων σε CSV",
    data=csv_data,
    file_name=f"energeia_{selected_date}.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Δοκιμαστική έκδοση με προσωρινά δεδομένα. Επόμενο βήμα: σύνδεση με το ENTSO-E API.")