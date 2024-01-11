
# Stay Worldly : https://stay-worldly.onrender.com/


Stay Worldly allows a user to create an account, search for cities world wide, learn about selected cities, save cities to their user page, and mark saved cities as visited. I created this for remote workers to see places they may want to visit or move to.


## Features:
- Register
- Log In
- Home page cities list
    - The home page cities list is a constantly changing list of cities recently saved by other users. Having this list allows for a user to be exposed to cities they may have never heard of.
- Edit User
    - This allows a user to update their employer timezone so they can get an idea of when their work day would begin in any given city.
- Search for a city
    - When a user searches for a city several cities with matching names are returned. The user can then choose one which will take them to a page that has information about the city or, if there is no information for the city selected they will be redirected back to the homepage and a flash message will let the user know that the selected city doesn’t have a page yet.
- Save/remove a city
    - When a user is viewing a city information page they have the option to save the city. This will add the city to the user's page and the city will appear on the user's page until they remove it, if they wish to do so.
- Mark a city as visited
    - This allows a user to move a saved city from "future adventures" to "past adventures". By doing so a user can keep track of the places they have visited.


# APIs used:


1. https://developers.teleport.org/api/reference/#!/root/getRoot
2. https://countryinfoapi.com/documentation
3. https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/


### Localhost 
- If running Stay Worldly locally and your travel database is empty an error will be triggered. To fix this error comment out line 49 and comment in line 51 until 9 atleast cities have been added to your database. 


### Tests:
1. test_gets.py
2. test_user.py
3. test_user_city.py


These tests can be ran in the terminal with:
- ipython -m unittest file_name.py


### User Flow
1. The home page prompts a user to log in or register and displays a list of 9 cities that have recently been saved by other users.
2. The user registers and is redirected back to the home page and is logged in.
3. The user sees the list of cities and a search form. A user can either select a city that is pre populated or search for a new city.
4. Upon selecting the city a user is taken to a page with information about the selected city.
5. A user has the option to save the city or to return to the home page to search for other cities.
6. If the user saves a city they are redirected to their user page.
7. The user page displays saved cities under future adventures and the user has the option to remove cities or to mark a city as visited. This would move the city from the Future Adventures section to the Past Adventures section.
8. On the user page the user sees their information and a button to edit their information.
9. A user has the ability to edit their first name, last name, and employer timezone which will only be updated if they put in the correct password.
10. A user can log out by clicking the logout button in the nav bar.


### Tech Stack:

#### Front end
1. html
2. CSS
3. Bootstrap 5
4. Javascript
5. Jinja


#### Back end
1. Python
2. Flask
3. SQLAlchemy
4. WTForms