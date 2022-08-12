# AudioVis - Your real-time python music visualizer!
WARNING! This is not finished at all! A lot of the stuff I wrote here is just stuff I planned to add.
Only use this if you know how to. I won't be giving any support at the current state. I also don't know if I'll ever finish this.


Since you can use full python to make effects, you can use this on every device.
If it's just a laptop screen or a full beamer, doesn't matter.

(Well actually, if you have a beamer and a fog machine you can make light shows. Looks pretty cool)

There are some pre-made effects if you just want to use it to impress your friends with lightshows.
The thing is, if you are not that good at this kinda stuff, getting this app to run might be a problem.

If you are still reading this, I guess you do want to use this.
Well here is how to install it:

First, install python.
Then you need to install 5 modules. Kivy, Numpy, Scipy, PyGame and PyAudio.
Since PyAudio is weird:
For pyaudio on linux, install python3-pyaudio or something like that.
For pyaudio on windows, open your cmd and type "pip install pipwin" and then "pipwin install pyaudio"
No idea about mac. I found this, but can't try it as I don't own a mac.
https://stackoverflow.com/questions/33851379/how-to-install-pyaudio-on-mac-using-python-3

Now, you need to have your sound output be a mic input.
There are many ways to do this.
First, the manual way. You take an aux cable and just connect the audio out and input, maybe also get an aux splitter.
Second, if you are on windows, I recommend using VoiceMeeter or Soundux.
Third, for linux, I really recommend Soundux. You just select python as the output and press Pass Through.
you could also use Jackaudio. I didn't try it but I saw some people get that to work,
And Fourth, if none of those worked for you, well you need to look on google for an answer.
Phrases that might help you are: Virtual sound cable, source to sink audio, system audio as microphone.
I have no idea about mac so... You can look if Soundux works on mac. Yeah I really love Soundux. It's just useful.
But if none of that worked and you really need this app, I suggest using MusicBeam. https://www.musicbeam.org/
It does about the same thing, but more oriented for beamers.
But if you really, really want to use this one, I guess you can just connect a mic.
Just hang that in front of the speaker and it should work, but keep in mind, it also picks up other noises.
If any of you find better ways to do this, please tell me

Now that you've come so far, there is not a lot left. Just download the app and start the .py file.
You will get a selection of devices. Use the one that you just set up for this.

Well now you have used the app a bit, and want to make your own effects.

Okay so to make an effect you need to make a folder in the "Effects" directory.
The folder can have any name you want.

In that folder you need to make a python script. (.py).
The name of that script will be the name of the effect.
(The first letter will be automatically capitalized)

In the python script you need to have an "Effect" class.
It has to have these 3 functions:
- "start"     | Executes when your effect is started
This one has to take 3 arguments. In. The. Correct. Order!
1: The pygame screen
   (Class: You know. The pygame screen.)
2: The width of the screen
   (Int: The width.)
3: The height of the screen
   (Int: The height)

- "stop"      | Executes when your effect is stopped.

And the most importand one:
- "update"
This one has to take 10 arguments. In. The. Correct. Order!
1: The pygame screen
   (Class: You know. The pygame screen.)
2: The width of the screen
   (Int: The width.)
3: The height of the screen
   (Int: The height)
4: The raw audio data
   (pyaudio.paInt16, 1 channel, 44100 KHz. Yeah It's some pyaudio format. Don't wanna explain, just google it.)
5: The frequencies and their volume
   (List: Just a range of frequencies. No idea which. You'll figure it out.)
6: Overall volume
   (Int: Just the volume you know. (0 to 255))
7: The PEAK beat detection
   (Boolean: True if there is a beat at the moment, False if not.)
8: The BASS beat detection
   (Boolean: True if there is a beat at the moment, False if not.)
9: The MID beat detection
   (Boolean: True if there is a beat at the moment, False if not.)
10: The HIGH beat detection
   (Boolean: True if there is a beat at the moment, False if not.)

Optionally, you can also have an __init__ function, but you don't need to.

Now for the beat detection. Bass, Medium and High are oriented to work on those frequencies,
but they also activate on others. It creates some diversity and well I found no way to easily change that. Deal with it.
If you want to detect Bass beats, Bass does that good, but Peak does it better. Personal Preference I guess.
And High rarely triggers. It's just like an extra. It triggers in quiet sections a lot. Well you'll find something.
Honestly. Use Peak for all the normal effects. The rest for special effects or cool stuff that doesn't happen a lot.

After that, you can just go ahead. Just use pygame.
BUT, don't create any screen or quit any screen.
You can import pygame and you get the screen through the update function.
Else, it would just break the window and that's no fun.
Otherwise, you can do anything you want.

By the way, The window is resizable and when you press "F11" it toggles between fullscreen and windowed.
Also, by pressing "r", you can restart the current effect. That's useful when you resize the screen.

Just some ideas:
- A game that changes to music OR to your voice
- Simple moving shapes that change color and speed to music
- A discord bot that puts messages on screen and they move to the music
- A camera that films you and adds video effects to the music
- Maybe even, an AI that finds out the song using the raw audio stream and shows the lyrics. LIVE!

You get the point. You can make cool stuff to live music that you can use a parties and more.
You can just start making effects without having to worry about the interface and beat detection.
Really, it took me a long time to figure everything out to make it work. You don't need to go through that headache.

Also, you can always look at the pre-made effects if you need some help.

Finally, stuff that you can use because why not:
- You can import src.utility.mprint
  That function not only prints it to console, but also to the main window.

And a little word at the end:
This is inspired by MusicBeam. I used that to make lightshows for some time, but I just kind of wanted more.
MusicBeam is made in processing and I have no experience in that. So I decided to make my own version in python.
Also, MusicBeam is old and rarely updated and I can barely find any community online. Can't find extra effects online.
I wanted this to be more advanced. MusicBeam is simple and everyone can easily use it. This is for if you know how to.
It's like a step up. If you don't have experience in python, it honestly makes more sense to use MusicBeam.
It's a great piece of software. I really like it and will still use it when I'm too lazy to set all of this up.

And well Licensing and copyright stuff goes here:
Yeah basic stuff like always. You are allowed to use this however you want, Modify whatever you want.
You are not allowed to distribute this as your own.
You do not get any warranty. I am just putting this thing out and am not liable for anything
If you agree to this, well go ahead and download it. Else, Well don't download it then I guess.

## More projects: https://zohiu.de/projects/  
