## Reviewers: Joris en Sander

## Functies samenvoegen 

Er zijn verschillende functies die een vergelijkbare functie vervullen.
Voor genres en artiesten bijvoorbeeld, moet ik vergelijkbare acties ondernemen. Zo moet ik bij het inladen van mijn data voor zowel genres als artiesten objecten aanmaken. 
Ook maak ik vergelijkbare grafieken voor beide objecten.
Voor genres en artiesten doe ik dus vaak een vergelijkbare behandeling.
zie hieronder ee
Destijds wist ik niet hoe ik die kon samenvoegen, maar wist wel dat het kon.
Voorbeeld:
```bash
  def artists_for_graph(top_artists, start_frame, end_frame):
    """ generate a list of artists plays and their names suitable for graph initialization"""
    names_artists = []
    list_artists = []
    # iterate over the top artists and 
    for artist in top_artists:
        names_artists.append(artist.artist_name) 
        temp_list = []
        for week_number in range(start_frame, end_frame):
            try:
                this_week_plays = ArtistWeek.objects.get(week_number=week_number, artist=artist)
                temp_list.append(this_week_plays.artist_plays)
            except ObjectDoesNotExist:
                temp_list.append(int(0))
        list_artists.append(temp_list)
    result = [names_artists, list_artists]
    return result

def genres_for_graph(top_genres, start_frame, end_frame):
    names_genres = []
    list_genres = []
    for genre in top_genres:
        names_genres.append(genre.genre_name)
        temp_list = []
        for week_number in range(start_frame, end_frame):
            try:
                this_week_plays  = GenreWeek.objects.get(week_number=week_number, genre=genre)
                temp_list.append(this_week_plays.genre_plays)
            except ObjectDoesNotExist:
                temp_list.append(int(0))
        list_genres.append(temp_list)
    result=[names_genres, list_genres]
    return result
```
Achteraf zijn er twee opties om dit te bewerkstelligen. Een daarvan is om een kleine subfunctie te maken die als argument 'genre' of 'artist' neemt en dan afhankelijk daarvan de juiste bewerking doet. Een andere optie is itereren over een lijst van 'genre'en 'artist' omdat deze twee nooit afzonderlijk nodig zijn.

## javascript
Ik heb minimaal gebruik gemaakt van javascript, het enige waar ik het voor gebruikt heb is het weergeven van mijn 4 paar grafieken.Wat ik eigenlijk nog had moeten veranderen was de onclick attribute die ik heb in mijn button:
```bash
  <button class="btn btn-sm btn-outline-primary" onclick="set_visibility('year')">Year</button>
```
Daarin heb ik dus een verwijzing naar een javascript functie. Een betere oplossing was geweest om een ```addEventListener()``` toe te voegen. Zo houd ik mijn javascript puur in de javascript file.
Had de tijd het toegestaan had ik nog meer javascript functionaliteiten geïmplementeerd. Omdat het laden van de database en het laden van de grafieken beide een intensief en langdurig proces is had ik dit beter moeten weergeven. Het laad icoon in de chrome tabblad is het enige die een indicatie geeft van het laadproces. Javascript was hiervoor een uitkomst geweest. Een laadscherm en/of een laadbalk had dit voor de gebruiker een stuk prettiger gemaakt.


## formatting en file assignment is niet consistent 
Een punt wat bij mijn code altijd blijft terugkomen is de formatting. Ik ben inconsistent met het gebruiken van witregels en daardoor bevat mijn code grote blokken code. 
Bijvoorbeeld:
```bash
  with open('data.txt', 'a') as outfile:
        for begin, end in charts:
            payload['from'] = begin
            payload['to'] = end
            response = get_lastfm(payload, user)
            if response.status_code != 200:
                print('something went wrong')
                return 0
            outfile.write(json.dumps(response.json()))
            outfile.write(",")
            weekly_top_ten.append(response.json())
            time.sleep(0.25)
            print(f'week {count} of {total_weeks}')
            count +=1
    return weekly_top_ten
```
Witregels rondom if-statements en for-loops zou bovenstaand stuk code een stuk leesbaarder maken.

Daar komt nog bij dat dit stuk code eigenlijk ook helemaal niet gebruikt wordt.
Dit hoort namelijk bij een functie die ik er nog in heb staan voor de toekomst. Deze functies had ik beter kunnen plaatsten in een aparte file waar ik deze groep verzamel.
Ook had ik een aparte file kunnen maken die de API requests maakt en functies die daarmee te maken hebben.

Zo wordt deze grote util.py file een stuk duidelijker omdat er alleen functies in staan die daadwerkelijk direct effect hebben op de user experience.

## 2 model objecten niet nodig bij goede logica
Een klein puntje van en voor mezelf is dat ik denk twee overbodige model objecten te hebben. Het betreft de objecten ArtistWeek en GenreWeek. Het aanmaken van deze model objecten werd geadviseerd vanuit de hands omdat ik dan makkelijker grafieken op kan zetten. In de grafieken bekijk ik per week de meest voorkomende artiesten en genres. 
Wat me een beetje tegen staat is dat al de benodigde info in principe al aanwezig is in de database. Ik wist en weet alleen niet hoe ik deze op een handige manier kon omzetten naar de lijsten die ik voor de grafieken nodig heb.

## laatste ontwikkelingsfase niet goed vervuld
In de laatste fase maak je over het algemeen je programma gebruiksvriendelijker. Door de tijdstress ben ik hier helaas niet aan toe gekomen. Hieronder een aantal dingen die ik graag had verbeterd.
Weinig aandacht is besteed aan het opvangen van errors. Zo levert het invullen van een verkeerde Last.fm account naam een KeyError op, maar deze wordt niet opgevangen. Dit is slechts een enkel voorbeeld want ik heb niet mijn best gedaan het programma te 'breken' en zo meer mogelijke bugs te achterhalen.
Ook is er geen rekening gehouden met het verkleinen/vergroten van het window. Door middel van '@media' en de ingebouwde functionaliteiten van bootstrap had ik de grafieken in sommige gevallen beter kunnen weergeven.

Veel van deze problemen komen voort uit het feit dat ik de 'scope' van mijn project niet goed in kaart had gebracht. Ik dacht dat mijn project redelijk modulair was en dat het toevoegen en verwijderen van functionaliteiten daarmee redelijk makkelijk was. Dit bleek dus niet zo te zijn. Het grootste deel van mijn tijd heb ik besteed aan het verwerken van de data van de API. Mocht dit niet gelukt zijn had ik niks om op terug te vallen. En extra functionaliteiten had ik geen ruimte voor omdat het 'minimal viable product' nu al veel te veel tijd kost om te laden. Extra functionaliteiten zouden dit verergeren.
