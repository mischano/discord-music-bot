import bot
import spotify

if __name__ == '__main__':
    """
    token = spotify.get_token()
    artist = spotify.search_for_artist(token, "ACDC")
    artist_id = artist["id"]
    songs = spotify.get_songs_by_artist(token, artist_id)
    
    for i, song in enumerate(songs):
        print(f"{i + 1}. {song['name']}")
    """

    bot.run()
