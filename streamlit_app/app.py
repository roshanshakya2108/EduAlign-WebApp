import pandas as pd
import joblib
import streamlit as st
import requests

# Load the pre-trained model
model = joblib.load('school_needs_model.pkl')


def get_prediction(input_data):
    """Function to get prediction from the model."""
    input_data = pd.get_dummies(
        input_data, columns=['State', 'Category'], drop_first=True)
    input_data = input_data.reindex(
        columns=model.feature_names_in_, fill_value=0)
    prediction = model.predict(input_data)
    return "Yes" if prediction[0] == 1 else "No"


def submit_to_database(data):
    """Function to submit data to PHP backend."""
    response = requests.post(
        'http://your-php-backend-url/submit.php', data=data)
    return response.text


def main():
    st.title("School Resource Allocation Prediction")

    st.sidebar.header("Input Data")

    # Sidebar inputs
    state = st.sidebar.selectbox(
        'State', ['Tamil Nadu', 'Kerala', 'Uttar Pradesh', 'West Bengal', 'Gujarat'])
    category = st.sidebar.selectbox(
        'Category', ['Upper Primary', 'Secondary', 'Primary', 'Higher Secondary'])
    total_students = st.sidebar.number_input('Total Students', min_value=0)
    total_teachers = st.sidebar.number_input('Total Teachers', min_value=0)
    total_classrooms = st.sidebar.number_input('Total Classrooms', min_value=0)
    student_teacher_ratio = st.sidebar.number_input(
        'Student Teacher Ratio', format="%.2f")
    has_computer_lab = st.sidebar.selectbox('Has Computer Lab', [0, 1])
    has_library = st.sidebar.selectbox('Has Library', [0, 1])
    odd_structure = st.sidebar.selectbox('Odd Structure', [0, 1])
    infrastructure_score = st.sidebar.number_input(
        'Infrastructure Score', format="%.2f")
    performance_score = st.sidebar.number_input(
        'Performance Score', format="%.2f")

    # Convert input data to DataFrame
    input_data = pd.DataFrame({
        'State': [state],
        'Category': [category],
        'Total_Students': [total_students],
        'Total_Teachers': [total_teachers],
        'Total_Classrooms': [total_classrooms],
        'Student_Teacher_Ratio': [student_teacher_ratio],
        'Has_Computer_Lab': [has_computer_lab],
        'Has_Library': [has_library],
        'Odd_Structure': [odd_structure],
        'Infrastructure_Score': [infrastructure_score],
        'Performance_Score': [performance_score]
    })

    if st.sidebar.button('Predict'):
        # Get prediction
        result = get_prediction(input_data)

        # Display result
        st.subheader("Prediction Results")
        st.write(f"**Needs Resource Allocation:** {result}")

        # Submit data to the database
        data_to_submit = input_data.to_dict(orient='records')[0]
        data_to_submit['Prediction'] = result
        response = submit_to_database(data_to_submit)
        st.write(f"**Database Submission Status:** {response}")


if __name__ == "__main__":
    main()
