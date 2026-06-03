import re
import math
import pandas as pd
import numpy as np
from .geo_features import (
    get_distance_to_metro,
    get_geo_features
)

# -----------------------------------
# LOCATION MAP
# -----------------------------------
location_MAP = {
    # ==========================================
    # TIER 10
    # ==========================================
    "alipore": "Alipore",
    "ballygunge": "Ballygunge",
    "park street": "Park Street",
    "parkstreet": "Park Street",
    "elgin road": "Elgin Road",
    "elginroad": "Elgin Road",
    "minto park": "Minto Park",
    "mintopark": "Minto Park",
    "camac street": "Camac Street",
    "camacstreet": "Camac Street",
    "loudon street": "Loudon Street",
    "loudonstreet": "Loudon Street",
    "ballygunge circular road": "Ballygunge Circular Road",
    "ballygunge circular rd": "Ballygunge Circular Road",
    "ballygungecircularroad": "Ballygunge Circular Road",
    "salt lake": "Salt Lake",
    "saltlake": "Salt Lake",

    # ==========================================
    # TIER 9
    # ==========================================
    "new alipore": "New Alipore",
    "newalipore": "New Alipore",
    "bhowanipore": "Bhowanipore",
    "bhowanipur": "Bhowanipore",
    "rash behari avenue": "Rash Behari Avenue",
    "rashbehari avenue": "Rash Behari Avenue",
    "rashbehariavenue": "Rash Behari Avenue",
    "lake market": "Lake Market",
    "lakemarket": "Lake Market",
    "gariahat": "Gariahat",
    "prince anwar shah road": "Prince Anwar Shah Road",
    "prince anwar shah rd": "Prince Anwar Shah Road",
    "anwar shah road": "Prince Anwar Shah Road",
    "em bypass": "EM Bypass",
    "em by pass": "EM Bypass",
    "science city area": "Science City Area",
    "science city": "Science City Area",
    "kalighat": "Kalighat",
    "golpark": "Golpark",
    "gol park": "Golpark",
    "foreshore road": "Foreshore Road",
    "foreshoreroad": "Foreshore Road",

    # ==========================================
    # TIER 8
    # ==========================================
    "new town": "New Town",
    "newtown": "New Town",
    "salt lake sector v": "Salt Lake Sector V",
    "salt lake sector 5": "Salt Lake Sector V",
    "sector v": "Salt Lake Sector V",
    "sector 5": "Salt Lake Sector V",
    "shankhmani": "Shankhmani",
    "newtown action area 3": "Shankhmani",
    "newtown aa3": "Shankhmani",
    "action area 3": "Shankhmani",
    "kankurgachi": "Kankurgachi",
    "kankurgachhi": "Kankurgachi",
    "bidhan nagar": "Bidhan Nagar",
    "bidhannagar": "Bidhan Nagar",
    "dhakuria": "Dhakuria",
    "chakgaria": "Chakgaria",
    "chak garia": "Chakgaria",
    "golf green": "Golf Green",
    "golfgreen": "Golf Green",
    "santoshpur": "Santoshpur",
    "chingrighata": "Chingrighata",
    "chingrihata": "Chingrighata",

    # ==========================================
    # TIER 7
    # ==========================================
    "tollygunge": "Tollygunge",
    "tollygunj": "Tollygunge",
    "tolly": "Tollygunge",
    "jadavpur": "Jadavpur",
    "jadabpur": "Jadavpur",
    "kasba": "Kasba",
    "ruby connector": "Ruby Connector",
    "rubyconnector": "Ruby Connector",
    "anandapur": "Anandapur",
    "anandpur": "Anandapur",
    "phoolbagan": "Phoolbagan",
    "phool bagan": "Phoolbagan",
    "lake town": "Lake Town",
    "laketown": "Lake Town",
    "bangur avenue": "Bangur Avenue",
    "bangur": "Bangur Avenue",
    "banguravenue": "Bangur Avenue",
    "shyambazar": "Shyambazar",
    "shyam bazar": "Shyambazar",
    "hatibagan": "Hatibagan",
    "hati bagan": "Hatibagan",
    "sealdah": "Sealdah",
    "sealdha": "Sealdah",
    "panchasayer": "Panchasayer",
    "pancha sayer": "Panchasayer",
    "shibpur": "Shibpur",
    "sibpur": "Shibpur",

    # ==========================================
    # TIER 6
    # ==========================================
    "beleghata": "Beleghata",
    "beliaghata": "Beleghata",
    "chetla": "Chetla",
    "maniktala": "Maniktala",
    "manicktala": "Maniktala",
    "ultadanga": "Ultadanga",
    "ultadanga more": "Ultadanga",
    "mukundapur": "Mukundapur",
    "mukundpur": "Mukundapur",
    "patuli": "Patuli",
    "baishnabghata patuli": "Patuli",
    "haltu": "Haltu",
    "garfa": "Garfa",
    "tangra": "Tangra",
    "topsia": "Topsia",
    "chinar park": "Chinar Park",
    "chinarpark": "Chinar Park",
    "chinar park crossroad": "Chinar Park Crossroad",
    "chinar park crossing": "Chinar Park Crossroad",
    "vip nagar": "VIP Nagar",
    "vipnagar": "VIP Nagar",
    "kestopur": "Kestopur",
    "keshtopur": "Kestopur",
    "baguiati": "Baguiati",
    "baguiati more": "Baguiati",
    "teghoria": "Teghoria",
    "teghoria more": "Teghoria",
    "haldiram": "Haldiram",
    "haldirams": "Haldiram",
    "kaikhali": "Kaikhali",
    "kalikapur": "Kalikapur",
    "ramrajatala": "Ramrajatala",
    "ramrajatola": "Ramrajatala",

    # ==========================================
    # TIER 5
    # ==========================================
    "rajarhat": "Rajarhat",
    "behala": "Behala",
    "garia": "Garia",
    "garia station area": "Garia Station Area",
    "garia station": "Garia Station Area",
    "kamalgazi": "Kamalgazi",
    "kamalgachhi": "Kamalgazi",
    "bansdroni": "Bansdroni",
    "bansduni": "Bansdroni",
    "kudghat": "Kudghat",
    "regent park": "Regent Park",
    "regentpark": "Regent Park",
    "naktala": "Naktala",
    "baghajatin": "Baghajatin",
    "bagha jatin": "Baghajatin",
    "picnic garden": "Picnic Garden",
    "picnicgarden": "Picnic Garden",
    "intally": "Intally",
    "entally": "Intally",
    "tiljala": "Tiljala",
    "parnasree pally": "Parnasree Pally",
    "parnasree": "Parnasree Pally",
    "haridevpur": "Haridevpur",
    "bijoygarh": "Bijoygarh",
    "bijoygarh area": "Bijoygarh",
    "paikpara": "Paikpara",
    "chiria more": "Chiria More",
    "chiriapore": "Chiria More",
    "sinthi more": "Sinthi More",
    "shinthi more": "Sinthi More",
    "nagerbazar": "Nagerbazar",
    "nager bazar": "Nagerbazar",
    "amherst street area": "Amherst Street Area",
    "amherst street": "Amherst Street Area",
    "gora bazar": "Gora Bazar",
    "gorabazar": "Gora Bazar",
    "airport area": "Airport Area",
    "kolkata airport": "Airport Area",
    "jessore road (airport side)": "Jessore Road",
    "jessore road airport": "Jessore Road",
    "kavi nazrul (metro periphery)": "Kavi Nazrul",
    "kavi nazrul metro": "Kavi Nazrul",
    "goria bazar metro": "Kavi Nazrul",
    "howrah": "Howrah",
    "howrah station": "Howrah",
    "kadamtala": "Kadamtala",
    "baranagar": "Baranagar",
    "barahanagar": "Baranagar",

    # ==========================================
    # TIER 4
    # ==========================================
    "thakurpukur": "Thakurpukur",
    "sarsuna": "Sarsuna",
    "taratala": "Taratala",
    "cossipore": "Cossipore",
    "kashipur": "Cossipore",
    "dum dum": "Dum Dum",
    "dumdum": "Dum Dum",
    "nayabad": "Nayabad",
    "narendrapur": "Narendrapur",
    "mahamayatala": "Mahamayatala",
    "mahamaya tala": "Mahamayatala",
    "ukhila": "Ukhila",
    "joka": "Joka",
    "pailan": "Pailan",
    "madhyamgram": "Madhyamgram",
    "madhyamgram chowmatha": "Madhyamgram Chowmatha",
    "madhyamgram chowrasta": "Madhyamgram Chowmatha",
    "barasat": "Barasat",
    "michael nagar": "Michael Nagar",
    "michaelnagar": "Michael Nagar",
    "new barrackpore": "New Barrackpore",
    "new barrackpur": "New Barrackpore",
    "birati": "Birati",
    "hridaypur": "Hridaypur",
    "hridoypur": "Hridaypur",
    "sodepur road madhyamgram": "Sodepur",
    "sodepur": "Sodepur",
    "sodepur road": "Sodepur",
    "belgharia": "Belgharia",
    "belghoria": "Belgharia",
    "agarpara": "Agarpara",
    "panihati": "Panihati",
    "kamarhati": "Kamarhati",
    "ariadaha": "Ariadaha",
    "dakshineswar": "Dakshineswar",
    "dakshineswar area": "Dakshineswar",
    "satgachhi": "Satgachhi",
    "satgachi": "Satgachhi",
    "jawpur": "Jawpur",
    "batanagar": "Batanagar",
    "maheshtala": "Maheshtala",
    "mahestala": "Maheshtala",
    "santragachi": "Santragachi",
    "santragachhi": "Santragachi",
    "shalimar": "Shalimar",
    "liluah": "Liluah",
    "salkia": "Salkia",
    "dasnagar": "Dasnagar",
    "ichapur (howrah)": "Ichapur (Howrah)",
    "ichapur howrah": "Ichapur (Howrah)",
    "uttarpara": "Uttarpara",
    "konnagar": "Konnagar",
    "serampore": "Serampore",
    "shrirampur": "Serampore",
    "serampore riverfront": "Serampore Riverfront",
    "makhla": "Makhla",
    "nabagram": "Nabagram",

    # ==========================================
    # TIER 3
    # ==========================================
    "sonarpur": "Sonarpur",
    "rajpur": "Rajpur",
    "harinavi": "Harinavi",
    "boral": "Boral",
    "elachi": "Elachi",
    "subhasgram": "Subhasgram",
    "subhas gram": "Subhasgram",
    "mallikpur": "Mallikpur",
    "nangi": "Nangi",
    "barrackpore": "Barrackpore",
    "barrackpur": "Barrackpore",
    "nona chandanpukur": "Nona Chandanpukur",
    "chandanpukur": "Nona Chandanpukur",
    "khardah": "Khardah",
    "khardah area": "Khardah",
    "titagarh": "Titagarh",
    "shyamnagar": "Shyamnagar",
    "mourigram": "Mourigram",
    "andul": "Andul",
    "kona expressway corridor": "Kona Expressway Corridor",
    "kona expressway": "Kona Expressway Corridor",
    "bankra": "Bankra",
    "hindmotor": "Hindmotor",
    "hind motor": "Hindmotor",
    "rishra": "Rishra",
    "baidyabati": "Baidyabati",
    "sheoraphuli": "Sheoraphuli",
    "sheoraphuly": "Sheoraphuli",
    "chandannagar": "Chandannagar",
    "chandannagore": "Chandannagar",
    "mankundu": "Mankundu",
    "chinsurah": "Chinsurah",
    "chuchura": "Chinsurah",
    "chinsurah raghunathpur": "Chinsurah Raghunathpur",
    "bandel": "Bandel",
    "kalyani expressway corridor": "Kalyani Expressway Corridor",
    "kalyani expressway": "Kalyani Expressway Corridor",

    # ==========================================
    # TIER 2
    # ==========================================
    "baruipur": "Baruipur",
    "govindapur (south)": "Govindapur (South)",
    "govindapur south": "Govindapur (South)",
    "langalberia": "Langalberia",
    "amtala": "Amtala",
    "bishnupur (south)": "Bishnupur (South)",
    "bishnupur south": "Bishnupur (South)",
    "budge budge": "Budge Budge",
    "budgebudge": "Budge Budge",
    "naihati": "Naihati",
    "kanchrapara": "Kanchrapara",
    "halisahar": "Halisahar",
    "badu": "Badu",
    "badu road (barasat)": "Badu Road (Barasat)",
    "badu road": "Badu Road (Barasat)",
    "nilganj": "Nilganj",
    "laskarhat": "Laskarhat",
    "domjur": "Domjur",
    "nibra": "Nibra",
    "salap": "Salap",
    "ankurhati": "Ankurhati",
    "lilua (jalan industrial complex area)": "Lilua (Jalan Industrial Complex Area)",
    "jalan industrial complex": "Lilua (Jalan Industrial Complex Area)",
    "bally durgapur": "Bally Durgapur",
    "bally": "Bally",
    "belur": "Belur",
    "sankrail": "Sankrail",
    "dankuni": "Dankuni",
    "dankuni housing complex area": "Dankuni Housing Complex Area",
    "dankuni housing complex": "Dankuni Housing Complex Area",
    "raghunathpur (hooghly)": "Raghunathpur (Hooghly)",
    "raghunathpur hooghly": "Raghunathpur (Hooghly)",
    "baigachhi": "Baigachhi",
    "telenipara": "Telenipara",
    "sugandha": "Sugandha",
    "delhi road corridor (hooghly)": "Delhi Road Corridor (Hooghly)",
    "delhi road hooghly": "Delhi Road Corridor (Hooghly)",
    "delhi road": "Delhi Road Corridor (Hooghly)",
    "bantala (it sez area)": "Bantala (IT SEZ Area)",
    "bantala": "Bantala (IT SEZ Area)",
    "hatisala": "Hatisala",
    "nandakumarpur / diamond harbour rd": "Nandakumarpur / Diamond Harbour Rd",
    "diamond harbour road": "Nandakumarpur / Diamond Harbour Rd",

    # ==========================================
    # TIER 1
    # ==========================================
    "habra": "Habra",
    "ashoknagar": "Ashoknagar",
    "dutta pukur": "Dutta Pukur",
    "duttapukur": "Dutta Pukur",
    "ghatakpukur (basanti highway)": "Ghatakpukur (Basanti Highway)",
    "ghatakpukur": "Ghatakpukur (Basanti Highway)",
    "basanti highway": "Ghatakpukur (Basanti Highway)",
    "bhangar": "Bhangar",
    "champahati": "Champahati",
    "sirakol": "Sirakol",
    "uluberia": "Uluceria",
    "bagnan": "Bagnan",
    "singur": "Singur"
}

# -----------------------------------
# PRICE CLEANING
# -----------------------------------
def clean_price(price):

    if not isinstance(price, str):
        return None

    price = price.replace(",", "").strip()

    try:
        if "Cr" in price:
            num = float(re.findall(r"\d+\.?\d*", price)[0])
            return int(num * 10000000)

        elif "Lac" in price:
            num = float(re.findall(r"\d+\.?\d*", price)[0])
            return int(num * 100000)

    except Exception:
        return None

    return None


# -----------------------------------
# AREA EXTRACTION
# -----------------------------------
def extract_sqft(area):

    if not isinstance(area, str):
        return None

    match = re.search(r"(\d+)\s*sqft", area.lower())

    if match:
        return int(match.group(1))

    return None


# -----------------------------------
# LOCATION EXTRACTION
# -----------------------------------
def extract_location(text):

    if not isinstance(text, str):
        return None

    text = text.lower()

    for key, value in location_MAP.items():
        if key in text:
            return value

    return None


# -----------------------------------
# LOCATION SCORE
# -----------------------------------
def get_location_score(location):

    scores = {
        # ==========================================
        # TIER 10: ULTRA LUXURY & PRIME COMMERCIAL CORRIDORS (> ₹12,500/sq.ft)
        # ==========================================
        "Alipore": 10,
        "Ballygunge": 10,
        "Park Street": 10,
        "Elgin Road": 10,
        "Minto Park": 10,
        "Camac Street": 10,
        "Loudon Street": 10,
        "Ballygunge Circular Road": 10,
        "Salt Lake": 10,

        # ==========================================
        # TIER 9: HIGH-END POSH CORE (₹10,000 - ₹12,500/sq.ft)
        # ==========================================
        "New Alipore": 9,
        "Bhowanipore": 9,
        "Rash Behari Avenue": 9,
        "Lake Market": 9,
        "Gariahat": 9,
        "Prince Anwar Shah Road": 9,
        "EM Bypass": 9,
        "Science City Area": 9,
        "Kalighat": 9,
        "Golpark": 9,
        "Foreshore Road": 9,

        # ==========================================
        # TIER 8: PREMIUM INNER SUBURBS & TECH HUBS (₹8,500 - ₹10,000/sq.ft)
        # ==========================================
        "New Town": 8,
        "Salt Lake Sector V": 8,
        "Shankhmani": 8,
        "Kankurgachi": 8,
        "Bidhan Nagar": 8,
        "Dhakuria": 8,
        "Chakgaria": 8,
        "Golf Green": 8,
        "Santoshpur": 8,
        "Chingrighata": 8,

        # ==========================================
        # TIER 7: ESTABLISHED MODERN NODES (₹7,000 - ₹8,500/sq.ft)
        # ==========================================
        "Tollygunge": 7,
        "Jadavpur": 7,
        "Kasba": 7,
        "Ruby Connector": 7,
        "Anandapur": 7,
        "Phoolbagan": 7,
        "Lake Town": 7,
        "Bangur Avenue": 7,
        "Shyambazar": 7,
        "Hatibagan": 7,
        "Sealdah": 7,
        "Panchasayer": 7,
        "Shibpur": 7,

        # ==========================================
        # TIER 6: MID-MARKET CORE & PRIME COMMUTER LOCALITIES (₹6,000 - ₹7,000/sq.ft)
        # ==========================================
        "Beleghata": 6,
        "Chetla": 6,
        "Maniktala": 6,
        "Ultadanga": 6,
        "Mukundapur": 6,
        "Patuli": 6,
        "Haltu": 6,
        "Garfa": 6,
        "Tangra": 6,
        "Topsia": 6,
        "Chinar Park": 6,
        "Chinar Park Crossroad": 6,
        "VIP Nagar": 6,
        "Kestopur": 6,
        "Baguiati": 6,
        "Teghoria": 6,
        "Haldiram": 6,
        "Kaikhali": 6,
        "Kalikapur": 6,
        "Ramrajatala": 6,

        # ==========================================
        # TIER 5: POPULAR URBAN POCKETS & TRANSIT HUBS (₹5,000 - ₹6,000/sq.ft)
        # ==========================================
        "Rajarhat": 5,
        "Behala": 5,
        "Garia": 5,
        "Garia Station Area": 5,
        "Kamalgazi": 5,
        "Bansdroni": 5,
        "Kudghat": 5,
        "Regent Park": 5,
        "Naktala": 5,
        "Baghajatin": 5,
        "Picnic Garden": 5,
        "Intally": 5,
        "Tiljala": 5,
        "Parnasree Pally": 5,
        "Haridevpur": 5,
        "Bijoygarh": 5,
        "Paikpara": 5,
        "Chiria More": 5,
        "Sinthi More": 5,
        "Nagerbazar": 5,
        "Amherst Street Area": 5,
        "Gora Bazar": 5,
        "Airport Area": 5,
        "Jessore Road": 5,
        "Kavi Nazrul": 5,
        "Howrah": 5,
        "Kadamtala": 5,
        "Baranagar": 5,

        # ==========================================
        # TIER 4: AFFORDABLE CITY CORE & GROWING SUBURBS (₹4,200 - ₹5,000/sq.ft)
        # ==========================================
        "Thakurpukur": 4,
        "Sarsuna": 4,
        "Taratala": 4,
        "Cossipore": 4,
        "Dum Dum": 4,
        "Nayabad": 4,
        "Narendrapur": 4,
        "Mahamayatala": 4,
        "Ukhila": 4,
        "Joka": 4,
        "Pailan": 4,
        "Madhyamgram": 4,
        "Madhyamgram Chowmatha": 4,
        "Barasat": 4,
        "Michael Nagar": 4,
        "New Barrackpore": 4,
        "Birati": 4,
        "Hridaypur": 4,
        "Sodepur": 4,
        "Belgharia": 4,
        "Agarpara": 4,
        "Panihati": 4,
        "Kamarhati": 4,
        "Ariadaha": 4,
        "Dakshineswar": 4,
        "Satgachhi": 4,
        "Jawpur": 4,
        "Batanagar": 4,
        "Maheshtala": 4,
        "Santragachi": 4,
        "Shalimar": 4,
        "Liluah": 4,
        "Salkia": 4,
        "Dasnagar": 4,
        "Ichapur (Howrah)": 4,
        "Uttarpara": 4,
        "Konnagar": 4,
        "Serampore": 4,
        "Serampore Riverfront": 4,
        "Makhla": 4,
        "Nabagram": 4,

        # ==========================================
        # TIER 3: SUBURBAN RAIL CORRIDORS & EXTENDED GROWTH PATHS (₹3,500 - ₹4,200/sq.ft)
        # ==========================================
        "Sonarpur": 3,
        "Rajpur": 3,
        "Harinavi": 3,
        "Boral": 3,
        "Elachi": 3,
        "Subhasgram": 3,
        "Mallikpur": 3,
        "Nangi": 3,
        "Barrackpore": 3,
        "Nona Chandanpukur": 3,
        "Khardah": 3,
        "Titagarh": 3,
        "Shyamnagar": 3,
        "Mourigram": 3,
        "Andul": 3,
        "Kona Expressway Corridor": 3,
        "Bankra": 3,
        "Hindmotor": 3,
        "Rishra": 3,
        "Baidyabati": 3,
        "Sheoraphuli": 3,
        "Chandannagar": 3,
        "Mankundu": 3,
        "Chinsurah": 3,
        "Chinsurah Raghunathpur": 3,
        "Bandel": 3,
        "Kalyani Expressway Corridor": 3,

        # ==========================================
        # TIER 2: MAJOR INDUSTRIAL-RESIDENTIAL MIX HUBS (₹2,800 - ₹3,500/sq.ft)
        # ==========================================
        "Baruipur": 2,
        "Govindapur (South)": 2,
        "Langalberia": 2,
        "Amtala": 2,
        "Bishnupur (South)": 2,
        "Budge Budge": 2,
        "Naihati": 2,
        "Kanchrapara": 2,
        "Halisahar": 2,
        "Badu": 2,
        "Badu Road (Barasat)": 2,
        "Nilganj": 2,
        "Laskarhat": 2,
        "Domjur": 2,
        "Nibra": 2,
        "Salap": 2,
        "Ankurhati": 2,
        "Lilua (Jalan Industrial Complex Area)": 2,
        "Bally Durgapur": 2,
        "Bally": 2,
        "Belur": 2,
        "Sankrail": 2,
        "Dankuni": 2,
        "Dankuni Housing Complex Area": 2,
        "Raghunathpur (Hooghly)": 2,
        "Baigachhi": 2,
        "Telenipara": 2,
        "Sugandha": 2,
        "Delhi Road Corridor (Hooghly)": 2,
        "Bantala (IT SEZ Area)": 2,
        "Hatisala": 2,
        "Nandakumarpur / Diamond Harbour Rd": 2,

        # ==========================================
        # TIER 1: PERIPHERAL HORIZONS & PRIMARY INVESTMENT HORIZONS (< ₹2,800/sq.ft)
        # ==========================================
        "Habra": 1,
        "Ashoknagar": 1,
        "Dutta Pukur": 1,
        "Ghatakpukur (Basanti Highway)": 1,
        "Bhangar": 1,
        "Champahati": 1,
        "Sirakol": 1,
        "Uluberia": 1,
        "Bagnan": 1,
        "Singur": 1
    }

    return scores.get(location, 0)


# -----------------------------------
# LIVABILITY SCORE
# -----------------------------------
def compute_livability(row):

    distances = [
        row["metro_distance_km"],
        row["railway_distance_km"],
        row["bus_stop_distance_km"],
        row["hospital_distance_km"],
        row["school_distance_km"],
        row["college_distance_km"],
        row["police_distance_km"],
        row["postoffice_distance_km"],
    ]

    distances = [
        d for d in distances
        if d is not None and not math.isnan(d)
    ]

    if not distances:
        return 0

    avg_dist = sum(distances) / len(distances)

    score = 10 * (1 / (1 + avg_dist / 2))

    return round(score, 2)


# -----------------------------------
# MAIN CLEANER
# -----------------------------------
def clean_data(df):

    df["price"] = df["price"].apply(clean_price)
    df["sqft"] = df["area"].apply(extract_sqft)
    df["location"] = df["location_text"].apply(extract_location)

    geo_data = df["location"].apply(get_geo_features)

    geo_df = pd.DataFrame(list(geo_data))

    df = pd.concat(
        [df.reset_index(drop=True),
        geo_df.reset_index(drop=True)],
        axis=1
    )

    # Keep only valid locations
    df = df.dropna(
        subset=[
            "price",
            "sqft",
            "location"
        ]
    )

    # Temporary geo placeholders
#    df["metro_distance_km"] = 5
#    df["hospital_distance_km"] = 5
#    df["school_distance_km"] = 5
#    df["college_distance_km"] = 5
#    df["bus_stop_distance_km"] = 5
#    df["railway_distance_km"] = 5
#    df["police_distance_km"] = 5
#    df["postoffice_distance_km"] = 5
#
    df["location_score"] = df["location"].apply(
        get_location_score
    )

    df["livability_score"] = df.apply(
        compute_livability,
        axis=1
    )

    print("\nDEBUG LOCATIONS:")
    print(sorted(df["location"].unique()))

    print("\nTOTAL CLEAN ROWS:")
    print(len(df))

    return df


# -----------------------------------
# TEST RUN
# -----------------------------------
if __name__ == "__main__":

    import pandas as pd
    from sqlalchemy import create_engine

    print("Loading data...")

    engine = create_engine(
        "sqlite:///data/real_estate.db"
    )

    df = pd.read_sql(
        "SELECT * FROM properties",
        engine
    )

    print("Raw rows:", len(df))

    df_clean = clean_data(df)

    df_clean.to_sql(
        "properties",
        engine,
        if_exists="replace",
        index=False
    )

    print("Clean rows:", len(df_clean))
    print(df_clean.head())#