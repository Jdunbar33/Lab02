import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")

st.divider()
st.header("Load Data")

# Load CSV from repository (relative path)
csv_file_path = 'data.csv'

try:
    current_data_df = pd.read_csv(csv_file_path)
    st.success("CSV data loaded successfully!")
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    current_data_df = pd.DataFrame()

# Load JSON from repository (relative path)
json_file_path = 'data.json'

try:
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    st.success("JSON data loaded successfully!")
except Exception as e:
    st.error(f"Error loading JSON file: {e}")
    json_data = {}

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH (CSV Data - Average Hours of Sleep per Night)
st.subheader("Graph 1: Average Hours of Sleep per Night (Line Chart)")

if not current_data_df.empty:
    if 'Day' not in current_data_df.columns or 'Hours of Sleep' not in current_data_df.columns:
        st.error("The 'Day' or 'Hours of Sleep' column is missing from the CSV data.")
    else:
        # Normalize Day names (case-insensitive)
        current_data_df['Day'] = current_data_df['Day'].str.strip().str.lower()

        # Custom order for the days of the week
        day_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        # Ensure the 'Day' column is in the correct order
        current_data_df['Day'] = pd.Categorical(current_data_df['Day'], categories=day_order, ordered=True)

        days = current_data_df['Day'].unique()
        days = [str(day) for day in days]
        st.write(f"Unique Days in the CSV file: {', '.join(days)}")

        # We are assuming that 'Hours of Sleep' is a numeric column
        numeric_columns = ['Hours of Sleep']

        if numeric_columns:
            day_avg = current_data_df.groupby('Day')[numeric_columns].mean()

            fig, ax = plt.subplots(figsize=(10, 6))
            day_avg.plot(kind='line', ax=ax)

            ax.set_xlabel("Day")
            ax.set_ylabel("Average Hours of Sleep")
            ax.set_title(f"Average Hours of Sleep per Night (Days: {', '.join(days)})")

            st.pyplot(fig)

else:
    st.warning("CSV data is not available for graph 1.")

# GRAPH 2: DYNAMIC GRAPH (Budget-based Flight Path Selection)
st.subheader("Graph 2: Flight Paths within Your Budget (Scatter Plot)")

flight_paths = json_data.get("flight_paths", [])

flight_paths_with_costs = {}
for flight in flight_paths:
    flight_paths_with_costs[f"{flight['from']} → {flight['to']}"] = flight['cost']
    for connection in flight['connections']:
        flight_paths_with_costs[f"{flight['from']} → {flight['to']} → {connection['to']}"] = flight['cost'] + connection['cost']

budget = st.slider(
    "Select your budget",
    min_value=200,
    max_value=600,
    value=200,
    step=50
)

st.write(f"Your selected budget is: **${budget}**")

available_flights = {path: cost for path, cost in flight_paths_with_costs.items() if cost <= budget}

sorted_available_flights = sorted(available_flights.items(), key=lambda x: x[1])

if sorted_available_flights:
    st.write(f"These flight paths are within your budget of **${budget}**:")

    labels = [flight[0] for flight in sorted_available_flights]
    costs = [flight[1] for flight in sorted_available_flights]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(labels, costs, color='blue', marker='o')  # Scatter plot instead of bar chart

    ax.set_xlabel("Flight Path")
    ax.set_ylabel("Cost ($)")
    ax.set_title(f"Flight Paths Within Your Budget (Up to ${budget})")

    plt.xticks(rotation=45, ha="right", fontsize=8)

    st.pyplot(fig)

else:
    st.write("No flight paths are available within your budget.")

# GRAPH 3: DYNAMIC GRAPH (Select Flight Path and Tally the Total Cost)
st.subheader("Graph 3: Select Flight Path and Tally the Total Cost")

first_flight_path = st.selectbox(
    "Select your departure flight path from ATL",
    options=[f"{flight['from']} → {flight['to']}" for flight in flight_paths]
)

available_second_flights = {}
for flight in flight_paths:
    if f"{flight['from']} → {flight['to']}" == first_flight_path:
        available_second_flights = {
            f"{flight['from']} → {flight['to']} → {connection['to']}": flight['cost'] + connection['cost']
            for connection in flight['connections']
        }
        available_second_flights["End Trip"] = 0

second_flight_path = st.selectbox(
    f"Select your second flight path from {first_flight_path}",
    options=list(available_second_flights.keys())
)

total_cost = 0

if second_flight_path == "End Trip":
    total_cost = flight_paths_with_costs[first_flight_path]

else:
    total_cost = available_second_flights.get(second_flight_path, 0)

st.write(f"The total cost for your selected flight paths is **${total_cost}**.")

all_flight_paths = list(flight_paths_with_costs.keys())
all_flight_costs = list(flight_paths_with_costs.values())

highlighted_colors = [
    'red' if path == second_flight_path else 'blue' 
    for path in all_flight_paths
]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(all_flight_paths, all_flight_costs, color=highlighted_colors, width=0.5)

ax.set_xlabel("Flight Path")
ax.set_ylabel("Cost ($)")
ax.set_title("Flight Paths and Their Costs (Highlighted)")

for bar, cost in zip(bars, all_flight_costs):
    ax.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,  
        f"${cost}", ha='center', va='bottom', fontsize=10
    )

st.pyplot(fig)
