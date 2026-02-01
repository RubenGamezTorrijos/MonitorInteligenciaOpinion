# Professional Streamlit Opinion Intelligence Monitor - styles.py

import streamlit as st

def apply_custom_styles():
    """Injects professional vanilla CSS for a premium glassmorphism look."""
    st.markdown("""
    <style>
        /* Main background and font */
        .stApp {
            background-color: #0F172A;
            font-family: 'Inter', sans-serif;
        }
        
        /* Glassmorphism containers */
        div[data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 15px;
            backdrop-filter: blur(10px);
        }
        
        /* Metric values */
        div[data-testid="stMetricValue"] {
            color: #00B4D8;
            font-weight: 700;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #1E293B;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Custom Analyze Button */
        div.stButton > button {
            background: linear-gradient(90deg, #00B4D8 0%, #0077B6 100%);
            color: white;
            border-radius: 8px;
            padding: 0.6rem 2rem;
            font-weight: 600;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 180, 216, 0.4);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            font-weight: 400;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 180, 216, 0.1);
            font-weight: 600;
            border-bottom: 2px solid #00B4D8 !important;
        }
    </style>
    """, unsafe_allow_html=True)
