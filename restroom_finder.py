##restroom_finder.py##

restrooms = [] #Creates an empty list called restrooms where all added restrooms will be stored.

print("Welcome to Elevens!\n")

def add_restroom(): #Defines the function add_restroom which asks the user the inputs.
    name    = input("Restroom name: ")
    address = input("Address: ")
    rating  = int(input("Rating (1-5): "))

    #Packages the inputs into the dictionary called restroom
    restroom = {
        "name"   : name,
        "address": address,
        "rating" : rating
    }

    #Adds the dictionary into the restrooms list
    restrooms.append(restroom)
    print(f" '{name}' added!\n") #Confirms the addition of a restroom


def view_all():
    if not restrooms: #If no restrooms are added, it shows you that there are no restrooms
        print("No restrooms added yet.")
        return
    for r in restrooms: #Loops through restrooms in the list and shows their details
        print(f"- {r['name']} | {r['address']} | {r['rating']} stars")

# Main
while True: #Starts a loop that provides option for the user, whether adding a restroom, or viewing the available ones or quiting the platform.
    print("What would you like to do?")
    print("1. Add restroom")
    print("2. View all restrooms available")
    print("3. Quit")
    choice = input("Choose: ")

    if choice == "1":
        add_restroom()
    elif choice == "2":
        view_all()
    elif choice == "3":
        break
