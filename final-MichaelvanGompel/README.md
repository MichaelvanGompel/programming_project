# Streams flow

Interactive graphs for users of [Last.fm](https://www.last.fm). 
Aside from generic artist information there is also a function for users to explore their own listening tendencies.
For instance seeing how the most listened genres evolved through time according to changing music taste.

## Problem statement

Last.fm is a site which tracks your music, allowing you to track your listening tendencies.
The site itself gives you graphs and numbers about your listening tendencies.
However, these graphs are lacking in depth for which the site used to lean heavily on community driven projects.
These projects are now outdated due to changes in the site and API.
My project is a kind of revival of these initiatives, giving the Last.fm users interactive graphs for their listinging history. 

An example of such a site is [explr](https://mold.github.io/explr/) where you can see from what countries artists come from and get an global overview of your listening history.
[Spelunke](https://github.com/sumeet-bansal/last.fm-spelunkerr) has programs for artists and scraping last.fm but is not user friendly or has genres implemented.

## Solution description

Using the [Last.fm API](https://www.last.fm/api) information about the artists, albums and their genres can be retrieved.
Coupling this to the Listening history of an user, we can generate graphs displaying this history in a more detailed manner.

## Details and sketches

[general outline](doc/general_outline.jpg)

Most challenging will be extracting user data and creating (interactive) graphs with that data. 
This is new for me and will require Java, a language im not familiar with yet. 

Make sure that this readme is well-readable when viewed via GitHub! Images should be appropriately sized, text and images should be clearly related etc.

[database diagram](doc/database_diagram.jpg)

[UI sketch](doc/streams_flow.png)

[screen cast](https://video.uva.nl/media/0_yey6lahw)
