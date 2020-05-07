Janani Sekar

This project was implemented using flask, html+css, and javascript.

Login and Register:
The login and register pages have largely the same function and purpose as the login and register pages in cs50 finance.
I set up the database mood.db with a users table to keep track of existing users and new users who make accounts.The login function asks a user to enter their username and their password.
The user and hashed value of the password are stored in the users table in mood.db. Both of these fields are unique to a user.
The register page is where the user first picks a username and a password whose hash value is stored.
I mainly used the code I wrote in cs50 finance with slight modifactions and changes in style. These changes were primarily made in styles.css.


Navigation:
Next, I designed a logo using a google-font, handlee, which I imported into my css. The styling for paragraphs on my page also uses the same google font for consistency.
The color scheme chosen for this project is one with cool shades, mostly purples, greens, and blues. The logo follows this scheme. This logo and the navbar, along with links to the login and register pages were coded into layout.html.
The styling for the navbar is using bootstrap, which is imported into layout.html
I knew I wanted a calendar and analysis page from the beginning, so I added links for those pages to my navbar.
layout.html was then moved to a templates folder, along with empty html files for the homepage, calendar, and analysis pages.

Index:
For the main part of the web app, I began by building the index page using html, css, and javascript. The html buttons were first created, one to represent each mood. Each mood was assigned a different color ranging from purples for more negative moods to greens for more positive moods.
Then, I added a font-awesome heart icon that would change color based on which mood button was clicked. This color change is made possible through a simple javascript function that checks which button is selected and correspondingly makes the heart that color.
One final touch to the heart was making it beat. This design element was added much later through some simple css. The heart was assigned a class, which was then animated over a 5 second interval by just oscillating the size.
The next part of building the index page was making sure the user's input mood was actually recorded and trackable.
To make this happen, I set up the buttons inside an html form, where the submission value would be the mood that corresponded to a certain button. This form is submitted via POST. The index function in application.py submits this value to a SQL database using db.execute, which is imported from the CS50 module. The SQL database in this case is the previously created mood.db.
The values get submitted to a new table called moods, which stores user_id, date, and mood. The date is an autofill value. I restrict the inputs to the table such that there can only be one mood stored per day.
When the form is submitted, the program checks if there is already a mood recorded for a day from a given user, and if so, just updates the mood instead of inserting a new entry.
Although this is not technically possible given the construct of my page, I make sure to return an apology if for some reason, no mood is submitted through the form.
As seen in the index function, the index.html template is rendered after submitting the form. When it is reloaded, the heart icon is no longer colored in from the javascript. To prevent the coloring from resetting, the coloring for the heart is stored in local storage and then accessed when the page is reloaded.

Calendar:
The calendar page displays your mood over the past 3 weeks.
For the first week, I import all the entries from the moods database for a certain user for the last week. This is done using the date entry in the SQL table and functions from the datetime module in python. The moods for each day ae then chronologically added to a list, while filling in null values for days where there was no entry.
Then, the html template for this page creates a table of 7 days, the first row displaying the date, and the second row displaying the mood. A javascript function then colors in the mood cell based on what the mood for that day is.
A similar process is used for the second and third week: the data for that week is accessed from the SQL table and then displayed in the same way.

Analysis:
This page requires adding 3 more tables to the SQL database. The weights table stores the numerical value associated with each mood. More "negative" moods are associated with more negative numerical values and more "positive" moods are associated with higher positive numerical values.
The analysis function then calculates an "average mood" for the week by totaling and dividing the value of every mood for that week and the number of entries.
The weekly table then stores a set of quotes and advice corresponing to FALSE for a negative average mood and TRUE for a positive average mood. The analysis function then randomly selects an entry from the weekly table to return to the user.
This analysis intentionally only has 2 boolean categories of negative average moods and positive average moods.
This is because forming more specific categories can lead to inaccuracies. For example, someone who was equally stressed and happy in the same week may average to a slightly positive sentiment. However, if we used the "mood" associated with this slightly positive number, it would be the "calm" mood, which is not reflective of how the person actually felt.
Moreover, the current day is included in this weekly average, and since a person's mood may change throughout the day, less categories allows for less fluctuation in recommendations.
Thus, the weekly analysis only looks to see if the person is feeling more positive or negative.
The daily analysis allows us to get more specific. Here, we create a daily table, storing quotes and activites that correspond to each mood. When a person chooses a mood, the function queries all the entires for that particular day and randomly returns one to the user.
The third component of the analysis is to watch out for unhealthy mood patterns. If someone logs that they are sad or anxious for three or more consecutive days, the application will flash them a message.
The quotes, "mood weights", and recommendations are all sourced from articles and journals linked in the "README". A smaller positive or negative value for a mood is not to dismiss it as unimportant, but rather to suggest that it is a more temporary or less strong emotion.
