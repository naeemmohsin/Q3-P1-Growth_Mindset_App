import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import random

# Page Configuration
st.set_page_config(
    page_title="Growth Mindset Journey",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        max-width: 100%;
        margin: 0 auto;
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Responsive container */
    @media screen and (min-width: 1200px) {
        .stApp {
            padding: 2rem;
            max-width: 1200px;
        }
    }

    /* Responsive text sizing */
    @media screen and (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        h3 {
            font-size: 1.2rem !important;
        }
        p, .stMarkdown {
            font-size: 0.9rem !important;
        }
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        border: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        min-height: 44px; /* Touch-friendly size */
    }

    /* Input field styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 0.8rem !important;
        font-size: 16px !important; /* Prevent zoom on mobile */
        min-height: 44px; /* Touch-friendly size */
    }

    /* Responsive grid layout */
    @media screen and (max-width: 768px) {
        .row-widget.stHorizontal {
            flex-direction: column !important;
        }
        
        .row-widget.stHorizontal > div {
            width: 100% !important;
            margin-bottom: 1rem !important;
        }
    }

    /* Header styling */
    h1 {
        color: #1E88E5 !important;
        font-size: clamp(1.8rem, 4vw, 2.5rem) !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }

    h2 {
        color: #2196F3 !important;
        font-size: clamp(1.5rem, 3vw, 2rem) !important;
        font-weight: 600 !important;
    }

    h3 {
        color: #42A5F5 !important;
        font-size: clamp(1.2rem, 2.5vw, 1.5rem) !important;
        font-weight: 500 !important;
    }

    /* Info box styling */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 10px !important;
        padding: 0.8rem !important;
        margin: 0.5rem 0 !important;
    }

    /* Container styling */
    .css-1d391kg, .css-12oz5g7 {
        padding: 1rem !important;
        border-radius: 15px !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        margin: 0.5rem 0 !important;
    }

    /* Navigation menu styling */
    .stSelectbox > div > div {
        background-color: white !important;
        border-radius: 10px !important;
        min-height: 44px; /* Touch-friendly size */
    }

    /* Option menu responsive styling */
    #MainMenu {
        font-size: clamp(0.8rem, 2vw, 1rem) !important;
    }

    /* Charts responsive styling */
    .js-plotly-plot {
        width: 100% !important;
        max-width: 100% !important;
    }

    /* Lottie animation responsive */
    .stLottie {
        width: 100% !important;
        max-width: 300px !important;
        margin: 0 auto !important;
    }

    /* Expander responsive */
    .streamlit-expanderHeader {
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        min-height: 44px; /* Touch-friendly size */
    }

    /* Touch-friendly spacing */
    .stButton, .stSelectbox, .stTextInput, .stTextArea {
        margin: 0.5rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'reflections' not in st.session_state:
    st.session_state.reflections = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = []

# Growth mindset quotes
quotes = [
    "The only way to learn is to challenge yourself.",
    "Mistakes are proof that you're trying.",
    "Everything is hard before it becomes easy.",
    "Growth is a process. Results take time.",
    "Your potential is unlimited. Go do what you want to do.",
]

def load_lottie_url(url):
    try:
        r = requests.get(url, timeout=10)  # Add timeout
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load animations with fallback
lottie_growth = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_havmBuqUAz.json")
lottie_achievement = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

# Main App Layout
st.title("🌱 Growth Mindset Journey")

# Navigation
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Goals", "Reflections", "Progress"],
    icons=["house", "target", "journal", "graph-up"],
    orientation="horizontal",
)

if selected == "Dashboard":
    # Use different column ratios for mobile
    if st.session_state.get('mobile_view', True):
        col1 = st.container()
        col2 = st.container()
    else:
        col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Welcome to Your Growth Journey")
        st.write("Today's Inspiration:")
        st.info(random.choice(quotes))
        
        st.subheader("Quick Actions")
        quick_action = st.selectbox(
            "What would you like to do?",
            ["Set a new goal", "Write a reflection", "Log an achievement"]
        )
        
        if quick_action == "Set a new goal":
            goal = st.text_input("Enter your goal:")
            col_btn1, col_btn2 = st.columns([2, 1])
            with col_btn1:
                if st.button("Add Goal", use_container_width=True):
                    if goal:
                        st.session_state.goals.append({
                            "goal": goal,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "status": "In Progress"
                        })
                        st.success("Goal added successfully!")
    
    with col2:
        if lottie_growth:
            st_lottie(lottie_growth, height=200 if st.session_state.get('mobile_view', True) else 300)

elif selected == "Goals":
    st.header("Goal Tracker")
    
    # Add new goal
    with st.expander("Add New Goal"):
        goal = st.text_input("What's your new goal?")
        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            if st.button("Add", use_container_width=True):
                if goal:
                    st.session_state.goals.append({
                        "goal": goal,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "status": "In Progress"
                    })
                    st.success("Goal added successfully!")
    
    # Display goals
    if st.session_state.goals:
        for idx, goal in enumerate(st.session_state.goals):
            with st.container():
                st.write(f"**Goal:** {goal['goal']}")
                st.write(f"*Started on: {goal['date']}*")
                if st.button("Complete", key=f"complete_{idx}", use_container_width=True):
                    st.session_state.goals[idx]["status"] = "Completed"
                    st.session_state.achievements.append({
                        "achievement": f"Completed goal: {goal['goal']}",
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
                st.markdown("---")

elif selected == "Reflections":
    st.header("Daily Reflections")
    
    # Add new reflection
    with st.expander("Add New Reflection"):
        reflection = st.text_area("What's on your mind today?")
        mood = st.select_slider(
            "How are you feeling?",
            options=["😔", "😐", "🙂", "😊", "🌟"]
        )
        if st.button("Save Reflection"):
            if reflection:
                st.session_state.reflections.append({
                    "reflection": reflection,
                    "mood": mood,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                st.success("Reflection saved!")
    
    # Display reflections
    if st.session_state.reflections:
        for reflection in reversed(st.session_state.reflections):
            with st.container():
                st.write(f"**{reflection['date']}** {reflection['mood']}")
                st.write(reflection['reflection'])
                st.markdown("---")

elif selected == "Progress":
    st.header("Your Growth Journey")
    
    # Display achievements
    st.subheader("Recent Achievements")
    if st.session_state.achievements:
        for achievement in reversed(st.session_state.achievements):
            st.success(f"🏆 {achievement['achievement']} ({achievement['date']})")
    
    # Progress metrics
    if st.session_state.get('mobile_view', True):
        col1 = st.container()
        col2 = st.container()
    else:
        col1, col2 = st.columns(2)

    with col1:
        completed_goals = len([g for g in st.session_state.goals if g['status'] == "Completed"])
        total_goals = len(st.session_state.goals)
        if total_goals > 0:
            progress = (completed_goals / total_goals) * 100
            fig = px.pie(
                values=[completed_goals, total_goals - completed_goals],
                names=['Completed', 'In Progress'],
                title='Goal Completion Rate'
            )
            # Make the chart responsive
            fig.update_layout(
                autosize=True,
                margin=dict(l=10, r=10, t=30, b=10),
                height=300 if st.session_state.get('mobile_view', True) else 400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if lottie_achievement:
            st_lottie(lottie_achievement, height=200 if st.session_state.get('mobile_view', True) else 300)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; padding: 1rem;'>"
    "*Remember: Your mindset shapes your reality. Keep growing! 🌱*"
    "</div>", 
    unsafe_allow_html=True
) 