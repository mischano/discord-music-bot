Discord Music Bot - plays music in a discord server. 

LIST OF COMMANDS: 
Join: 
    * If caller is not in the vc, signal message.
    * If caller is in the vc:
        * If bot is not in the vc, connect the bot.
        * If bot is in the vc:
            * If bot is by itself in a different vc, re-connect to callers vc.
            * If bot is not by itself in a different vc, signal message.
            * If bot is in the same vc as the caller, do nothing. 

Quit:
    * If caller is not in the vc:
        * If bot is not in the vc, signal message.
        * If bot is by itself in the vc, disconnect bot.
        * If bot is not by itself in the vc, signal message.
    * If caller is in the vc:
        * If bot is not in the vc, signal message.
        * If bot is by itself in the different vc, disconnect bot.
        * If bot is in the same vc as the caller, disconnect bot. 
        * If bot is not by itself in the different vc, signal message.
        
Play:
    * If caller is not in the vc, signal message. 
    * If caller is in the vc:
        * If bot is not in the vc, connect & play.
        * If bot is by itself in the different vc, re-connected to callers vc & play.
        * If bot is not by itself in the different vc, signal message. 
       
Pause:
    * If caller is not in the vc:
        * If bot is not in the vc, signal message.
        * If bot is in the vc, signal message.
    * If caller is in the vc:
        * If bot is not in the vc, signal message.
        * If bot is in the different vc, signal message.
        * If bot is in the same vc as the caller:
            * If bot is playing music, pause the music.
            * If bot is not playing music, signal message. 

Resume:
    * If caller is not in the vc: 
        * If bot is not in the vc, signal message.
        * If bot is in the vc, signal message. 
    * If caller is in the vc: 
        * If bot is not in the vc, signal message. 
        * If bot is in the different vc, signal message. 
        * If bot is in the same vc as the caller: 
            * If bot is paused, resume the music.
            * If bot is not paused, signal message. 

Current:
    * If bot is not in the vc, signal message.
    * If bot is in the vc: 
        * If bot is playing/paused, display the song.
        * If bot is inactive, signal message. 

List:
    1. Bot is not connected to vc, signal message.
    2. Bot is connected to vc:
        * Song list is empty, signal message.
        * Song list is not empty, show list.

Skip:
    * If caller is not in the vc, signal message. 
    * If caller is in the vc: 
        * If bot is not in the vc, signal message.
        * If bot is in the vc:
            * If bot is the different vc, signal message.
            * If bot is in the same vc as the caller:
                * If playlist is empty, signal message. 
                * If playlist is not empty, skip the current song: 

Remove: 
    * If caller is not in the vc, signal message. 
    * If caller is in the vc:
        * If bot is not in the vc, signal message.
        * If bot is in the vc: 
            * If the playlist is empty, signal message.
            * If playlist is not empty:
                * If song number is out of range, signal message.
                * If song number is in range, remove the song from the playlist. 

Shuffle:
    * If caller is not in the vc, signal message.
    * If caller is in the vc:
        * If bot is not in the vc, signal message.
        * If bot is in the vc: 
            * If the playlist is empty, signal message.
            * If the playlist is not empty, shuffle the songs. 
  
Helpme:
    * Display the bot commands. 