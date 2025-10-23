import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sleep Survey",
    page_icon="🛏️",
)

st.title("Sleep Data Collection 🛏️")
st.write("Please fill out the form below to add your hours of sleep data to the dataset.")

# Path to the CSV file in the repository (assuming it's on GitHub)
csv_file_path = 'data.csv'  # Replace this with the path where your file is stored on GitHub

# Check if CSV exists and load it
try:
    current_data_df = pd.read_csv(csv_file_path)
    st.success("CSV data loaded successfully!")
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    current_data_df = pd.DataFrame()

# Form to submit data
with st.form("survey_form"):
    day_input = st.text_input("Enter a day of the week:")
    sleep_hours_input = st.text_input("Enter the hours of sleep for this day:")

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        new_data = {
            "Day": day_input,
            "Hours of Sleep": sleep_hours_input
        }

        if not current_data_df.empty:
            # Append the new data to the existing dataframe
            new_data_df = pd.DataFrame([new_data])
            current_data_df = pd.concat([current_data_df, new_data_df], ignore_index=True)
            current_data_df = current_data_df[['Day', 'Hours of Sleep']]  # Ensure correct column order
            
            # Here we would typically save it back to GitHub, but since we can't persist the file,
            # we'll simulate the save by updating the local dataframe (within this session)
            st.success("Your data has been submitted!")
            st.write(f"You entered: **Day:** {day_input}, **Hours of Sleep:** {sleep_hours_input}")

            # Show the updated data
            st.dataframe(current_data_df)

        else:
            # If CSV is empty or doesn't exist, create a new one
            df = pd.DataFrame([new_data])
            df.to_csv(csv_file_path, index=False)
            st.success("Your data has been submitted!")
            st.write(f"You entered: **Day:** {day_input}, **Hours of Sleep:** {sleep_hours_input}")

# Display the current data in CSV format
st.divider()
st.header("Current Data in CSV")

if not current_data_df.empty:
    st.dataframe(current_data_df)
else:
    st.warning("No data to display yet. Please submit your data first.")
