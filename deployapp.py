import streamlit as st
import time
import os  # Added to check for file existence
from Frontend import styles, components
from Backend import ai_engine, offline_data, auth

# 1. SETUP & SESSION STATE
st.set_page_config(page_title="Rasoi AI", page_icon="🍳", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- THEME & COLOR STATE ---
if 'theme_mode' not in st.session_state:
    st.session_state['theme_mode'] = "Dark"
if 'theme_color' not in st.session_state:
    st.session_state['theme_color'] = "#FFA726" # Default Orange

# --- 2. LOGIN SCREEN ---
def show_login_page():
    st.markdown(f"""
        <style>
            /* 1. BACKGROUND IMAGE */
            .stApp {{
                background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.9)),
                            url('https://images.unsplash.com/photo-1556911220-e15b29be8c8f?q=80&w=2940&auto=format&fit=crop');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            /* 2. LOGIN INPUTS (White Background / Black Text) */
            div[data-testid="stForm"] input {{
                background-color: #FFFFFF !important;
                color: #000000 !important;
                font-weight: 600 !important;
                border: 2px solid #ddd !important;
                border-radius: 8px !important;
                padding: 12px !important;
                caret-color: black !important;
            }}
            label p {{
                color: #FFFFFF !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
                text-shadow: 0 1px 3px rgba(0,0,0,0.8);
            }}

            /* 3. LOGIN BOX */
            .login-box {{
                background: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 167, 38, 0.3);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 50px rgba(0,0,0,0.8);
            }}

            /* 4. BUTTONS */
            div.stButton > button {{
                background: linear-gradient(135deg, {st.session_state['theme_color']} 0%, #FF5722 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                font-weight: bold !important;
                width: 100%;
            }}
            div.stButton > button:hover {{ transform: scale(1.02); }}

            /* 5. TYPOGRAPHY - UPDATED FOR HIGH VISIBILITY */
            h1 {{ 
                font-size: 4rem !important; 
                font-weight: 900 !important; 
                color: #FFFFFF !important; /* Pure white color for visibility */
                text-shadow: 0 4px 15px rgba(0,0,0,1) !important; /* Deep shadow to separate from background */
            }}
            .highlight {{ color: {st.session_state['theme_color']}; text-shadow: 0 0 20px rgba(255,167,38,0.6); }}
            .subtitle {{ font-size: 1.3rem; color: #DDD; font-weight: 300; text-shadow: 0 2px 4px black; }}
            
            #MainMenu, header, footer, div[data-testid="stDecoration"] {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.4, 1], gap="large")

    with c1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"# Master your kitchen with <span class='highlight'>Rasoi AI</span>.", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Stop wasting food. Turn ingredients into Michelin-star recipes instantly.</p>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; gap: 30px; margin-top: 40px; color: white;">
            <div><h2>∞</h2><small>Possibilities</small></div>
            <div><h2>0%</h2><small>Food Waste</small></div>
            <div><h2>100%</h2><small>Delicious</small></div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        # Centered Logo on Login
        if os.path.exists("logo.png"):
            l_col1, l_col2, l_col3 = st.columns([1, 2, 1])
            with l_col2:
                st.image("logo.png", use_container_width=True)

        st.markdown("<h2 style='text-align:center; color:white; margin-bottom:20px;'>Welcome Back</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Log In", "Sign Up"])
        with tab1:
            with st.form("login_form"):
                st.markdown("<br>", unsafe_allow_html=True)
                user = st.text_input("Username")
                pw = st.text_input("Password", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("🚀 Log In"):
                    success, user_data = auth.login(user, pw)
                    if success:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = user
                        st.session_state['history'] = user_data.get("history", [])
                        st.success("Login Successful!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        with tab2:
            with st.form("signup_form"):
                st.markdown("<br>", unsafe_allow_html=True)
                new_user = st.text_input("Choose Username")
                new_pw = st.text_input("Choose Password", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("✨ Create Account"):
                    if new_user and new_pw:
                        ok, msg = auth.signup(new_user, new_pw)
                        if ok: st.success(msg)
                        else: st.error(msg)
                    else:
                        st.warning("Please fill all fields")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. MAIN APP ---
def show_main_app():
    try:
        GROQ_KEY = st.secrets["GROQ_KEY"]
        HF_TOKEN = st.secrets["HF_TOKEN"]
    except:
        GROQ_KEY = None; HF_TOKEN = None

    # --- THEME LOGIC (Static Dark Mode) ---
    bg_color = "#050505"
    text_color = "#FAFAFA"
    card_bg = "rgba(255, 255, 255, 0.05)"

    # --- DYNAMIC CSS ---
    st.markdown(f"""
        <style>
            .stApp {{ 
                background-image: none !important;
                background-color: {bg_color} !important; 
                color: {text_color} !important; 
            }}
            header[data-testid="stHeader"] {{ background-color: transparent !important; }}
            div[data-testid="stDecoration"] {{ visibility: hidden; height: 0px; }}
            
            [data-testid="stSidebarCollapsedControl"] {{
                color: {st.session_state['theme_color']} !important;
                background-color: rgba(255, 167, 38, 0.1) !important;
                display: block !important;
                z-index: 999999 !important;
            }}
            [data-testid="stSidebarCollapsedControl"] svg {{
                fill: {st.session_state['theme_color']} !important;
                stroke: {st.session_state['theme_color']} !important;
            }}
            
            [data-testid="stDownloadButton"] button {{
                background-color: {st.session_state['theme_color']} !important;
                color: #000000 !important;
                border: none !important;
                font-weight: bold !important;
            }}
            [data-testid="stDownloadButton"] button:hover {{
                background-color: #FF5722 !important;
                color: #FFFFFF !important;
            }}

            [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
                color: {text_color} !important;
            }}

            div[data-baseweb="select"] > div {{
                background-color: #1E1E1E !important;
                border: 1px solid #333 !important;
                color: {text_color} !important;
            }}
            div[data-baseweb="select"] span {{ color: {text_color} !important; }}
            div[data-baseweb="select"] input {{ caret-color: transparent !important; color: transparent !important; }}
            ul[data-baseweb="menu"] {{ background-color: #1E1E1E !important; border: 1px solid #444 !important; }}
            li[data-baseweb="option"] {{ color: {text_color} !important; }}
            
            div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div {{
                background-color: #1E1E1E !important;
                border: 1px solid #333 !important;
            }}
            div[data-baseweb="input"] > div > input, textarea {{
                color: {text_color} !important;
                -webkit-text-fill-color: {text_color} !important;
                caret-color: {st.session_state['theme_color']} !important;
            }}
            label p {{ color: {text_color} !important; }}

            .glass-card {{
                background: {card_bg}; backdrop-filter: blur(10px);
                border-radius: 16px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.08);
                margin-bottom: 20px;
            }}
            .storage-card {{
                background: rgba(76, 175, 80, 0.1); border: 1px solid #4CAF50;
                border-radius: 12px; padding: 15px; margin-bottom: 15px;
            }}
            .nutri-val {{ font-size: 2.2rem; font-weight: bold; margin-bottom: -5px; line-height: 1; }}
            .nutri-lbl {{ font-size: 0.8rem; color: #AAA; text-transform: uppercase; letter-spacing: 1px;}}
            .ing-alt {{ color: #FF9800 !important; font-weight: bold; font-size: 0.85rem; margin-left: 28px; margin-top: -12px; margin-bottom: 8px; font-style: italic; }}
            .som-title {{ font-family: 'Georgia', serif; font-size: 1.1rem; color: #E91E63; font-weight: bold; }}
            
            h1, h2, h3, h4 {{ color: {st.session_state['theme_color']} !important; text-shadow: none !important; }}
            .stCheckbox label {{ color: {text_color} !important; font-size: 1rem; }}
        </style>
    """, unsafe_allow_html=True)

    styles.load_css(st.session_state['theme_color'])

    components.render_navbar()
    components.render_marquee()

    # SIDEBAR
    with st.sidebar:
        # Sidebar Logo logic
        c_logo, c_title = st.columns([0.4, 0.6])
        with c_logo:
            if os.path.exists("logo.png"):
                st.image("logo.png", use_container_width=True)
        with c_title:
            st.markdown("<h3 style='margin: 0; padding-top: 10px;'>Rasoi AI</h3>", unsafe_allow_html=True)

        # --- THEME COLOR PICKER ONLY ---
        st.markdown("---")
        st.markdown("### 🎨 Personalize")
        st.session_state['theme_color'] = st.color_picker("Brand Accent Color", st.session_state['theme_color'])
        st.markdown("---")

        st.markdown(f"**👤 {st.session_state['username']}**")
        if st.button("Logout", type="secondary"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.markdown("---")
        
        with st.expander("📜 History", expanded=True):
            if not st.session_state['history']:
                st.caption("No recent dishes.")
            else:
                for item in st.session_state['history']:
                    st.markdown(f"**• {item}**")
            
            if len(st.session_state['history']) > 0:
                if st.button("Clear History"): 
                    st.session_state['history'] = []
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 🚨 Kitchen SOS")
        sos_q = st.text_input("Disaster?", placeholder="e.g. Too salty!", label_visibility="collapsed")
        if st.button("🚑 Fix It"):
            if not sos_q: st.warning("Type a problem!")
            else:
                with st.spinner("Analyzing..."):
                    try: fix = ai_engine.get_sos_help(GROQ_KEY, sos_q)
                    except: fix = "Connection Error."
                    st.info(fix)

    # MAIN CONTENT
    col_left, col_right = st.columns([1.4, 1], gap="large")

    with col_left:
        components.render_hero_text()

    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### 🍳 Create your plate")
        
        if GROQ_KEY:
            st.markdown(f"""<div style="background: rgba(76, 175, 80, 0.1); border: 1px solid #4CAF50; color: #4CAF50; padding: 6px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; text-align: center; margin-bottom: 15px;">🟢 SYSTEM ONLINE</div>""", unsafe_allow_html=True)
        
        c_mood, c_serve = st.columns([2, 1])
        with c_mood:
            mood = st.selectbox("Craving / Taste Mood", ["No Preference", "Spicy (Teekha) 🌶️", "Tangy (Chatpata) 🍋", "Crispy 🍟", "Rich 🧀", "Healthy 🥗", "Comforting 🍲", "Sweet 🍬", "Garlicky 🧄", "Smoky 🍖", "Cheesy 🧀", "Buttery 🧈", "Zesty 🍊"])
        with c_serve:
            servings = st.number_input("People 👥", min_value=1, max_value=20, value=2)
        
        input_type = st.radio("Starting with?", ["Raw Ingredients (Pantry)", "Cooked Leftover (Repurpose Dish)"], horizontal=True)
        ingredients = st.text_area("Your Input", height=80, placeholder="e.g. Eggs, Bread, Tomato...")
        
        c1, c2 = st.columns(2)
        with c1: language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French", "German", "Japanese", "Arabic", "Mandarin", "Portuguese", "Russian", "Bengali", "Tamil", "Telugu", "Kannada", "Malayalam", "Marathi", "Gujarati", "Punjabi", "Urdu"])
        with c2: cuisine = st.selectbox("Cuisine", ["Global (Any)", "Indian", "Italian", "Mexican", "Chinese", "Mediterranean", "Thai", "American", "Japanese", "French", "Spanish", "Greek", "Lebanese", "Turkish", "Korean", "Vietnamese", "Middle Eastern", "African", "Caribbean", "Brazilian"])
        
        c3, c4, c5 = st.columns(3)
        with c3: diet = st.selectbox("Diet", ["None", "Vegetarian", "Vegan", "Keto", "Gluten-Free", "High Protein", "Low Carb", "Dairy-Free", "Paleo", "Halal", "Kosher", "Low Fat", "Sugar-Free", "Nut-Free", "Egg-Free"])
        with c4: occasion = st.selectbox("Occasion", ["Daily Meal", "Pre-Workout 💪", "Post-Workout ⚡", "Hangover Core 🤕", "Date Night 🍷", "Sick Day 🍵", "Festival 🎉", "Midnight Craving 🌙", "Tiffin/Lunchbox 🍱", "Birthday Party 🎂", "Potluck 🍲", "Picnic 🧺", "Brunch 🥞", "High Tea ☕", "Road Trip 🚗"])
        with c5: vibe = st.selectbox("Course", ["Dinner", "Lunch", "Breakfast", "Dessert 🍰", "Snack", "Meal Prep (Bulk)", "Cheat Meal 🍔", "Appetizer 🥟", "Soup 🥣", "Salad 🥗", "Beverage 🍹"])
        
        col_a, col_b = st.columns(2)
        with col_a: fireless_mode = st.checkbox("🔥 No Gas Mode", value=False)
        
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("✨ START COOKING", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    container = st.container()

    def check_conflicts(ing_text, selected_vibe):
        savory_triggers = ["garlic", "onion", "chili", "chilli", "brinjal", "curry", "mustard", "cumin", "chicken", "fish", "meat"]
        if "Dessert" in selected_vibe:
            for trigger in savory_triggers:
                if trigger in ing_text.lower(): return True, trigger
        return False, ""

    if generate_btn:
        if not ingredients: st.warning("⚠️ Input is empty!")
        else:
            has_conflict, bad_item = check_conflicts(ingredients, vibe)
            if has_conflict:
                st.session_state['conflict_active'] = True
                st.session_state['conflict_item'] = bad_item
            else:
                st.session_state['conflict_active'] = False
                with container:
                    with st.spinner(f"👨‍🍳 Chef is planning your {occasion}..."):
                        try:
                            data = ai_engine.generate_ai_recipe(
                                GROQ_KEY, HF_TOKEN, ingredients, diet, vibe, cuisine, language, occasion, 
                                mood, True, input_type, fireless_mode, servings
                            )
                            st.session_state['recipe_data'] = data
                            
                            # Update History immediately upon success
                            new_title = data.get('title', 'Unknown Dish')
                            st.session_state['history'].insert(0, new_title)
                            auth.save_recipe_to_history(st.session_state['username'], new_title)
                            
                        except Exception as e:
                            st.error(f"System Error: {str(e)}")

    if st.session_state.get('conflict_active'):
        with container:
            st.markdown(f"""
            <div style="background: rgba(255, 87, 34, 0.15); border: 1px solid #FF5722; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #FF5722; margin-top: 0;">⚠️ Culinary Warning!</h3>
                <p style="color: #EEE; font-size: 1.1rem;">You selected <strong>Dessert</strong>, but ingredients include <strong>"{st.session_state['conflict_item']}"</strong>.</p>
            </div>
            """, unsafe_allow_html=True)
            c_y, c_n = st.columns(2)
            with c_y:
                if st.button("🤢 Continue (Weird Dessert)"):
                    st.session_state['conflict_active'] = False
                    with st.spinner("Processing..."):
                        data = ai_engine.generate_ai_recipe(GROQ_KEY, HF_TOKEN, ingredients, diet, vibe, cuisine, language, occasion, mood, True, input_type, fireless_mode, servings)
                        st.session_state['recipe_data'] = data
                        new_title = data.get('title', 'Unknown Dish')
                        st.session_state['history'].insert(0, new_title)
                        auth.save_recipe_to_history(st.session_state['username'], new_title)
                        st.rerun()
            with c_n:
                if st.button("🍲 Switch to Savory"):
                    st.session_state['conflict_active'] = False
                    with st.spinner("Switching..."):
                        data = ai_engine.generate_ai_recipe(GROQ_KEY, HF_TOKEN, ingredients, diet, "Dinner", cuisine, language, occasion, mood, True, input_type, fireless_mode, servings)
                        st.session_state['recipe_data'] = data
                        new_title = data.get('title', 'Unknown Dish')
                        st.session_state['history'].insert(0, new_title)
                        auth.save_recipe_to_history(st.session_state['username'], new_title)
                        st.rerun()

    if 'recipe_data' in st.session_state and not st.session_state.get('conflict_active'):
        data = st.session_state['recipe_data']
        with container:
            c_title, c_dl = st.columns([3, 1])
            with c_title:
                st.markdown(f"<h1>{data.get('title')}</h1>", unsafe_allow_html=True)
                st.caption(f"💡 {data.get('logic')}")
            with c_dl:
                recipe_txt = f"RECIPE: {data.get('title')}\n\nINGREDIENTS:\n" + "\n".join([f"- {i['item']}" for i in data.get('ingredients_data', [])]) + "\n\nINSTRUCTIONS:\n" + "\n".join([f"{idx+1}. {s['text']}" for idx, s in enumerate(data.get('instructions', []))])
                st.download_button("📥 Download", recipe_txt, file_name=f"{data.get('title')}.txt")

            c_img, c_notes = st.columns([0.8, 1.2])
            with c_img:
                if data.get('image'): st.image(data.get('image'), use_container_width=True)
            with c_notes:
                if data.get('storage_tips'): st.markdown(f"<div class='storage-card'><strong style='color:#4CAF50;'>♻️ Leftover Saver</strong><div style='color:#EEE; margin-top:5px;'>{data.get('storage_tips')}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:12px; border-left:4px solid {st.session_state['theme_color']};'><h4 style='color:{st.session_state['theme_color']}; margin:0;'>👅 Chef's Notes</h4><p style='color:{text_color}; font-style:italic;'>\"{data.get('tasting_notes')}\"</p><div style='color:#4CAF50; font-weight:bold; margin-top:10px;'>PROFILE: {data.get('taste_profile', 'SAVORY').upper()}</div></div>", unsafe_allow_html=True)

            st.markdown("### 📊 Nutrition Per Serving")
            nut = data.get('nutrition', {})
            n1, n2, n3, n4 = st.columns(4)
            with n1: st.markdown(f"<div class='nutri-val' style='color:#4CAF50'>{nut.get('Protein', '0g')}</div><div class='nutri-lbl'>PROTEIN</div>", unsafe_allow_html=True)
            with n2: st.markdown(f"<div class='nutri-val' style='color:#2196F3'>{nut.get('Carbs', '0g')}</div><div class='nutri-lbl'>CARBS</div>", unsafe_allow_html=True)
            with n3: st.markdown(f"<div class='nutri-val' style='color:#FFC107'>{nut.get('Fat', '0g')}</div><div class='nutri-lbl'>FAT</div>", unsafe_allow_html=True)
            with n4: st.markdown(f"<div class='nutri-val' style='color:#FF5722'>{nut.get('Calories', '200')}</div><div class='nutri-lbl'>CALORIES</div>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🍷 Sommelier's Selection")
            bevs = data.get('beverages', [])
            cols = st.columns(4)
            for i in range(4): 
                if i < len(bevs):
                    d = bevs[i]
                    with cols[i]: st.markdown(f"<div style='background:{card_bg}; padding:15px; border-radius:12px;'><div class='som-title'>{d.get('name')}</div><span style='font-size:0.75rem; color:#AAA;'>{d.get('type')}</span><hr style='border-color:rgba(255,255,255,0.1);'><div style='font-size:0.85rem; color:{text_color};'>🥣 {d.get('quick_recipe')}</div></div>", unsafe_allow_html=True)

            st.markdown("---")
            c_ing, c_steps = st.columns([1, 1.5])
            with c_ing:
                st.markdown("### 🛒 Ingredients")
                for item in data.get('ingredients_data', []):
                    has_item = st.checkbox(item['item'], value=True, key=item['item'])
                    if not has_item: st.markdown(f"<div class='ing-alt'>🔄 Try: {item.get('substitute', 'No sub')}</div>", unsafe_allow_html=True)
            with c_steps:
                st.markdown("### 👩‍🍳 Instructions")
                for i, step in enumerate(data.get('instructions', [])):
                    st.markdown(f"<div style='margin-bottom:25px;'><div style='color:{st.session_state['theme_color']}; font-weight:bold;'>Step {i+1}</div><div style='background:{card_bg}; padding:15px; border-radius:8px;'>{step['text']}</div></div>", unsafe_allow_html=True)

# --- APP FLOW CONTROL ---
if st.session_state['logged_in']:
    show_main_app()
else:
    show_login_page()