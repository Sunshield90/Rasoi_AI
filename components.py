import streamlit as st

FALLBACK_IMG = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80"

# Marquee Images
MARQUEE_IMAGES = [
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&q=80",
    "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&q=80",
    "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=400&q=80",
    "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=400&q=80",
    "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=400&q=80",
    "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&q=80",
    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80",
    "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&q=80"
]

def get_theme():
    return st.session_state.get('theme_color', '#FFA726')

def render_navbar():
    c = get_theme()
    st.markdown(f"""<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;"><div style="font-family: 'Outfit', sans-serif; font-size: 28px; font-weight: 800; color: #fff; letter-spacing: -0.5px;">RASOI<span style="color:{c};">.AI</span></div><div style="font-family: 'Outfit', sans-serif; font-size: 11px; letter-spacing: 1.5px; color: #666; text-transform:uppercase;">AI Culinary Engine</div></div>""", unsafe_allow_html=True)

def render_marquee():
    imgs_html = "".join([f'<img src="{url}" class="marquee-item">' for url in MARQUEE_IMAGES])
    st.markdown(f"""<div class="marquee-wrapper"><div class="marquee-content">{imgs_html}{imgs_html}{imgs_html}</div></div>""", unsafe_allow_html=True)

def render_hero_text():
    c = get_theme()
    st.markdown(f"""<div class="hero-container"><div class="hero-bg-img"><img src="https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=1200&q=80" style="width: 100%; border-radius: 50%;"></div><div class="hero-text"><h1 style="font-family: 'Playfair Display', serif; font-weight: 700; font-size: 4rem; line-height: 1.1; margin-bottom: 20px; color: #fff;">Your fridge is full of <br><span style="color: {c}; font-style: italic;">possibilities.</span></h1><p style="font-size: 1.3rem; color: #bbb; line-height: 1.5; font-weight: 400; margin-bottom: 20px;">Tell AI your ingredients, and turn <b>"nothing to eat"</b> into a Michelin-worthy dish.</p></div></div>""", unsafe_allow_html=True)

def render_result(data):
    if not data: return
    c = get_theme()
    title = data.get('title', 'Recipe Ready')
    logic = data.get('logic', 'Custom made for you.')
    time = data.get('time', '15 mins')
    img = data.get('image', FALLBACK_IMG)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<div class="glass-card" style="border-left: 4px solid {c};"><h1 style="margin:0; font-size: 3rem; font-family:'Playfair Display', serif; font-weight: 700;">{title}</h1><p style="color: {c}; font-size: 1.1rem; margin-top: 10px; font-style: italic;">"{logic}"</p><div style="margin-top: 20px;"><span style="background: {c}20; color: {c}; padding: 6px 16px; border-radius: 30px; font-weight: 600; font-size: 0.85rem; border: 1px solid {c}40;">⏱️ {time}</span></div></div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div style="border-radius: 16px; overflow: hidden; margin-bottom: 25px; margin-top: 20px; border:1px solid rgba(255,255,255,0.1);"><img src="{img}" style="width: 100%; display:block;"></div>""", unsafe_allow_html=True)
    
    if 'taste_profile' in data:
        st.markdown(f"""<div class="glass-card" style="background: {c}08; border: 1px solid {c}30;"><div style="display: flex; align-items: flex-start; gap: 20px;"><div style="font-size: 30px; line-height:1;">👅</div><div><h3 style="margin: 0; color: {c}; font-size: 1.5rem; font-family: 'Playfair Display', serif; font-weight: 700;">Chef's Notes</h3><p style="margin: 5px 0 0 0; color: #ccc; font-size: 0.95rem; font-style: italic; line-height:1.5;">"{data.get('tasting_notes', 'Flavorful.')}"</p><div style="margin-top: 10px; font-weight: bold; color: #fff; text-transform: uppercase; letter-spacing: 1px; font-size: 0.8rem;">PROFILE: <span style="color: #81C784;">{data['taste_profile']}</span></div></div></div></div>""", unsafe_allow_html=True)

    # SOMMELIER (4 COLUMNS - UPDATED)
    if 'beverages' in data and data['beverages']:
        st.markdown(f"<h3 style='color:#ff8a80; margin-top:30px; font-family: Playfair Display, serif; font-weight: 700; font-size: 2.2rem;'>🍷 Sommelier's Selection</h3>", unsafe_allow_html=True)
        # Using 4 columns as requested
        cols = st.columns(4)
        for i, drink in enumerate(data['beverages']):
            if i < 4:
                with cols[i]:
                    st.markdown(f"""<div class="glass-card" style="padding: 20px; min-height: 220px;"><div style="font-size: 10px; color: #ff8a80; text-transform: uppercase; letter-spacing: 2px; margin-bottom:10px;">{drink.get('type', 'BEVERAGE')}</div><h3 style="margin: 0 0 10px 0; color: #fff; font-size: 1.4rem; font-family: 'Playfair Display', serif; font-weight: 700;">{drink['name']}</h3><p style="font-size: 0.9rem; color: #aaa; margin-bottom: 15px; line-height: 1.4;">{drink['desc']}</p><div style="padding-top:15px; border-top:1px solid rgba(255,255,255,0.1); font-size: 0.85rem; color: #ddd;"><b>🥣 Mix:</b> {drink.get('quick_recipe', 'Mix and serve.')}</div></div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 INGREDIENTS", "👨‍🍳 PREPARATION"])
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### <span style='font-family: Playfair Display, serif; font-weight: 700;'>🛒 Checklist</span>", unsafe_allow_html=True)
            if 'ingredients_data' in data:
                for idx, item_obj in enumerate(data['ingredients_data']):
                    # SUBSTITUTE LOGIC (KEPT)
                    has_item = st.checkbox(item_obj['item'], value=True, key=f"ing_{idx}")
                    if not has_item:
                        st.markdown(f"""
                        <div style="margin-left: 25px; margin-bottom: 12px; padding: 10px; background: rgba(100, 181, 246, 0.1); border-left: 3px solid #64B5F6; border-radius: 0 8px 8px 0;">
                            <span style="color: #64B5F6; font-size: 0.8rem; font-weight: bold; text-transform:uppercase;">Substitute</span><br>
                            <span style="color: #e0e0e0; font-size: 0.95rem;">{item_obj['substitute']}</span>
                        </div>
                        """, unsafe_allow_html=True)
        with c2:
            st.markdown("### <span style='font-family: Playfair Display, serif; font-weight: 700;'>📊 Nutrition</span>", unsafe_allow_html=True)
            if 'nutrition' in data:
                n = data['nutrition']
                cols = st.columns(3)
                cols[0].markdown(f"""<div class="nutri-box"><div class="nutri-val">{n.get('Protein','?')}</div><div class="nutri-lbl">PRO</div></div>""", unsafe_allow_html=True)
                cols[1].markdown(f"""<div class="nutri-box"><div class="nutri-val">{n.get('Carbs','?')}</div><div class="nutri-lbl">CARB</div></div>""", unsafe_allow_html=True)
                cols[2].markdown(f"""<div class="nutri-box"><div class="nutri-val">{n.get('Fat','?')}</div><div class="nutri-lbl">FAT</div></div>""", unsafe_allow_html=True)
            
            if 'storage' in data and data['storage']:
                 st.markdown(f"""<div style="margin-top:30px; padding:20px; background:rgba(129, 199, 132, 0.1); border: 1px solid #81C784; border-radius:16px;"><div style="color:#81C784; font-weight:800; font-size:1.2rem; margin-bottom:8px; text-transform:uppercase;">♻️ Leftover Saver</div><div style="color:#ccc; font-size:1.1rem; line-height:1.6;">{data['storage']}</div></div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        if 'instructions' in data:
            for i, step in enumerate(data['instructions']):
                c_img, c_txt = st.columns([1, 2])
                with c_img:
                    img_url = step.get('image_url') or FALLBACK_IMG
                    st.image(img_url, use_container_width=True)
                with c_txt:
                    st.markdown(f"""<div style="border-left: 2px solid {c}40; padding-left: 25px; height: 100%; display: flex; flex-direction: column; justify-content: center;"><h3 style="color: {c}; margin: 0; font-size: 1.2rem; font-family:'Outfit';">STEP {i+1}</h3><p style="color: #ddd; margin-top: 8px; font-size: 1.1rem; line-height: 1.6;">{step['text']}</p></div>""", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)