#Sun Finder

- Update: Plans to revampt the site and launch on Heroku for July.

A Bay Area inspired web application to simplify search for micro climate weather results by just entering a San Francisco neighborhood. 

Developed in 3 weeks at the end of Hackbright Spring 2013.

For additional information on the development, checkout my blogpost at [nyghtowl.io](http://nyghtowl.io/category/hackbright/sun-finder/).

For screenshots, checkout [nyghtowl.github.io](http://nyghtowl.github.io/).

Technologies Used:
Python, Flask, Postgres, SQLAlchemy, Weather Underground API, Forecast.io API, Google Places & Maps APIs, Twitter Bootstrap, Javascript, JQuery, WTForms

===
### Project Walkthrough

I built this with a focus first on San Francisco and the intent on scaling out from there. There are two main pieces to this app which are search and results.

---
Search Function:

The first page of the app starts with just a search bar so you can enter the location you want the weather for. 

I created a database that lists common San Francisco neighborhoods with central coordinates and estimated radiuses. Initially I built the database in SQLite and then moved it to Postgres in anticipation of posting to Heroku in the future. I integrated the neighborhood names from the database by pulling it with SQLAlchemy &Python, passing it into my Flask views, extrapolating it with Jinja and then passing it through to JQuery to include as auto-complete results in the search bar.

If a user does not want to use the auto-complete then I set up search to switch over to utilize Google Places API and set parameters to bias the results to San Francisco. I did this by setting a central coordinate in the Bay Area with a radius that would cover from Sonomo to Half Moon Bay.

Either way the search result produces coordinates.

I also added the ability for the user to enter a future date to search on with the JQuery datepicker function. The default is the current date and time and the free API weather results are limited to 4 days out. I want to improve this by refining the search to time.

---
Weather Results:

I pass the resulting coordinates to Weather Underground and Forecast.io APIs. I used both APIs to compare the weather results and also because they produce different data points (e.g. one gives cloud cover). 

Initially, I pulled specific weather data points out of the resulting JSON files into a dictionary to help clarify what information I wanted to use. I changed the data structure into an object to make it easier to manage the weather results and cooresponding methods.

The methods and Flask views are really about clarifying what is presented out. For example based on the icon that is pulled from the weather data, it will help assign a corresponding sun or not sun image to post on the page. For fun I added a moonphase library that will post images of different moonphases if its nighttime in PST.

The initial resulting view that is returned is just an image and temperature without all the details you find on some weather sites because I wanted a simple answer. I do have a link that expands the page with more weather details if the user wants them. I also added Google Maps in the details to see the location of the search results. There is a overlay on Maps that pulls the names of the neighborhoods from my database.

---
Additional Notes & Plans:

Regarding Google Maps, I plan in future enhancements to add the ability to cache weather results and show them on the map next to the neighborhood names. I will also need to make adjustments on how neighborhood names are stored and pulled onto the map if I want to scale the results beyond SF. Additionally, I want to add functionality so the overlay results adjust when you zoom in and out on the map and I want the map to come up on the first page and adjust its results based on your IP location.

I started building out login functionality to enable user accounts. Two reasons were that I wanted to practice with Flask Login and WTForms while I had access to the Hackbright school resources and because I do want to create the ability for users to customize views (e.g. save favorites like 'I live in Sunset and work in SOMA'). More work is needed here to build this out.
