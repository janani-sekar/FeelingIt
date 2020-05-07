#Feeling it!
"Feeling it!" is a mood tracker that allows a user to enter, track, and analyze their mood over an extended period of time.

This project was entirely implemented using CS50 IDE. In order to use the project, one must import the cs50 module, download the project directory which contains application.py, a SQL database (mood.db) and html templates.
After downloading the project directory and opening it, run flask from the terminal to open up the project.
It will take the user to the login page.

#Login page:
If you have an account that exists, or are a returning user, enter your user-id and password to hit the login button to login to the website.
Here, you will be redirected to the homepage, where you will be able to record and access your personal mood data.
If you do not have an account that exists, at the top right of the page, there is the option to register for an account.

#Register Page:
If you do not already have an account, you can register for one here. You will be prompted for a username and password. You will have to re-enter your password to confirm it.
If you do not see an error, you have successfully registered and will be taken to the homepage.

#The homepage:
The homepage is where you record your mood for a particular day.
On the homepage, you will see a beating heart and below it a range of moods, each of which is a button. Click on the corresponding button to record your mood for that day.
You will see the heart change color according to the mood you just marked as a confirmation. Only one mood gets stored per day, based on what value has been recorded at 11:59 p.m. that day.
If your mood changes over the course of the day, you can update your mood by selecting a different button and the new value will get recorded instead.
If you do not enter your mood for a particular day, nothing will get recorded. At any given point in time, the heart displays your last recorded mood, no matter how many days prior this entry was made.

#Calendar:
The calendar page can be accessed through the navigation bar at the top. On this page, you will see personalized mood data for three weeks: the current week, last week, and two weeks ago.
For each week, the date is displayed and below it, the mood that was recorded for that day. This allows the user to visualize trends and patterns in their mood over periods of time.
The current day's mood is the rightmost entry in the current week. As a user may modify their mood throughout the day, the mood entry for the current day may keep changing until 11:59 when it has been permanently recorded.

#Analysis:
This page calculates a weekly weighted average mood, based on how negative and positive your feelings were over the past week. Because your entry for the current day is included in the weekly average, the weekly average may shift based on how you feel today.
Based on the weighted average, the page reccommends an activity for you to do or offers recommendations pulled from various psychology blogs and journals, all linked below. Below the weekly message is a daily message.
The analysis page also knows to identify unhealthy patterns in a user's mood. If a user indicates that they are feeling sad or anxious multiple times a week, the page will ask if everything is normal. This message displays below the weekly and daily messages.
The analysis page offers an interactive spin on a mood tracker which gives the user more insight on what their mood may mean, and also provides a sense of comfort and support.


Sources:

https://lifelabs.psychologies.co.uk/users/11134-lydia-kimmerling/posts/5241-feel-like-your-living-ground-hog-day-make-life-exciting-again-in-just-30-minutes
https://www.psychologytoday.com/us/blog/the-creativity-cure/201402/how-be-calm-person
https://greatist.com/happiness/34-ways-bust-bad-mood-ten-minutes#1
https://www.verywellmind.com/ways-to-calm-down-quickly-when-overwhelmed-3145197
https://www.huffpost.com/entry/stress-relief-that-works_n_3842511
https://www.medicalnewstoday.com/articles/323454#takeaway
https://www.healthline.com/health/how-to-calm-down#1
https://www.healthline.com/health/how-to-calm-anxiety#5


