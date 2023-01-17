# Design Doc

## Features
the features of the minimum viable product are:
- general overview of most listened artists and their genre on Last.fm
- general overview of the most prominent artists within a genre, through the years
with a last.fm username you can:
- check out your general streaming history
    - of genres
    - of top 10 artists
each of the graphs should display extra information on mouseover. 
For the genres that would be the top artists, number of scrobbles and period.
For the top artist that would be the number of scrobbles and period


## Databases and techniques
[Last.fm API](https://www.last.fm/api) 
data visualisation tools -TODO
Javascript for interactive graph design (depends on visualisation tool)

## Url paths
### /index/
this is the starting page where you can fill in your [Last.fm](https://www.last.fm/) username and the program will download your data from the API.
form - here you are able to fill in your last fm account for retrieving your data.
'get my data' - button to submit your last fm name
'log in'/'register' - links to forms that handle registration and loging in
----- if logged in -----
'create my plot'- link to the graph page (/create_plot/)
'log out' - link to log out, redirects to index page

### /create_plot/
generates graphs for the user that is present.
in the top [part](doc/top_graphs.png) you can see generic information 
'Download csv file' - an option to download your data in csv format.
These [graphs](doc/project_grafiek.gif) are interactive and show 4 different timeframes.
You can navigate through the timeframes using the buttons: '4 weeks(default)','half year', 'year', 'all time'

You can double click any genre or artist to view a single plot instead of the cumulative graph.
[seen here](doc/project_grafiek.gif)

## /login/ and /register/
generic login and register forms for creating and login in to an account.
