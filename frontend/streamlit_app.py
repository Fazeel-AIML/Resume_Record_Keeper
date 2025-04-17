import streamlit as st
import requests

# Define the API endpoint with port 8000 hardcoded
API_URL = "http://127.0.0.1:8000/api/upload_resume/"

st.title("AI-Powered Resume Analyzer")

# Input fields for user data
name = st.text_input("Enter Your Name")
current_designation = st.text_input("Enter Your Current Designation")
experiences = st.number_input("Enter Number of Experiences", min_value=0, step=1)
skills = st.text_input("Enter Your Skills (comma-separated, e.g., Python, Java, SQL)")

# File uploader for PDF resumes
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

# Button to submit the form
if st.button("Analyze Resume"):
    if not all([name, current_designation, experiences is not None, skills, uploaded_file]):
        st.error("Please fill in all fields and upload a resume.")
    else:
        # Prepare the data and file for upload
        data = {
            "name": name,
            "current_designation": current_designation,
            "experiences": experiences,
            "skills": skills
        }
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

        # Attempt to send the data to the Django API with increased timeout
        try:
            response = requests.post(API_URL, data=data, files=files, timeout=30)  # Increased from 10 to 30 seconds
            response.raise_for_status()  # Raise an exception for bad status codes

            # Check if the request was successful (expecting 201 from your API)
            if response.status_code == 201:
                data = response.json()

                # Display submitted user data
                st.subheader("Submitted Information:")
                st.write(f"Name: {data.get('name', 'N/A')}")
                st.write(f"Current Designation: {data.get('current_designation', 'N/A')}")
                st.write(f"Number of Experiences: {data.get('experiences', 0)}")
                st.write(f"Skills: {data.get('skills', 'N/A')}")

                # Display generated summary
                st.subheader("Resume Summary:")
                summary = data.get("summary", "No summary generated")
                st.text(summary)

            else:
                st.error(f"Unexpected response from server: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please ensure the Django server is running on http://127.0.0.1:8000.")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The server might be slow or unresponsive. Try again or upload a smaller file.")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to analyze resume: {str(e)}")