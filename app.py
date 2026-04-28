import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_folium import st_folium
import folium
from src.logic import EcoNavigator

load_dotenv()
api_key = os.getenv('api_key')

st.set_page_config(
    page_title="EcoPath AI | Kanpur Health Navigator",
    page_icon="🌱",
    layout="wide"
)

# Initialize memory to minimize Gemini API calls
if "selected_idx" not in st.session_state:
    st.session_state.selected_idx = 0
if "route_insights" not in st.session_state:
    st.session_state.route_insights = {}

with st.sidebar:
    st.title("EcoPath AI")
    st.caption("Active Urban Load Balancing & Health Navigation")

    if api_key:
        st.success("✅ Google Gemini Connected")
    else:
        st.error("❌ GEMINI_API_KEY Missing in .env")

    st.divider()
    o_name = st.text_input("Start Location", placeholder="e.g., HBTU")
    d_name = st.text_input("Destination", placeholder="e.g., Moti Jheel")

    if st.button("🚀 Find Healthiest Paths"):
        if api_key and o_name and d_name:
            # Clear previous trip memory
            st.session_state.route_insights = {}
            st.session_state.selected_idx = 0
            st.session_state.calculate = True
        else:
            st.warning("Please enter both locations to begin.")

def get_dynamic_insight(idx):
    if idx not in st.session_state.route_insights:
        nav = EcoNavigator(api_key)
        route = st.session_state.routes[idx]

        with st.spinner(f"Gemini is analyzing the health profile of Route {idx}..."):
            is_best = (idx == 0)
            new_insight = nav.get_ai_advice_simple(
                st.session_state.names[0],
                st.session_state.names[1],
                route['avg_aqi'],
                is_best=is_best
            )
            st.session_state.route_insights[idx] = new_insight

    return st.session_state.route_insights[idx]

if st.session_state.get("calculate"):
    nav = EcoNavigator(api_key)
    with st.spinner("Geocoding and analyzing city pollution corridors..."):
        s_coords = nav.get_coordinates(o_name)
        e_coords = nav.get_coordinates(d_name)

        if s_coords and e_coords:
            routes = nav.get_all_routes(s_coords, e_coords)
            if routes:
                st.session_state.update({
                    "routes": routes,
                    "s_coords": s_coords,
                    "names": (o_name, d_name),
                    "calculate": False
                })
            else:
                st.error("No valid driving paths found."); st.session_state.calculate = False
        else:
            st.error("Location not found."); st.session_state.calculate = False

if "routes" in st.session_state:
    routes = st.session_state.routes

    # Lazy-load advice for the currently selected path
    current_insight = get_dynamic_insight(st.session_state.selected_idx)
    sel_route = routes[st.session_state.selected_idx]

    # Metrics Row
    st.write(f"### 📍 Journey Analysis: {st.session_state.names[0]} to {st.session_state.names[1]}")
    c1, c2, c3 = st.columns([1, 1, 2])
    c1.metric("Selected Path AQI", f"{sel_route['avg_aqi']}")
    c2.metric("Estimated Time", f"{sel_route['duration']}m")
    c3.info(f"🤖 **AI Advisory:** {current_insight}")

    # Map Rendering
    m = folium.Map(location=st.session_state.s_coords, zoom_start=13)

    # DRAW ALL PATHS (Layered: Alternatives first, Selected last)
    for i, r in enumerate(routes):
        is_active = (i == st.session_state.selected_idx)

        l_weight = 8 if is_active else 4
        l_opacity = 1.0 if is_active else 0.3

        # Color coding: Gray for background, Green/Red for selected
        if is_active:
            l_color = "#2ecc71" if r['avg_aqi'] < 165 else "#e74c3c"
        else:
            l_color = "#4b7bab"

        pts = [p for seg in r['segments'] for p in seg['coords']]
        folium.PolyLine(
            pts, color=l_color, weight=l_weight, opacity=l_opacity,
            tooltip=f"Route {i}", popup=f"AQI: {r['avg_aqi']}"
        ).add_to(m)

    # Start Marker
    folium.Marker(st.session_state.s_coords, icon=folium.Icon(color='green', icon='play')).add_to(m)

    map_data = st_folium(m, width=1200, height=550, key="eco_map")

    # Change selection if a different line's tooltip was clicked
    if map_data and map_data.get("last_object_clicked_tooltip"):
        tooltip = map_data["last_object_clicked_tooltip"]
        if "Route " in tooltip:
            new_idx = int(tooltip.replace("Route ", ""))
            if new_idx != st.session_state.selected_idx:
                st.session_state.selected_idx = new_idx
                st.rerun() # Refresh to update the 'brightest' line and AI advice

else:
    # Landing Page
    st.write("---")
    st.info("👋 Enter your journey details to visualize the healthiest path through Kanpur.")
    st.caption(f"Developed by Ajitesh Chaurasia (PSIT Kanpur) for the Google Solution Challenge 2026.")
