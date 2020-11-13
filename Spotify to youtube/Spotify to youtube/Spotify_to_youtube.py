import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Google import Create_Service

# Initializare Api youtube
CLIENT_SECRET_FILE  =  'secret.json'
API_NAME  =  'youtube'
API_VERSION  =  'v3'
SCOPES  = ['https://www.googleapis.com/auth/youtube']
youtube =  Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
osut_playlist_id=['PLK0iyR4xrNXOlKnBW2EnJmL0UFzYU1nui']
#initializare Api Spotify
osut_spotify_id = 'l6z7sjdky5gorstf7p4s2ddx3'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id= 'f2acf923b19e4bbb9ff3017137ef4c58',
                 client_secret= 'de6dcc001d8042f98a950dd441ac2af5'))

      

def afisare_pieseYT(playlist_id):
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId= playlist_id

    )
    nr_piese = 0 
    response = request.execute()
    n = response['pageInfo']['totalResults']
    print(n," Piese \n===========\n")
    if n>50:
       
       while(n > 0):
            if n > 50:
                next = response['nextPageToken']
                x=50
            else: 
                x=n
            for i in range(0,x):
                print(nr_piese,". ",response['items'][i]['snippet']['title'])
                print("    ",response['items'][i]["contentDetails"]['videoId'],"\n")
                nr_piese+=1
            n-=50
            request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            pageToken=next,
            playlistId= playlist_id
            )
            response = request.execute()
            
    else:
        for i in range(0,n):
            print(nr_piese,". ",response['items'][i]['snippet']['title'])
            print("    ",response['items'][i]["contentDetails"]['videoId'],"\n")
            nr_piese+=1

        

def verificare_dubluriYT(playlist_id,video_id):
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId= playlist_id

    )
    nr_piese = 1
    response = request.execute()
    n = response['pageInfo']['totalResults']
    
    if n>50:
       print(n,"\n===========\n")
       while(n > 0):
            if n > 50:
                next = response['nextPageToken']
                x=50
            else: 
                x=n
            for i in range(0,x):
                #print(response['items'][i]["contentDetails"]['videoId'])
                if response['items'][i]['contentDetails']['videoId'] == video_id:
                    print("S-a gasit o dublura la piesa cu nr: ",nr_piese)
                    nr_piese+=1
                    return 0;
            n-=50
            request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            pageToken=next,
            playlistId= playlist_id
            )
            response = request.execute()
            next = response['nextPageToken']
    else:
        for i in range(0,n):
             #print(response['items'][i]["contentDetails"]['videoId'])
             if response['items'][i]['contentDetails']['videoId'] == video_id:
                  print("S-a gasit o dublura la piesa cu nr: ",nr_piese)
                  nr_piese+=1
                  return 0;

     
    return 1
       

def cautare_inserare_pieseYT(nume,playlist_id):
    request = youtube.search().list(
        part = "snippet",
        maxResults = 2,
        q = nume
    )
    responses = request.execute()
    vid = responses['items'][0]['id']['videoId']
    print("id piesa", nume," :", responses['items'][0]['id']['videoId'])
    if verificare_dubluriYT(playlist_id,vid) == 1:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
            "snippet": {
                "playlistId": playlist_id,
                "position": 0,
                "resourceId": {
                "kind": "youtube#video",
                "videoId": vid
                }
            }
            }
        )
        response = request.execute()
        print("Piesa ", nume," a fost adagata cu succes!")
    print('')

def afisare_piese(songs,k,nrplaylist):
    for i in range(0, len(songs)):
        print(k, songs[i]['track']['name'])
        cautare_inserare_pieseYT(songs[i]['track']['name'],osut_playlist_id[nrplaylist])
        k+=1
           
 

def extragere_piese(admin,user,playlist_id,nr_album):
    counter_piese = 0
    playlist = admin.user_playlist_tracks(user, playlist_id,limit = 100,offset = counter_piese )
    print("NR ALBUM",nr_album)
    while len(playlist["items"]) >0:
        songs = playlist["items"];
        afisare_piese(songs,counter_piese,nr_album)
        counter_piese +=99
        playlist = admin.user_playlist_tracks(user, playlist_id,limit = 100,offset = counter_piese )
   

def SpYT():
    results = spotify.user_playlists(osut_spotify_id, 20, 0)
    albums = results['items']
    nr_album=0
    while results['next']:
         results = spotify.next(results)
         albums.extend(results['items'])
    for album in albums:
         print(album['name'],"\n")

    for album in albums:
       print(album['name'])
       print("=====================\n")
       extragere_piese(spotify,osut_spotify_id,album['id'],nr_album)
       print("=====================\n\n")
       nr_album+=1

afisare_pieseYT('PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10')
#==== Codu de aici e de test, pt un singur playlist

#nr_album=0
#results = spotify.user_playlists(osut_spotify_id, 20, 0)
#albums = results['items']
#extragere_piese(spotify,osut_spotify_id,albums[0]['id'],nr_album)
#cautare_inserare_pieseYT(nume,playlist_id)

#=====================

 

