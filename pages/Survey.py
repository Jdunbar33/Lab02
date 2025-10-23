import streamlit as st
import pandas as pd
import os

data_file_path = os.path.expanduser('~/Documents/CS1301/Lab02/data.csv')

st.set_page_config(
    page_title="Sleep Survey",
    page_icon="🛏️",
)

st.title("Sleep Data Collection 🛏️")
st.write("Please fill out the form below to add your hours of sleep data to the dataset.")

with st.form("survey_form"):
    day_input = st.text_input("Enter a day of the week:")
    sleep_hours_input = st.text_input("Enter the hours of sleep for this day:")

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        new_data = {
            "Day": day_input,
            "Hours of Sleep": sleep_hours_input
        }

        if os.path.exists(data_file_path):
            current_data_df = pd.read_csv(data_file_path)
            new_data_df = pd.DataFrame([new_data])
            current_data_df = pd.concat([current_data_df, new_data_df], ignore_index=True)
            current_data_df = current_data_df[['Day', 'Hours of Sleep']]
            current_data_df.to_csv(data_file_path, index=False)
        else:
            df = pd.DataFrame([new_data])
            df.to_csv(data_file_path, index=False)

        st.success("Your data has been submitted!")
        st.write(f"You entered: **Day:** {day_input}, **Hours of Sleep:** {sleep_hours_input}")

st.divider()
st.header("Current Data in CSV")

if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
    current_data_df = pd.read_csv(data_file_path)
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")

