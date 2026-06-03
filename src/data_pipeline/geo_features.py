from geopy.distance import geodesic

# Kolkata metro stations
metro_STATIONS = {
    # --- BLUE LINE (North-South) #27
    "Dakshineswar": (22.6548, 88.3582),
    "Baranagar": (22.6433, 88.3654),
    "Noapara": (22.6402, 88.3934),
    "Dum Dum": (22.6246, 88.4250),
    "Belgachia": (22.6042, 88.3811),
    "Shyambazar": (22.6015, 88.3712),
    "Shobhabazar Sutanuti": (22.5947, 88.3662),
    "Girish Park": (22.5855, 88.3615),
    "Mahatma Gandhi Road": (22.5822, 88.3591),
    "Central": (22.5678, 88.3617),
    "Chandni Chowk": (22.5631, 88.3609),
    "Esplanade": (22.5647, 88.3533),
    "Park Street": (22.5534, 88.3503),
    "Maidan": (22.5452, 88.3475),
    "Rabindra Sadan": (22.5381, 88.3456),
    "Netaji Bhavan": (22.5317, 88.3444),
    "Jatin Das Park": (22.5234, 88.3431),
    "Kalighat": (22.5183, 88.3426),
    "Rabindra Sarobar": (22.5085, 88.3461),
    "Mahanayak Uttam Kumar": (22.4951, 88.3459),
    "Netaji": (22.4831, 88.3468),
    "Masterda Surya Sen": (22.4746, 88.3562),
    "Gitanjali": (22.4719, 88.3725),
    "Kavi Nazrul": (22.4678, 88.3845),
    "Shahid Khudiram": (22.4712, 88.3965),
    "Kavi Subhash": (22.4741, 88.3995),

    # --- GREEN LINE (East-West) #11
    "Howrah Maidan": (22.5816, 88.3243),
    "Howrah": (22.5847, 88.3315),
    "Mahakaran": (22.5714, 88.3491),
    "Sealdah": (22.5684, 88.3720),
    "Phoolbagan": (22.5711, 88.3917),
    "Salt Lake Stadium": (22.5714, 88.4064),
    "Bengal Chemical": (22.5794, 88.4082),
    "City Centre": (22.5891, 88.4093),
    "Central Park": (22.5898, 88.4167),
    "Karunamoyee": (22.5878, 88.4233),
    "Salt Lake Sector V": (22.5804, 88.4337),

    # --- PURPLE LINE (Joka-Esplanade) #7
    "Joka": (22.4522, 88.3018),
    "Thakurpukur": (22.4632, 88.3054),
    "Sakher Bazar": (22.4754, 88.3101),
    "Behala Chowrasta": (22.4842, 88.3129),
    "Behala Bazar": (22.4925, 88.3148),
    "Taratala": (22.5034, 88.3182),
    "Majerhat": (22.5184, 88.3246),

    # --- ORANGE LINE (Kavi Subhash-Airport) #5
    "Hemanta Mukhopadhyay": (22.5173, 88.4005),
    "VIP Bazar": (22.5285, 88.4011),
    "Ritwik Ghatak": (22.5372, 88.4022),
    "Barun Sengupta": (22.5434, 88.4036),
    "Beliaghata": (22.5539, 88.4055),

    #Yellow Line (Noapara – Barasat) #10
    "Noapara": (22.6402, 88.3934),
    "Dum Dum Cantt": (22.6417, 88.4069),
    "Jessore Road": (22.6515, 88.4214),
    "Jai Hind (Airport)": (22.6534, 88.4446),
    "Birati": (22.6683, 88.4371),
    "Michael Nagar": (22.6811, 88.4428),
    "New Barrackpore": (22.6954, 88.4445),
    "Madhyamgram": (22.7011, 88.4526),
    "Hridaypur": (22.7128, 88.4685),
    "Barasat": (22.7214, 88.4851),

    #Pink Line (Baranagar – Barrackpore) #10
    "Baranagar": (22.6433, 88.3654),
    "Kamarhati": (22.6715, 88.3698),
    "Agarpara": (22.6852, 88.3741),
    "Sodepur": (22.6974, 88.3765),
    "Panihati": (22.7092, 88.3782),
    "Subhash Nagar": (22.7221, 88.3795),
    "Khardah": (22.7294, 88.3802),
    "Tata Gate": (22.7441, 88.3775),
    "Titagarh": (22.7538, 88.3761),
    "Barrackpore": (22.7604, 88.3734)

}

# Approx location coordinates (simple mapping)
locations_COORDS = {
    # =========================================================================
    # TIER 10: ULTRA LUXURY & PRIME COMMERCIAL CORRIDORS (> ₹12,500/sq.ft)
    # =========================================================================
    "Alipore": (22.5310, 88.3330),
    "Ballygunge": (22.5280, 88.3650),
    "Park Street": (22.5488, 88.3526),
    "Elgin Road": (22.5407, 88.3512),
    "Minto Park": (22.5435, 88.3556),
    "Camac Street": (22.5442, 88.3531),
    "Loudon Street": (22.5458, 88.3562),
    "Ballygunge Circular Road": (22.5348, 88.3615),
    "Salt Lake": (22.5800, 88.4200),

    # =========================================================================
    # TIER 9: HIGH-END POSH CORE (₹10,000 - ₹12,500/sq.ft)
    # =========================================================================
    "New Alipore": (22.5115, 88.3356),
    "Bhowanipore": (22.5352, 88.3473),
    "Rash Behari Avenue": (22.5180, 88.3540),
    "Lake Market": (22.5170, 88.3510),
    "Gariahat": (22.5190, 88.3680),
    "Prince Anwar Shah Road": (22.5028, 88.3621),
    "EM Bypass": (22.5255, 88.3994),
    "Science City Area": (22.5401, 88.3962),
    "Kalighat": (22.5204, 88.3467),
    "Golpark": (22.5164, 88.3664),
    "Foreshore Road": (22.5681, 88.3312),

    # =========================================================================
    # TIER 8: PREMIUM INNER SUBURBS & TECH HUBS (₹8,500 - ₹10,000/sq.ft)
    # =========================================================================
    "New Town": (22.5750, 88.4786),
    "Salt Lake Sector V": (22.5694, 88.4322),
    "Shankhmani": (22.5451, 88.4912),
    "Kankurgachi": (22.5790, 88.3890),
    "Bidhan Nagar": (22.5900, 88.3900),
    "Dhakuria": (22.5105, 88.3692),
    "Chakgaria": (22.4815, 88.3991),
    "Golf Green": (22.4932, 88.3592),
    "Santoshpur": (22.4891, 88.3976),
    "Chingrighata": (22.5654, 88.4011),

    # =========================================================================
    # TIER 7: ESTABLISHED MODERN NODES (₹7,000 - ₹8,500/sq.ft)
    # =========================================================================
    "Tollygunge": (22.4950, 88.3458),
    "Jadavpur": (22.4950, 88.3700),
    "Kasba": (22.5184, 88.3832),
    "Ruby Connector": (22.5143, 88.4035),
    "Anandapur": (22.5174, 88.4116),
    "Phoolbagan": (22.5714, 88.3946),
    "Lake Town": (22.6041, 88.4032),
    "Bangur Avenue": (22.6083, 88.4068),
    "Shyambazar": (22.6020, 88.3710),
    "Hatibagan": (22.5974, 88.3703),
    "Sealdah": (22.5670, 88.3710),
    "Panchasayer": (22.4842, 88.4024),
    "Shibpur": (22.5641, 88.3214),

    # =========================================================================
    # TIER 6: MID-MARKET CORE & PRIME COMMUTER LOCALITIES (₹6,000 - ₹7,000/sq.ft)
    # =========================================================================
    "Beleghata": (22.5650, 88.3900),
    "Chetla": (22.5186, 88.3364),
    "Maniktala": (22.5812, 88.3742),
    "Ultadanga": (22.5855, 88.3832),
    "Mukundapur": (22.4862, 88.4124),
    "Patuli": (22.4742, 88.3883),
    "Haltu": (22.5093, 88.3814),
    "Garfa": (22.5021, 88.3765),
    "Tangra": (22.5513, 88.3917),
    "Topsia": (22.5385, 88.3942),
    "Chinar Park": (22.6250, 88.4500),
    "Chinar Park Crossroad": (22.6241, 88.4485),
    "VIP Nagar": (22.5380, 88.4000),
    "Kestopur": (22.5973, 88.4215),
    "Baguiati": (22.6148, 88.4232),
    "Teghoria": (22.6241, 88.4326),
    "Haldiram": (22.6364, 88.4371),
    "Kaikhali": (22.6321, 88.4412),
    "Kalikapur": (22.5024, 88.3968),
    "Ramrajatala": (22.5794, 88.2981),

    # =========================================================================
    # TIER 5: POPULAR URBAN POCKETS & TRANSIT HUBS (₹5,000 - ₹6,000/sq.ft)
    # =========================================================================
    "Rajarhat": (22.6100, 88.4800),
    "Behala": (22.5000, 88.3150),
    "Garia": (22.4620, 88.4000),
    "Garia Station Area": (22.4635, 88.4121),
    "Kamalgazi": (22.4542, 88.3934),
    "Bansdroni": (22.4764, 88.3618),
    "Kudghat": (22.4842, 88.3503),
    "Regent Park": (22.4795, 88.3514),
    "Naktala": (22.4721, 88.3653),
    "Baghajatin": (22.4815, 88.3732),
    "Picnic Garden": (22.5273, 88.3921),
    "Intally": (22.5550, 88.3680),
    "Tiljala": (22.5380, 88.3840),
    "Parnasree Pally": (22.5024, 88.3032),
    "Haridevpur": (22.4830, 88.3380),
    "Bijoygarh": (22.4920, 88.3640),
    "Paikpara": (22.6105, 88.3782),
    "Chiria More": (22.6186, 88.3798),
    "Sinthi More": (22.6284, 88.3791),
    "Nagerbazar": (22.6241, 88.4012),
    "Amherst Street Area": (22.5784, 88.3651),
    "Gora Bazar": (22.6251, 88.4112),
    "Airport Area": (22.6421, 88.4435),
    "Jessore Road": (22.6481, 88.4315),
    "Kavi Nazrul": (22.4681, 88.3812),
    "Howrah": (22.5850, 88.3300),
    "Kadamtala": (22.5842, 88.3115),
    "Baranagar": (22.6415, 88.3694),

    # =========================================================================
    # TIER 4: AFFORDABLE CITY CORE & GROWING SUBURBS (₹4,200 - ₹5,000/sq.ft)
    # =========================================================================
    "Thakurpukur": (22.4431, 88.2934),
    "Sarsuna": (22.4632, 88.2912),
    "Taratala": (22.5145, 88.3182),
    "Cossipore": (22.6212, 88.3694),
    "Dum Dum": (22.6200, 88.4000),
    "Nayabad": (22.4810, 88.4110),
    "Narendrapur": (22.4391, 88.3964),
    "Mahamayatala": (22.4512, 88.3981),
    "Ukhila": (22.4315, 88.4011),
    "Joka": (22.4312, 88.2864),
    "Pailan": (22.4215, 88.2694),
    "Madhyamgram": (22.6900, 88.4500),
    "Madhyamgram Chowmatha": (22.6952, 88.4601),
    "Sodepur": (22.6912, 88.4215),
    "Barasat": (22.7200, 88.4800),
    "Michael Nagar": (22.6512, 88.4491),
    "New Barrackpore": (22.6842, 88.4312),
    "Birati": (22.6612, 88.4284),
    "Hridaypur": (22.7051, 88.4712),
    "Belgharia": (22.6570, 88.3850),
    "Agarpara": (22.6804, 88.3782),
    "Panihati": (22.6934, 88.3742),
    "Kamarhati": (22.6715, 88.3712),
    "Ariadaha": (22.6631, 88.3592),
    "Dakshineswar": (22.6548, 88.3512),
    "Satgachhi": (22.6181, 88.4115),
    "Jawpur": (22.6212, 88.3915),
    "Batanagar": (22.5112, 88.2315),
    "Maheshtala": (22.5084, 88.2512),
    "Santragachi": (22.5714, 88.2812),
    "Shalimar": (22.5584, 88.3181),
    "Liluah": (22.6184, 88.3412),
    "Salkia": (22.5991, 88.3494),
    "Dasnagar": (22.5912, 88.3012),
    "Ichapur (Howrah)": (22.5932, 88.2891),
    "Uttarpara": (22.6681, 88.3442),
    "Konnagar": (22.6991, 88.3481),
    "Serampore": (22.7512, 88.3414),
    "Serampore Riverfront": (22.7562, 88.3512),
    "Makhla": (22.6715, 88.3312),
    "Nabagram": (22.6981, 88.3242),

    # =========================================================================
    # TIER 3: SUBURBAN RAIL CORRIDORS & EXTENDED GROWTH PATHS (₹3,500 - ₹4,200/sq.ft)
    # =========================================================================
    "Sonarpur": (22.4350, 88.4300),
    "Rajpur": (22.4215, 88.3912),
    "Harinavi": (22.4132, 88.4015),
    "Boral": (22.4412, 88.3721),
    "Elachi": (22.4271, 88.4092),
    "Subhasgram": (22.4012, 88.4215),
    "Mallikpur": (22.3794, 88.4281),
    "Nangi": (22.5015, 88.2212),
    "Barrackpore": (22.7600, 88.3700),
    "Nona Chandanpukur": (22.7564, 88.3812),
    "Khardah": (22.7164, 88.3815),
    "Titagarh": (22.7381, 88.3762),
    "Shyamnagar": (22.8271, 88.3912),
    "Mourigram": (22.5694, 88.2612),
    "Andul": (22.5742, 88.2415),
    "Kona Expressway Corridor": (22.5815, 88.2715),
    "Bankra": (22.6115, 88.2912),
    "Hindmotor": (22.6812, 88.3391),
    "Rishra": (22.7154, 88.3492),
    "Baidyabati": (22.7915, 88.3284),
    "Sheoraphuli": (22.7791, 88.3341),
    "Chandannagar": (22.8684, 88.3694),
    "Mankundu": (22.8512, 88.3514),
    "Chinsurah": (22.9015, 88.3891),
    "Chinsurah Raghunathpur": (22.8981, 88.3742),
    "Bandel": (22.9215, 88.3781),
    "Kalyani Expressway Corridor": (22.7415, 88.4012),

    # =========================================================================
    # TIER 2: MAJOR INDUSTRIAL-RESIDENTIAL MIX HUBS (₹2,800 - ₹3,500/sq.ft)
    # =========================================================================
    "Baruipur": (22.3556, 88.4312),
    "Govindapur (South)": (22.3815, 88.4094),
    "Langalberia": (22.4012, 88.4151),
    "Amtala": (22.3712, 88.2715),
    "Bishnupur (South)": (22.3781, 88.2512),
    "Budge Budge": (22.4815, 88.1812),
    "Naihati": (22.8915, 88.4194),
    "Kanchrapara": (22.9421, 88.4312),
    "Halisahar": (22.9232, 88.4151),
    "Badu": (22.7121, 88.5214),
    "Badu Road (Barasat)": (22.7291, 88.5024),
    "Nilganj": (22.7481, 88.4312),
    "Laskarhat": (22.5181, 88.4194),
    "Domjur": (22.6394, 88.2212),
    "Nibra": (22.5994, 88.2612),
    "Salap": (22.6124, 88.2681),
    "Ankurhati": (22.6015, 88.2484),
    "Lilua (Jalan Industrial Complex Area)": (22.6412, 88.2515),
    "Bally Durgapur": (22.6515, 88.3212),
    "Bally": (22.6481, 88.3412),
    "Belur": (22.6315, 88.3491),
    "Sankrail": (22.5312, 88.2415),
    "Dankuni": (22.6815, 88.2915),
    "Dankuni Housing Complex Area": (22.6891, 88.3012),
    "Raghunathpur (Hooghly)": (22.7212, 88.3341),
    "Baigachhi": (22.7294, 88.3115),
    "Telenipara": (22.8421, 88.3612),
    "Sugandha": (22.9124, 88.3315),
    "Delhi Road Corridor (Hooghly)": (22.7412, 88.3181),
    "Bantala (IT SEZ Area)": (22.5184, 88.4682),
    "Hatisala": (22.5312, 88.4742),
    "Nandakumarpur / Diamond Harbour Rd": (22.3912, 88.2612),

    # =========================================================================
    # TIER 1: PERIPHERAL HORIZONS & PRIMARY INVESTMENT HORIZONS (< ₹2,800/sq.ft)
    # =========================================================================
    "Habra": (22.8364, 88.6603),
    "Ashoknagar": (22.8315, 88.6212),
    "Dutta Pukur": (22.7664, 88.5412),
    "Ghatakpukur (Basanti Highway)": (22.5112, 88.5815),
    "Bhangar": (22.5381, 88.6012),
    "Champahati": (22.4112, 88.4915),
    "Sirakol": (22.3412, 88.2415),
    "Uluberia": (22.4691, 88.1112),
    "Bagnan": (22.4721, 87.9715),
    "Singur": (22.8124, 88.2312)
}

def get_distance_to_metro(location):
    if location not in locations_COORDS:
        return None

    property_coord = locations_COORDS[location]

    min_distance = float("inf")

    for metro, coord in metro_STATIONS.items():
        dist = geodesic(property_coord, coord).km
        min_distance = min(min_distance, dist)

    return round(min_distance, 2)

def get_geo_features(location):
    
    metro = get_distance_to_metro(location)

    if metro is None:
        metro = 5

    return {
        "metro_distance_km": metro,

        "hospital_distance_km": round(max(0.5, metro * 1.2), 2),
        "school_distance_km": round(max(0.5, metro * 0.8), 2),
        "college_distance_km": round(max(0.5, metro * 1.1), 2),
        "bus_stop_distance_km": round(max(0.2, metro * 0.5), 2),
        "railway_distance_km": round(max(0.5, metro * 1.3), 2),
        "police_distance_km": round(max(0.5, metro * 1.0), 2),
        "postoffice_distance_km": round(max(0.5, metro * 1.1), 2),
    }