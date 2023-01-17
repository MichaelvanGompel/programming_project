#PROCESS BOOK

1/12 TO 3/12
This week had been rough, getting bad news from UvA threw a spanner in the works.

4/12 
General outline was formed using the help of Hands and Quinten/Quintin. 
Due to the nature of this week I trimmed down my large plan to a more achievable goal.

Instead of making graphs for genres and artists in general I will focus on specific users for now, and add more applications if the time allows it.

5/12
Today I went looking for a HTML web scraping tool only to find the API from last.fm has enough tools for my goal
Checking to see how a Last.fm user can log in on the web application. This turned out to be rather difficult.

Turns out I dont need authentication, it is only needed for write functions.

06/12
Today I start with exploring the Last.fm API. Trying to get the logic down for extracting data for the user. I need to know how the structure is built from API responses before I make the models. This way I will be able to fit my modles onto the API because the API is not flexible.

If I want to make a graph for weekly artists/tags then I will need the lists of available weeks.
I can use this list to get the top artists/tags for those weeks, while keeping track of the date.

Probably will still add a login feature, so that users will only have to log in once to keep their data.

API top weekly artist feature only finds one artist, insufficient for my project so I will have to find another workaround.

Looks like I will have to load all the songs. Wrote a function to clean unnecessary data but one 'mbid' still remains, unclear why.
<<<<<<< HEAD

7/12
Trying to convert json response into managable data. There is lots of redundent information, got rid of almost all. Also added a week count from 1970 
The rest of the day was about trying to solve git push problems.
A cache file that was deleted does not allow me to push

8/12
Finally fixed the git push problem
Found a function to flatten the json style dictionary. This allows me to get rid of the mbid thing more easily. also changed the variables in the returning API data for easy future access. 
made it possible to add the tracks to a csv file.
spent the rest of the day thinking of how to incorporate this into a suitable database following models.

9/12
Fixed my models so I can fill the Song model objects with the tracks from the json response. Made a function for generating weekly top artists, but this only generates one, where I need multiple for the graphs. Also a function for extracting similar artists, from the artist object database. Later I want to count these and see which artists are present the most while not present in the database. Thereby generating nice recommendations, because this is the 'closest artist' to the users taste. If time permits I will add this as an extra feature.

10/12
Finished functions for loading ArtistWeek and GenreWeek. These Model objects will be the base for my top artists/genres per week for the graphs. Which made my loading functions quite slow. I dont know how I can fix this, other than restructuring my entire database. There is not enough time to do this so I will just work with it.

11/12
Generating graphs with matplotlib was very tedious with underwelming results. Linkning it to the html page is most challenging. I spent the large part of the day trying to fix this problem, without succes. I should have started to look for a new library sooner, but the I was unwilling to give up because of the time I already spent researching this. Tomorrow I will no longer fall in the sunken ost fallacy trap and search for a suitable library.

12/12
Found library plotly which was much easier to implement in Django. I ran into a lot of errors while loading my large Last.fm database. The loading process takes 3-4 hours and errors occur randomly. The most notable error was this one https://stackoverflow.com/questions/16573332/jsondecodeerror-expecting-value-line-1-column-1-char-0, which has no easy solution. My database almost finished loading so I will not risk it right now.

13/12
Did not do much today, visited my grandparents, but was able to finalize the graph section. Uploading to github is still a problem with the large database.

14/12
Finalize graphs, implement Javascript for the 4 different timeframes, had to be javascript so the long loading process is not necessary
and cleant up my code, because the create_plot function in views.py had lots of copy-paste elements. Also did 'some' styling but not much.
Added a feature to see total scrobbles and artists for a last.fm user.
Added another feature so users can download a csv file with their data.
Was thinking about adding more features(like similar artists) but because of the already long loading time I dont think it is a good idea.

=======
>>>>>>> e1998ccd75da3e2b6b01de04b8f14a4c151705b7
