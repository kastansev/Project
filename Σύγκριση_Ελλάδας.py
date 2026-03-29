
import streamlit as st
from entsoe import Client
import pandas as pd

# αρχκη συνδεση με ΑΡΙ
API_KEY = "YOUR_API_KEY"
client = Client(api_key=API_KEY)

# διαθέσιμες χώρες (απλοποιημένη λίστα για τώρα)
country_codes = {
    "Ελλάδα 🇬🇷": "GR",
    "Ιταλία 🇮🇹": "IT",
    "Βουλγαρία 🇧🇬": "BG"
}

# βοηθητική συνάρτηση για λήψη και καθαρισμό δεδομένων παραγωγής
def fetch_generation_data(code, start, end):
    try:
        df = client.generation(start, end, country=code)
    except Exception as e:
        st.warning(f"Δεν φορτώθηκαν δεδομένα για {code}")
        return pd.DataFrame()

    if df.empty:
        return df

    # αντικατάσταση ελλιπών τιμών και υπολογισμός συνολικής παραγωγής
    df = df.fillna(0)
    df["total"] = df.sum(axis=1)
    return df
 
# χρονικό παράθυρο (τελευταίες 7 ημέρες)
now = pd.Timestamp.now(tz="Europe/Athens")
week_ago = now - pd.Timedelta(days=7)

#  UI 
st.title("Σύγκριση Παραγωγής Ηλεκτρικής Ενέργειας")

selected = st.multiselect(
    "Διάλεξε χώρες:",
    list(country_codes.keys()),
    default=["Ελλάδα 🇬🇷", "Ιταλία 🇮🇹"]
)

if not selected:
    st.info("Επίλεξε τουλάχιστον μία χώρα για να δεις δεδομένα.")
    st.stop()

# δημιουργία συνόλου δεδομένων σύγκρισης
results = pd.DataFrame()

for label in selected:
    code = country_codes[label]
    data = fetch_generation_data(code, week_ago, now)

    if data.empty:
        continue

    daily = data["total"].resample("D").sum()
    results[label] = daily

#αποτέλεσμα 
if results.empty:
    st.error("Δεν υπάρχουν διαθέσιμα δεδομένα.")
else:
    st.line_chart(results)