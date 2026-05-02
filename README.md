# 🌱 EcoPath AI
### **Smart Urban Resource Allocation & Health-Centric Navigation**
*Ensuring the shortest path isn't a shortcut to poor health.*

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://ecopath.streamlit.app)
[![Python 3.13](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Google Cloud](https://img.shields.io/badge/Google-Gemini-yellow?style=for-the-badge&logo=google)](https://aistudio.google.com/)

### Live Deployment : [EcoPath](https://ecopath.streamlit.app)

---

## 📌 Overview
**EcoPath AI** is an intelligent routing and urban load-balancing engine designed for the **Google Solution Challenge 2026**. Standard navigation apps are "health-blind"—they funnel 100% of traffic into single shortest paths, creating toxic pollution hotspots. 

EcoPath AI treats road networks as dynamic health assets. By redistributing traffic across cleaner corridors, the system aims to solve **SDG 3 (Good Health & Well-being)** and **SDG 11 (Sustainable Cities & Communities)**, potentially reducing individual respiratory risk by up to **75%** in industrial clusters like Kanpur.

## 🧠 The Discrete Logic Engine
The system processes navigation through a modular, seven-stage data pipeline:

1.  **Coordinate Acquisition:** Converts user input into precise Lat/Long pairs via **Nominatim API**.
2.  **Corridor Generation:** Uses the **OSRM engine** to identify four distinct geographic corridors through the city.
3.  **Sensing Data Fusion:** Fetches real-time AQI and PM2.5 data from **OpenAQ** for every road segment (Step).
4.  **Risk Engine:** Calculates the path-level "Respiratory Cost" using segment-by-segment summation:
    $$Total Cost = \sum(AQI \times Segment Distance)$$
5.  **Comparative Ranking:** Identifies and ranks the "Green Path" vs. the traditional "Fast Path".
6.  **AI Health Reasoning:** Employs **Google Gemini 3 Flash** to transform raw pollutant metrics into conversational, path-specific health advisories.
7.  **Dynamic Rendering:** Deploys a **Streamlit** dashboard for real-time map interaction and "Healthy Nudges".

## 🛠️ Tech Stack
*   **AI Core:** Google Gemini 3 Flash API.
*   **Language:** Python 3.13.
*   **Environment:** OpenSUSE Tumbleweed (Linux).
*   **GIS & Mapping:** OSRM, OpenStreetMap, Geopy (Nominatim), and Folium.
*   **Deployment:** Streamlit Cloud with GitHub CI/CD.

## 🚀 Getting Started

### Installation
1.  **Clone the repository:**
```sh
git clone https://github.com/DynamicLinker/ecopath-ai.git
cd ecopath-ai
```
2. **Install dependencies:**
```sh
pip install -r requirements.txt
```

3. **Configure API Key:**
> Create a .env file and add your Google AI Studio key:
```
api_key=YOUR_GEMINI_API_KEY
```

4. **Launch the Dashboard:**
```sh
streamlit run app.py
```


___
👨‍💻 Developer

Ajitesh Chaurasia

B.Tech Computer Science & Engineering



---
Developed for the Google Solution Challenge 2026.
