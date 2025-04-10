# Streamlit-based prototype for botulism signal dashboard
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Simulate real-time data
np.random.seed(42)
locations = [
    ("Moscow", 55.7558, 37.6173),
    ("Irkutsk", 52.2870, 104.3050),
    ("St. Petersburg", 59.9343, 30.3351),
    ("Kazan", 55.7963, 49.1088),
    ("Novosibirsk", 55.0302, 82.9204)
]

entries = []
for i in range(20):
    city, lat, lon = locations[np.random.randint(0, len(locations))]
    date = datetime.date.today() - datetime.timedelta(days=np.random.randint(0, 180))
    urgency = np.random.randint(1, 6)
    severity = np.random.randint(1, 6)
    population = np.random.choice(["General", "Children", "Elderly"])
    entries.append({
        "Date": date,
        "Location": city,
        "Latitude": lat,
        "Longitude": lon,
        "Urgency": urgency,
        "Severity": severity,
        "Population": population
    })

df = pd.DataFrame(entries)

# Sidebar filters
st.sidebar.title("Filters")
selected_city = st.sidebar.multiselect("Select location", df["Location"].unique(), default=df["Location"].unique())
min_urgency = st.sidebar.slider("Minimum urgency", 1, 5, 1)
min_severity = st.sidebar.slider("Minimum severity", 1, 5, 1)

filtered_df = df[(df["Location"].isin(selected_city)) &
                 (df["Urgency"] >= min_urgency) &
                 (df["Severity"] >= min_severity)]

st.title("Botulism Signal Monitoring Dashboard")
st.markdown("This dashboard simulates real-time outbreak signals with geolocation and priority scoring.")

# Display table
st.subheader("Filtered Signals")
st.dataframe(filtered_df)

# Map
st.subheader("Geolocation of Signals")
map_center = [56.0, 60.0]
map_outbreak = folium.Map(location=map_center, zoom_start=4, tiles='CartoDB positron')
marker_cluster = MarkerCluster().add_to(map_outbreak)

for _, row in filtered_df.iterrows():
    popup = f"<b>{row['Location']}</b><br>Date: {row['Date']}<br>Urgency: {row['Urgency']}<br>Severity: {row['Severity']}<br>Affected: {row['Population']}"
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup,
        icon=folium.Icon(color="red" if row['Urgency'] >= 4 else "orange")
    ).add_to(marker_cluster)

folium_static(map_outbreak)

# Priority score chart
st.subheader("Priority Score Overview")
df["Priority Score"] = df["Urgency"] * 3 + df["Severity"] * 2
chart_data = df.groupby("Location")["Priority Score"].mean().sort_values(ascending=False)
st.bar_chart(chart_data)
