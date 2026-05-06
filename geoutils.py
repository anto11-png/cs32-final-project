##geoutils.py##
# THE MATHEMATICAL ENGINE (geoutils.py)
# This file handles all the tricky map math. We keep it separate so it doesn't
# clutter up our main user interface file.
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    This function measures the distance between two pairs of coordinates.
    Since the Earth is round like a ball, we can't just use a straight flat ruler.
    We use a formula called the 'Haversine Formula' to calculate distances
    accurately around the Earth's curve.
    """
    # Earth's radius is roughly 6371 kilometers. We need this to get our final answer in km.
    R = 6371

    # Python's math functions don't understand regular map degrees.
    # We must convert the degrees into 'radians' first, otherwise the math breaks.
    phi1 = math.radians(lat1)    # Starting point latitude
    phi2 = math.radians(lat2)    # Destination point latitude

    # Calculate how far apart the two places are vertically and horizontally
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    # This is the core magic of the Haversine formula. It computes the curve
    # between the two points through three-dimensional space.
    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2

    # This cleans up the raw math and turns it into a proper curved angle.
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Finally, we multiply that angle by the Earth's size to get the actual kilometers.
    return R * c


def get_travel_time(km):
    """
    Telling someone 'the toilet is 2km away' isn't helpful when they are in a rush.
    This simple function changes kilometers into minutes so it makes sense to a human.
    """
    # Walking time: Assumes a normal person walks at about 5 kilometers per hour.
    # We divide the distance by 5, then multiply by 60 to convert hours to minutes.
    walk_min = (km / 5) * 60

    # Driving time: Assumes standard town driving speed of 40 kilometers per hour.
    # This takes into account things like bumps, roundabouts, and basic Kenyan town traffic.
    drive_min = (km / 40) * 60

    # Send back both times at once (walking minutes, driving minutes)
    return walk_min, drive_min
