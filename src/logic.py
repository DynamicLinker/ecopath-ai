
import requests
import google.generativeai as genai
import polyline
import time

class EcoNavigator:
    def __init__(self, gemini_key):
        genai.configure(api_key=gemini_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def get_coordinates(self, location_name):
        url = "https://nominatim.openstreetmap.org/search"
        params = {'q': f"{location_name}", 'format': 'json', 'limit': 1}
        headers = {'User-Agent': 'EcoPath_Project'}
        try:
            time.sleep(1) # Compliance with free-tier rate limits
            res = requests.get(url, params=params, headers=headers, timeout=10).json()
            return (float(res[0]['lat']), float(res[0]['lon'])) if res else None
        except: return None

    def get_aqi_at_coord(self, lat, lng):
        """Simulated pollution levels for Kanpur hotspots."""
        base_aqi = 145
        # Mall Road & Panki Industrial Area hotspots
        if 26.46 < lat < 26.48 and 80.32 < lng < 80.36: base_aqi += 110
        if 26.43 < lat < 26.46 and 80.25 < lng < 80.29: base_aqi += 125
        return base_aqi

    def _process_osrm_response(self, res_json):
        if 'routes' not in res_json: return []
        processed = []
        for r in res_json['routes']:
            points = polyline.decode(r['geometry'])
            segments = []
            total_aqi = 0
            step = max(1, len(points) // 12)
            for j in range(0, len(points) - 1, step):
                seg_pts = points[j : j + step + 1]
                mid = seg_pts[len(seg_pts)//2]
                aqi = self.get_aqi_at_coord(mid[0], mid[1])
                segments.append({"coords": seg_pts, "aqi": aqi})
                total_aqi += aqi
            processed.append({
                "segments": segments,
                "avg_aqi": int(total_aqi / len(segments)),
                "duration": round(r['duration'] / 60, 1)
            })
        return processed

    def get_all_routes(self, start, end):
        """Forces 4 distinct corridors using radial nudging."""
        routes = []
        # Standard Route
        url_std = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=polyline&alternatives=true"
        try: routes.extend(self._process_osrm_response(requests.get(url_std).json()))
        except: pass

        m_lat, m_lng = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        nudges = [(0.018, 0.018), (-0.018, -0.018), (0.018, -0.018), (-0.018, 0.018)]

        for lat_n, lng_n in nudges:
            url_n = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{m_lng+lng_n},{m_lat+lat_n};{end[1]},{end[0]}?overview=full&geometries=polyline"
            try: routes.extend(self._process_osrm_response(requests.get(url_n).json()))
            except: continue

        return sorted(routes, key=lambda x: x['avg_aqi'])


    def get_ai_advice_simple(self, start, end, aqi, is_best=True):
        """Generates path-specific health advice."""
        status = "the healthiest option" if is_best else " a higher-exposure alternative"

        prompt = (
            f"Context: Trip from {start} to {end} in Kanpur. This specific route has an AQI of {aqi} "
            f"and is considered {status}. Provide a 2-sentence health advisory for the commuter."
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return f"Current Route AQI: {aqi}. Please exercise caution in high-traffic zones."
