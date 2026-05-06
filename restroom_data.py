##restroom_data.py##
# THE DATABASE LAYER
# This file acts as our data manager. It holds our built-in landmarks for all
# 10 counties, automatically sets up dummy restrooms, and saves everything to a
# file so we don't lose data.

import json
import os

# This is the name of the file that will be created on your computer to save our data.
FILE_NAME = "restrooms_db.json"


def get_regional_data():
    """
    This is our local map directory. Instead of making users type raw coordinates,
    we let them pick a famous, undeniable landmark they already recognize.
    We store them nicely by County -> Landmark Name -> Real Coordinates.

    All 10 original counties are fully restored below!
    """
    return {
        "Nairobi": {
            "Kencom/Ambassadeur": {"lat": -1.2844, "lon": 36.8245},
            "Westlands (Sarit)": {"lat": -1.2650, "lon": 36.8044},
            "Upperhill (NHIF)": {"lat": -1.2990, "lon": 36.8144},
            "JKIA Airport": {"lat": -1.3331, "lon": 36.9275},
            "Gikomba Market": {"lat": -1.2845, "lon": 36.8340}
        },
        "Mombasa": {
            "Elephant Tusks": {"lat": -4.0664, "lon": 39.6639},
            "Nyali Centre": {"lat": -4.0321, "lon": 39.7021},
            "Likoni Ferry": {"lat": -4.0811, "lon": 39.6644},
            "SGR Terminus": {"lat": -3.9981, "lon": 39.5932},
            "Mama Ngina Drive": {"lat": -4.0725, "lon": 39.6739}
        },
        "Kisumu": {
            "Kondele Junction": {"lat": -0.0917, "lon": 34.7680},
            "Winam Gulf Pier": {"lat": -0.1022, "lon": 34.7617},
            "United Mall": {"lat": -0.0981, "lon": 34.7622},
            "Kisumu Airport": {"lat": -0.0847, "lon": 34.7289},
            "Jubilee Market": {"lat": -0.1044, "lon": 34.7522}
        },
        "Nakuru": {
            "Main Bus Stage": {"lat": -0.2833, "lon": 36.0667},
            "Westside Mall": {"lat": -0.2881, "lon": 36.0622},
            "Free Area Stage": {"lat": -0.2895, "lon": 36.0912},
            "Section 58": {"lat": -0.2811, "lon": 36.0844},
            "Hyrax Hill": {"lat": -0.2858, "lon": 36.1021}
        },
        "Uasin Gishu": {
            "Zion Mall Eldoret": {"lat": 0.5167, "lon": 35.2833},
            "Rupa Mall": {"lat": 0.5211, "lon": 35.3012},
            "Eldoret Sossiani": {"lat": 0.5144, "lon": 35.2691},
            "Eldoret Airport": {"lat": 0.4122, "lon": 35.2344},
            "Eldoret Central Market": {"lat": 0.5181, "lon": 35.2711}
        },
        "Kiambu": {
            "Thika Blue Post": {"lat": -1.0267, "lon": 37.0667},
            "Kiambu Town Stage": {"lat": -1.1714, "lon": 36.8275},
            "Roysambu (TRM)": {"lat": -1.2210, "lon": 36.8837},
            "Limuru Stage": {"lat": -1.1084, "lon": 36.6421},
            "Ruaka Triangle": {"lat": -1.2064, "lon": 36.7767}
        },
        "Machakos": {
            "Peoples Park": {"lat": -1.5165, "lon": 37.2616},
            "Machakos Bus Station": {"lat": -1.5211, "lon": 37.2655},
            "Mavoko (Ath River)": {"lat": -1.5011, "lon": 36.9612},
            "Kyumvi Junction": {"lat": -1.5644, "lon": 37.1512},
            "Tala Market": {"lat": -1.2811, "lon": 37.3812}
        },
        "Kilifi": {
            "Malindi Marine": {"lat": -3.2235, "lon": 40.1281},
            "Vasco Da Gama": {"lat": -3.2321, "lon": 40.1311},
            "Pwani University": {"lat": -3.6331, "lon": 39.8491},
            "Mtwapa Mall": {"lat": -3.9421, "lon": 39.7345},
            "Kilifi Bridge": {"lat": -3.6381, "lon": 39.8512}
        },
        "Garissa": {
            "Post Office": {"lat": -0.4532, "lon": 39.6461},
            "Garissa University": {"lat": -0.4721, "lon": 39.6612},
            "Dadaab Area": {"lat": 0.1067, "lon": 40.2981},
            "Tana Bridge": {"lat": -0.4511, "lon": 39.6312},
            "Garissa Market": {"lat": -0.4561, "lon": 39.6481}
        },
        "Kajiado": {
            "Kitengela Mall": {"lat": -1.4820, "lon": 36.9600},
            "Namanga Border": {"lat": -2.5431, "lon": 36.7845},
            "Kajiado Stage": {"lat": -1.8510, "lon": 36.7750},
            "Ngong Hills": {"lat": -1.3611, "lon": 36.6512},
            "Ongata Rongai": {"lat": -1.3961, "lon": 36.7612}
        }
    }


def get_preseed_data():
    """
    Typing out 100 restrooms manually is exhausting. This function automatically
    generates sample restrooms around our main landmarks when the app runs for
    the first time. It slightly alters the numbers so the restrooms pop up
    a few meters away from the landmark.
    """
    regions = get_regional_data()
    data = []

    # Loop through every single county and landmark we have saved above
    for county, landmarks in regions.items():
        for l_name, coords in landmarks.items():

            # Restroom 1: Shift coordinates slightly North-East.
            # This creates a premium restroom super close by (under 300 meters away).
            data.append({
                "name": f"{l_name} Premium Lounge",
                "address": f"Inside {l_name} Complex, {county}",
                "lat": coords['lat'] + 0.0015,
                "lon": coords['lon'] + 0.001,
                "rating": 5
            })

            # Restroom 2: Shift coordinates slightly South-West.
            # This simulates a basic public toilet further down the street (about 400 meters away).
            data.append({
                "name": f"{l_name} Public Point",
                "address": f"Lower parking near {l_name}, {county}",
                "lat": coords['lat'] - 0.0035,
                "lon": coords['lon'] - 0.002,
                "rating": 3
            })
    return data


def load_data():
    """
    This function loads our data. If it's your first time opening the app, it
    creates the 'restrooms_db.json' file and fills it with our sample toilets.
    If the file already exists, it just reads it normally.
    """
    if not os.path.exists(FILE_NAME):
        # File is missing! Let's generate a fresh batch of sample restrooms.
        data = get_preseed_data()
        save_data(data)
        return data

    # File exists, let's open it up, read the text, and turn it into a Python list.
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_data(data):
    """
    This takes our list of restrooms and writes it back onto your hard drive
    so your changes are safely saved when you close the app.
    """
    with open(FILE_NAME, "w") as f:
        # 'indent=4' makes the saved text file neat and readable for humans to look at.
        json.dump(data, f, indent=4)
