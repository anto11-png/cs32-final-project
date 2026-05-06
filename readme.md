I realized that most apps that show direction do not actually locate restrooms. When one is in a new place, restromms can be the hardest things to find. I saw a niche in this, and decided that I will have this as my project. My project is creating a platform that has a portal of adding any public restroom available within a locality, then gives the directions to thos restrooms, within that specific locality. So first of all, I will have to create this portal where people add information of restrooms they know, their address, and their quality (for example, 3-star). Next will be making this information public to anybody accessing the platform. After this, I will have to have a manner to show direction from someone's current location, to where the nearest restroom is. I will create an algorithm that only identifies restrooms within a 5-drive or 10-minute walk.


So in restroom_finder.py I did a code that gives one the option to add a restroom or access another restroom that has been added. While adding the restroom, you include information like the address and star rating. However, this information is all stored in the computer RAM. Once you close the program, every restroom is deleted forever. So I needed to advance to a state where I have restroom data saved in a database.

**Haversine Formula**
However, before coming up with the database, I needed the location of the restroom to be included in the database. So I designed the locations in terms of latitudes and longitudes of common places in Kenya which I marked as landmarks. Therefore, while you are in a new area or unknown area, you simply type in the landmark that you are closest to, then you will be able to find a restroom. So the big thing at the moment, it is about locating the landmark that will be instrumental in finding the restroom.

**Restroom Database**
So I have a database that is saved in terms of landmarks within Kenyan counties (the correspondence of American states). So wherever you are, when you enter the Elevens Platform (the platform for finding restrooms), you first of all key in the county where you are. After keying in your county, you will be given the available landmarks nearby. So you need to choose the closest landmark, which is definitely a common place that cannot lack any restroom. The information of the counties and landmarks are found in restroom_data.py and the file that makes this possible is restroom_main.py, because it deals with the use interface.

***FP_SUBMISSION ADJUSTMENT****
This are the final additions and adjustments that I made to my CS32 project.

(i) **Walking and Driving Times** - Adding the get_travel_time function to geoutils.py

You realize that being the Elevens Portal telling you that a restroom is 2km away is not really helpful. It can be deceptive because 2km might sound short, whereas it could be a long distance away. This can be disastrous because a restroom could be needed for emergency purposes. So I added the time element whereby the distance to the restroom is matched with the estimated time of arrival. This is calculated using a walking speed of 5km/hr and a driving speed of 40km/hr.


(ii) **Autogenerating Restrooms** - Including get_preseed_data function in restroom_data.py
In FP Status, I encountered a single problem, whereby some landmarks had no restroom anywhere close to them. "No restroom available" was the response of clicking those landmaarks. However, the significance of using a landmaark was positioning one in a place where most facilities are, for example, bus stop, restaurants and restrooms. Having no restroom at a landmark just made no sense.

So get_preseed_data function basically generates restrooms for each landmark, the first time I run restroom_main.py. Each landmark therefore has a restroom available, making this project complete, even though this is not the case in real life.

(iii) **Checking Kenyan Borders** - Having is_point_inside_kenya function in restroom_main.py
To avoid issues like adding or searching up restrooms in the ocean or somewhere in America, I restricted the domains to the latitudes and longitudes bounding Kenya. So I implemented this through the is_point_inside_kenya function that creates digital boundaries for the search engine.

(iv) **Typos Will Not Crash The Elevens Portal** Having the get_safe_float function in restroom_main.py
Someone interacting with the user interface for the first time is likely to key in words or alphabets when told to write their latitudes and longitudes (even though I avoided this as much as possible, it still features somewhere, but in a small portion). To avoid crsshing, we have the get_safe_float function that ensures an error is printed in case of typos or wrong entries.

(v) **Google Maps Directions** - webbrowser.open
Initially, the final stage of searching for a restroom was getting to know the closest landmark, and the distance of the restrooms from that particular landmark. However, this is not helpful because one is using this platform to find a restroom in a place they are not particularly familiar with. Therefore, telling them the distance or even the time they will take to reach the restroom isn't ideally valuable. So I introduced this connection with Google Maps whereby after entering the landmark you are closest to, the Google maps directs you from your specific location to the location of the restroom. Google Maps has both the paths and roads followed by pedestrians and drivers respectively, so both parties are taken care of.

   *Why it was necessary to generate the restrooms in the database using AI*
   AI generated the restrooms with almost accurate latitudes and longitudes. As a result, switching to Google Maps had the portal working almost accurately. You can imagine what5 could have happened if I had plugged in restroom latitudes and longitudes entirely from my mind.

*What if I do not know any landmark*
In case the use of Elevens Platform is totally new to the area where they are, and doesn't know the landmarks around, this is when they is demanded to key in their latitudes and longitudes. This could be simple, ideally through a Google search. The user will then key in their latitudes and longitudes, after which Elevens Platform will give them an option for the closest landmark available. From there they can select the restrooms associated with the landmark, and move to the ones of their interest as guided by Google Maps.

(vi) **Aesthetics**
To make the Elevens Portal cleaner and more aesthetic:
- I added os.system('cls||clear'), which ensures that the page gets cleared of the previous information displayed, once a function is executed. For example, after choosing the county, the page fully shifts to the landmarks available in that county, without showing the list of counties. In short, Elevens Portal now transits from one page to another once a code has been executed.
- I added emojis in order to improve the visual eefect of Elevens Portal. For instance, instead of writing '3-star' I adjusted it to ⭐️⭐️⭐️ to make it more appealing to the eye of the user. (The code to generate the emojis were AI generated because I am not that good with that part of Python).
- I also added lines to separate the list of landmarks in each country. Furthermore, I made the platform present all the details on their separate lines in order to improve the overall appearance of the information displayed by the portal.


*This is my project. I appreciate feedback from Melody.*

*Thank you for esxploring Elevens Portal. It has been an absolute honor to work on this.*
