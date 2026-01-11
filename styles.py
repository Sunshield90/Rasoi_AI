import streamlit as st

def load_css(theme_color="#FFA726"):
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
        
        /* 1. DARK LUXURY BACKGROUND */
        .stApp {{
            background-color: #050505;
            background-image: 
                radial-gradient(at 20% 20%, {theme_color}10 0px, transparent 50%),
                radial-gradient(at 90% 90%, #1a1a1a 0px, transparent 50%);
            color: #E0E0E0;
            font-family: 'Outfit', sans-serif;
            overflow-x: hidden;
        }}

        /* 2. FIXED MARQUEE (Safely contained) */
        @keyframes scroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        
        .marquee-wrapper {{
            width: 100%;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.02);
            border-top: 1px solid rgba(255,255,255,0.05);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 20px;
            padding: 10px 0;
            mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
        }}
        
        .marquee-content {{
            display: flex;
            gap: 0;
            width: max-content;
            animation: scroll 50s linear infinite;
        }}
        
        .marquee-item {{
            width: 200px;
            height: 120px;
            object-fit: cover;
            opacity: 0.6;
            transition: opacity 0.3s;
            margin: 0;
            display: block;
        }}
        .marquee-item:hover {{ opacity: 1; }}

        /* 3. HERO LAYOUT */
        .hero-container {{
            position: relative;
            padding: 20px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }}
        
        .hero-bg-img {{
            position: absolute;
            width: 80%;
            opacity: 0.15; 
            z-index: 0;
            pointer-events: none;
            filter: grayscale(100%);
        }}
        
        .hero-text {{
            position: relative;
            z-index: 2;
        }}

        /* 4. COMPONENTS */
        .glass-card {{
            background: rgba(15, 15, 15, 0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        }}

        .stTextInput > div > div, .stTextArea > div > div, .stSelectbox > div > div {{
            background-color: #0F0F0F !important; 
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px;
        }}

        .stButton > button {{
            background: linear-gradient(135deg, {theme_color} 0%, {theme_color}cc 100%);
            color: white;
            border: none;
            height: 50px;
            font-weight: 700;
            border-radius: 10px;
            font-size: 16px;
            width: 100%;
        }}

        section[data-testid="stSidebar"] {{
            background-color: #080808;
            border-right: 1px solid rgba(255,255,255,0.05);
        }}

        #MainMenu, footer {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)