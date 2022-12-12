from flask import Flask, Response, url_for, render_template, redirect, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def recommendations():

    if request.method == "POST":
        if request.form['input_type'] == 'search':
            query = request.form['query']
            results = redis_client.get(query)
            if results is None:
                print("Not in cache")
                sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e54b28b15f574338a709fdbde414b428",
                                                                    client_secret="7dead9452e6546fabdc9ad09ed00f172"))
                results = sp.search(q=query)
                redis_client.set(query, json.dumps(results))
            else:
                print("Found in cache")
                results = json.loads(results)
            
            track_names = []
            for idx, track in enumerate(results['tracks']['items']):
                song = track['name']
                artist = track['album']['artists'][0]['name']
                track_names.append([song, artist])

            return render_template('recommendations.html', track_names=track_names)
        elif request.form['input_type'] == 'recommendations':
            selected_songs = []
            for i, k in enumerate(request.form.keys()):
                if i == 0:
                    continue
                selected_songs.append(k)
            
            ### Write code for getting recommendations from selected songs
            ### CURRENTLY PASSING DUMMY DATA

            recommendations = selected_songs

            return render_template('recommendations.html', recommendations=recommendations)    

    return render_template("recommendations.html")



if __name__ == "__main__":
    app.run(debug=True)