import streamlit as st
import requests
import pandas as pd

# Import your agent modules
from user_conversation_agent import UserConversationAgent
from api_calling_agent import APICallingAgent
from summarizer_agent import SummarizerAgent
from best_crop_recommendation_agent import BestCropRecommendationAgent
from planning_agent import PlanningAgent
from doctor_agent import DoctorAgent

# ---------- Custom CSS Styling for a Modern, Dark-Themed UI ----------
st.markdown(
    """
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

    html, body {
        margin: 0;
        padding: 0;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #2c3e50, #4ca1af);
        color: #ecf0f1;
    }
    
    .stApp {
        background: linear-gradient(135deg, #2c3e50, #4ca1af);
    }
    
    /* Header styling */
    .header {
        font-size: 64px;
        text-align: center;
        margin-top: 30px;
        font-weight: 700;
        color: #ecf0f1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .subheader {
        font-size: 32px;
        text-align: center;
        color: #bdc3c7;
        margin-top: 10px;
    }
    
    .description {
        font-size: 20px;
        text-align: center;
        color: #bdc3c7;
        margin: 20px auto;
        max-width: 800px;
        line-height: 1.6;
    }
    
    /* Navigation title styling */
    .nav-title {
        font-size: 24px;
        font-weight: 600;
        color: #ecf0f1;
        margin-bottom: 15px;
    }
    
    /* Section title styling */
    .section-title {
        font-size: 40px;
        text-align: center;
        color: #ecf0f1;
        margin: 30px 0;
        border-bottom: 3px solid #00b894;
        padding-bottom: 10px;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #00b894;
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #019875;
        transform: scale(1.05);
    }
    
    /* Form container styling with a semi-transparent dark background */
    .form-container {
        background: rgba(44, 62, 80, 0.85);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
        margin: 20px auto;
        max-width: 700px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Initialize Agents ----------
user_agent = UserConversationAgent()
api_agent = APICallingAgent()
summary_agent = SummarizerAgent()
crop_agent = BestCropRecommendationAgent()
planning_agent_obj = PlanningAgent()
doctor_agent_obj = DoctorAgent()

# ---------- Initialize Session State Variables ----------
if "summarized_data" not in st.session_state:
    st.session_state["summarized_data"] = {}
if "selected_crop" not in st.session_state:
    st.session_state["selected_crop"] = None

# ---------- Sidebar Navigation ----------
st.sidebar.markdown('<div class="nav-title">Navigation</div>', unsafe_allow_html=True)
pages = ["🏠 Home", "🌾 Best Crop Recommendation", "📅 Planning", "🩺 Plant Health Diagnosis"]
page = st.sidebar.radio("Go to", pages)

# ---------- Home (Dashboard) Page ----------
if page == "🏠 Home":
    st.markdown('<div class="header">Smart Farming Assistant 🚜</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Professional Dashboard Overview</div>', unsafe_allow_html=True)
    
    # Use real data if available; otherwise use dummy data for the dashboard
    if st.session_state["summarized_data"]:
        data = st.session_state["summarized_data"]
        user_data = data.get("user", {})
        api_data = data.get("api", {})
    else:
        # Dummy Data for Dashboard
        user_data = {
            "budget": "5000",
            "resources": "Water, Fertilizers",
            "location": "California",
            "soil_type": "Loamy",
            "water_availability": "High",
            "equipment": "Tractor, Irrigation System"
        }
        api_data = {
            "economic": {
                "average_income": 3500,
                "crop_prices": {
                    "Wheat": 3.5,
                    "Corn": 2.9,
                    "Soybean": 4.1,
                    "Rice": 3.2,
                    "Barley": 3.0
                }
            },
            "environmental": {
                "temperature": 24,
                "rainfall": 120,
                "humidity": 65
            }
        }
    
    economic_data = api_data.get("economic", {})
    environmental_data = api_data.get("environmental", {})
    
    # Display key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_income = economic_data.get("average_income", 0)
        st.metric("Avg Income", f"${avg_income:,.2f}")
    with col2:
        temp = environmental_data.get("temperature", 0)
        st.metric("Temp", f"{temp:.1f} °C")
    with col3:
        rainfall = environmental_data.get("rainfall", 0)
        st.metric("Rainfall", f"{rainfall:.1f} mm")
    with col4:
        humidity = environmental_data.get("humidity", 0)
        st.metric("Humidity", f"{humidity:.1f} %")
    
    st.markdown('<div class="section-title">Crop Prices Overview</div>', unsafe_allow_html=True)
    # Prepare data for crop prices chart
    crop_prices = economic_data.get("crop_prices", {})
    if crop_prices:
        df_prices = pd.DataFrame.from_dict(crop_prices, orient='index', columns=['Price'])
        df_prices = df_prices.sort_values("Price")
        st.bar_chart(df_prices)
    else:
        st.info("No crop price data available yet.")
    
    st.markdown('<div class="description">Use the sidebar to navigate to different sections of the application.</div>', unsafe_allow_html=True)

# ---------- Best Crop Recommendation Page ----------
elif page == "🌾 Best Crop Recommendation":
    st.markdown('<div class="section-title">Best Crop Recommendation 🌾</div>', unsafe_allow_html=True)
    st.markdown('<div class="description">Step 1: Provide Your Farm Details 📝</div>', unsafe_allow_html=True)
    
    with st.form(key="user_input_form"):
        with st.container():
            st.markdown("<div class='form-container'>", unsafe_allow_html=True)
            budget = st.text_input("Budget 💰", placeholder="Enter your budget")
            resources = st.text_input("Resources 🔧", placeholder="Enter available resources")
            location = st.text_input("Location 📍", placeholder="Enter your farm location")
            soil_type = st.text_input("Soil Type 🌱", placeholder="Enter your soil type")
            water_availability = st.text_input("Water Availability 💧", placeholder="Enter water availability")
            equipment = st.text_input("Equipment 🚜", placeholder="Enter available equipment")
            submit_user_data = st.form_submit_button(label="Submit")
            st.markdown("</div>", unsafe_allow_html=True)
    
    if submit_user_data:
        form_data = {
            "budget": budget,
            "resources": resources,
            "location": location,
            "soil_type": soil_type,
            "water_availability": water_availability,
            "equipment": equipment
        }
        # Collect user data using the User Conversation Agent
        user_data = user_agent.collect_user_input(form_data)
        # Fetch external API data using the API Calling Agent
        api_data = api_agent.get_all_api_data(location)
        # Aggregate the data using the Summarizer Agent
        summarized_data = summary_agent.aggregate_data(user_data, api_data)
        st.session_state["summarized_data"] = summarized_data
        st.success("✅ Data collected and summarized successfully!")
    
    if st.session_state["summarized_data"]:
        st.markdown('<div class="description">Step 2: Choose Your Preferred Crop 🌾</div>', unsafe_allow_html=True)
        recommended_crops = crop_agent.recommend_crops(st.session_state["summarized_data"])
        selected_crop = st.radio("Select a Crop", recommended_crops)
        if st.button("Confirm Crop Selection", key="confirm_crop"):
            st.session_state["selected_crop"] = selected_crop
            st.success(f"✅ You have selected: {selected_crop}. Proceed to the Planning page.")

# ---------- Planning Page ----------
elif page == "📅 Planning":
    st.markdown('<div class="section-title">Planning 🗓️</div>', unsafe_allow_html=True)
    selected_crop = st.session_state.get("selected_crop", None)
    if not selected_crop:
        st.warning("⚠️ Please complete the Best Crop Recommendation page and select a crop first.")
    else:
        st.subheader(f"Planning for: {selected_crop} 🌱")
        additional_input = st.text_area("Additional Details (if any) ✍️", placeholder="Provide any extra information for your plan here...")
        if st.button("Generate Growing Plan", key="generate_plan"):
            summarized_data = st.session_state.get("summarized_data", {})
            plan = planning_agent_obj.provide_plan(summarized_data, selected_crop, additional_input)
            st.markdown('<div class="subheader">Sustainable Growing Plan 💡</div>', unsafe_allow_html=True)
            st.text(plan)

# ---------- Plant Health Diagnosis Page ----------
elif page == "🩺 Plant Health Diagnosis":
    st.markdown('<div class="section-title">Plant Health Diagnosis 🩺</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a plant image 📸", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Diagnose Plant Health", key="diagnose"):
            summarized_data = st.session_state.get("summarized_data", {})
            diagnosis = doctor_agent_obj.diagnose_plant(uploaded_file, summarized_data)
            st.markdown('<div class="subheader">Diagnosis Result 🔍</div>', unsafe_allow_html=True)
            st.write(diagnosis)
