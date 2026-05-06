##restroom_main.py##
# MAIN ENGINE & SCREEN MANAGER - User Interface
# This is the heart of our program. It controls what the user sees, handles menus,
# catches typing errors, and opens up the final map directions link.

import os
import webbrowser
from geoutils import calculate_distance, get_travel_time
from restroom_data import load_data, save_data, get_regional_data

def clear_screen():
    """
    A simple housekeeping function. It clears out old text from your command line
    terminal screen so the app looks clean like a modern visual page.
    """
    os.system('cls||clear')


def is_point_inside_kenya(lat, lon):
    """
    BORDER PROTECTION SCRIPT:
    This prevents users from inputting coordinates that point to the middle of
    the ocean or America. It treats the edges of Kenya like a giant connect-the-dots
    shape on a graph. It projects an imaginary line from your location and counts
    how many times it hits the border. An odd number means you are safely inside Kenya.
    """
    # A rough bounding box outlining the actual border shapes of Kenya.
    kenya_polygon = [
        (4.0, 34.0), (4.5, 36.0), (4.0, 42.0), (-1.5, 41.5),
        (-4.7, 39.2), (-1.0, 34.0), (1.0, 35.0), (4.0, 34.0)
    ]

    inside = False
    n = len(kenya_polygon)

    # Loop through all sides of our Kenya dot map shape.
    # The '(i + 1) % n' trick makes sure the very last line loops back to close the shape.
    for i in range(n):
        p1x, p1y = kenya_polygon[i]
        p2x, p2y = kenya_polygon[(i + 1) % n]

        # Check if our current latitude falls vertically between the two border points
        if min(p1x, p2x) < lat <= max(p1x, p2x):
            # Check if our longitude falls to the left of the border segment
            if lon <= max(p1y, p2y):
                # Calculate exactly where our imaginary line cuts through the border vector
                if p1x != p2x:
                    xints = (lat - p1x) * (p2y - p1y) / (p2x - p1x) + p1y
                # If our line crosses properly, flip the 'inside' state (True to False, or False to True)
                if p1y == p2y or lon <= xints:
                    inside = not inside

    return inside


def get_safe_float(prompt):
    """
    CRASH GLOVE:
    Normally, if an app asks for a number and a user accidentally types letters like 'xyz',
    the whole program instantly crashes with an ugly error. This safety function traps
    the typo, shows a friendly warning, and gently asks the user to try typing the number again.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ That wasn't a valid number. Please check your typing and try again.")


def find_nearest_ui(db):
    """
    THE SEARCH DASHBOARD:
    This is where everything comes together. It walks the user through selecting
    their County -> Landmark -> and filters out the closest toilets.
    """
    regions = get_regional_data()


    # STAGE 1: PICKING YOUR COUNTY
    clear_screen()
    print("\n🗺️  --- SELECT YOUR COUNTY ---")
    county_list = list(regions.keys())
    for i, county in enumerate(county_list, 1):
        print(f"  {i}. {county}")

    try:
        c_idx = int(input("\n👉 Choose County Number: ")) - 1
        # Block inputs that are smaller than 0 or larger than our county menu list
        if c_idx < 0 or c_idx >= len(county_list):
            raise IndexError
        selected_county = county_list[c_idx]
    except (ValueError, IndexError):
        print("❌ Invalid choice. Taking you back to the main menu.")
        return

    # STAGE 2: CHOOSE A LANDMARK (OR REQUEST HELP)
    clear_screen()
    print(f"\n📍 --- LANDMARKS IN {selected_county.upper()} ---")
    landmarks = regions[selected_county]
    landmark_list = list(landmarks.keys())

    for i, name in enumerate(landmark_list, 1):
        print(f"  {i}. {name}")

    print("  ──────────────────────────────────────────────────")
    print("  💡 Don't know which landmark is closest? Enter [0]")
    print("  ──────────────────────────────────────────────────")

    try:
        l_idx = int(input("\n👉 Choose your closest Landmark (or 0 for help): ")) - 1
    except ValueError:
        print("❌ Invalid choice. Taking you back to the main menu.")
        return

    # THE GPS ASSISTANT BRANCH: Triggered if the user typed 0 (Index -1)
    if l_idx == -1:
        clear_screen()
        print("\n🛰️  --- LOCAL COORDINATE ENFORCEMENT ASSISTANT ---")
        print("  ┌──────────────────────────────────────────────────────────┐")
        print("  │ ⚠️  COORDINATE DOMAIN RESTRICTIONS FOR KENYA:             │")
        print("  │    • Latitude must be between  -5.0  and   5.0           │")
        print("  │    • Longitude must be between  34.0  and  42.0          │")
        print("  └──────────────────────────────────────────────────────────┘\n")

        # Use our safe crash-proof input filter to grab coordinates
        user_lat = get_safe_float("   Enter your Latitude  (e.g. -1.2844): ")
        user_lon = get_safe_float("   Enter your Longitude (e.g. 36.8245): ")

        # Boot them out if they entered numbers that sit outside Kenya's territory
        if not is_point_inside_kenya(user_lat, user_lon):
            print("\n❌ ACCESS DENIED: Those coordinates point outside Kenya's borders.")
            input("\nPress Enter to return to the main menu...")
            return

        # Let's search through all our landmarks to see which one is closest to their coordinates
        closest_landmark_name = None
        shortest_distance = float('inf')

        for landmark_name, landmark_coords in landmarks.items():
            dist = calculate_distance(user_lat, user_lon, landmark_coords['lat'], landmark_coords['lon'])
            if dist < shortest_distance:
                shortest_distance = dist
                closest_landmark_name = landmark_name

        print(f"\n🎯 LOCAL SUGGESTION MATCHED!")
        print(f"   The closest landmark to your position is: {closest_landmark_name.upper()} ({shortest_distance:.2f} km away)")
        confirm = input("\nUse this landmark to find surrounding restrooms? (y/n): ").strip().lower()
        if confirm == 'y':
            selected_landmark = closest_landmark_name
        else:
            return
    else:
        # If they chose a normal number from the menu list, verify it fits inside bounds
        if 0 <= l_idx < len(landmark_list):
            selected_landmark = landmark_list[l_idx]
        else:
            print("❌ That number is not on the menu. Returning to main menu.")
            return

    # Extract the exact latitude and longitude values of the chosen landmark anchor
    u_lat = landmarks[selected_landmark]['lat']
    u_lon = landmarks[selected_landmark]['lon']

    # STAGE 3: RADIAL PROXIMITY SEARCH FILTER (Cut off at 5.0 km)
    nearby = []
    for r in db:
        dist = calculate_distance(u_lat, u_lon, r['lat'], r['lon'])
        # If the toilet is within 5 kilometers, save a copy of it to show the user
        if dist <= 5.0:
            res = r.copy() # Make a quick copy so we don't accidentally edit the primary database file
            res['dist'] = dist
            nearby.append(res)

    # STAGE 4: SORTING & DISPLAYING TOILETS
    clear_screen()
    if nearby:
        # Sort the toilets so the absolute closest one appears first at the top
        nearby.sort(key=lambda x: x['dist'])
        print(f"\n✨ FOUND {len(nearby)} OPTIONS NEAR {selected_landmark.upper()} ✨")
        print("─" * 65)

        for i, item in enumerate(nearby, 1):
            walk, drive = get_travel_time(item['dist'])
            print(f" 📍 [{i}]  {item['name'].upper()}")
            print(f"      Distance: {item['dist']:.2f} km")
            print(f"      ETA:      🚶 {int(walk)} min walk | 🚗 {int(drive)} min drive")
            print(f"      Location: {item['address']}")
            print("─" * 65)

        # STAGE 5: OPENING GOOGLE MAPS FOR NAVIGATION
        try:
            choice = int(input("\n👉 Select restroom number to navigate: "))
            if 1 <= choice <= len(nearby):
                selected_restroom = nearby[choice-1]

                # We build a standard web layout URL passing our starting landmark
                # and destination toilet coordinates.
                maps_url = (
                    f"https://www.google.com/maps/dir/?api=1"
                    f"&origin={u_lat},{u_lon}"
                    f"&destination={selected_restroom['lat']},{selected_restroom['lon']}"
                    f"&travelmode=walking"
                )
                print("\n🌐 Opening Google Maps in your web browser for walking directions...")
                webbrowser.open(maps_url)
        except ValueError:
            print("❌ Invalid input entry.")
    else:
        print(f"❌ Sorry, we don't have any restrooms registered within 5km of {selected_landmark}.")


def main():
    """
    THE SYSTEM MAIN LOOP:
    This runs an infinite menu cycle that loops continuously until the user
    explicitly chooses option 3 to close the terminal program window.
    """
    restrooms_db = load_data()
    while True:
        print("\n=== ELEVENS RESTROOM PORTAL ===")
        print("1. Add a Restroom\n2. Find Nearest Restroom\n3. Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            print("Feature coming soon! For now, please edit restrooms_db.json manually.")
        elif choice == "2":
            find_nearest_ui(restrooms_db)
        elif choice == "3":
            print("Closing the portal. Have a great day!")
            break
        else:
            print("❌ That choice is not on the menu. Try again.")

if __name__ == "__main__":
    main()
