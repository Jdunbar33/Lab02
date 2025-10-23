import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Sleep Survey",
    page_icon="🛏️",
)

st.title("Sleep Data Collection 🛏️")
st.write("Please fill out the form below to add your hours of sleep data to the dataset.")

# File uploader for the CSV file
csv_file = st.file_uploader("Upload your CSV file", type="csv")

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

        if csv_file is not None:
            # Read the uploaded CSV file
            current_data_df = pd.read_csv(csv_file)

            # Append the new data
            new_data_df = pd.DataFrame([new_data])
            current_data_df = pd.concat([current_data_df, new_data_df], ignore_index=True)

            # Ensure correct column order
            current_data_df = current_data_df[['Day', 'Hours of Sleep']]
            
            # Save the updated dataframe back to the uploaded file's buffer
            st.success("Your data has been submitted!")
            st.write(f"You entered: **Day:** {day_input}, **Hours of Sleep:** {sleep_hours_input}")

            # Show the updated data
            st.dataframe(current_data_df)

        else:
            st.warning("Please upload a CSV file to store your data.")

# Display the current data in CSV format
st.divider()
st.header("Current Data in CSV")

if csv_file is not None:
    current_data_df = pd.read_csv(csv_file)
    st.dataframe(current_data_df)
else:
    st.warning("Please upload a CSV file to view the data.")
