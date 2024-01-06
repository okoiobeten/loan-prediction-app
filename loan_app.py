import streamlit as st
import pandas as pd
import pickle

# Load the trained model (replace 'your_model.pkl' with your model's filename)
with open('myloan_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Function to set the page background color to light blue
def set_bg_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: lightblue;
        }
        .title {
            background-color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit application layout
def main():
    set_bg_color()
    st.title("Bank Loan Status Prediction")

    # Create two columns for inputs
    col1, col2 = st.columns(2)

    with col1:
        # User inputs in the first column
        dependents = st.number_input("Dependents", min_value=0, step=1)
        applicant_income = st.number_input("Applicant Income", min_value=0)
        coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
        loan_amount = st.number_input("Loan Amount", min_value=0)
        loan_amount_term = st.number_input("Loan Amount Term", min_value=0)
        credit_history = st.selectbox("Credit History", [0, 1])

    with col2:
        # User inputs in the second column
        gender_encoded = st.selectbox("Gender", ["Male", "Female"])
        married_encoded = st.selectbox("Married", ["Yes", "No"])
        education_encoded = st.selectbox("Education", ["Graduate", "Not Graduate"])
        self_employed_encoded = st.selectbox("Self Employed", ["Yes", "No"])
        property_area = st.selectbox("Property Area", ["Rural", "Semiurban", "Urban"])

    # Encoding categorical inputs
    gender_encoded = 1 if gender_encoded == "Male" else 0
    married_encoded = 1 if married_encoded == "Yes" else 0
    education_encoded = 1 if education_encoded == "Graduate" else 0
    self_employed_encoded = 1 if self_employed_encoded == "Yes" else 0
    property_area_rural = 1 if property_area == "Rural" else 0
    property_area_semiurban = 1 if property_area == "Semiurban" else 0
    property_area_urban = 1 if property_area == "Urban" else 0

    # Submit button
    if st.button("Check Loan Status"):
        # Create a DataFrame for the model
        input_data = pd.DataFrame([[dependents, applicant_income, coapplicant_income, loan_amount, 
                                    loan_amount_term, credit_history, gender_encoded, married_encoded, 
                                    education_encoded, self_employed_encoded, property_area_rural, 
                                    property_area_semiurban, property_area_urban]],
                                  columns=['Dependents', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                                           'Loan_Amount_Term', 'Credit_History', 'Gender_Encoded',
                                           'Married_Encoded', 'Education_Encoded', 'Self_Employed_Encoded',
                                           'Property_Area_Rural', 'Property_Area_Semiurban',
                                           'Property_Area_Urban'])

        # Make a prediction
        prediction = model.predict(input_data)

        # Display the result
        result = "Accepted" if prediction[0] == 1 else "Rejected"
        st.success(f"Loan Status: {result}")

if __name__ == "__main__":
    main()
