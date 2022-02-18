# Team Bad Apple – Stuy Hacks 2022

## Roster: Ishraq Mahid, Kellen Yu

### Project Links
Hackathon Submission: https://devpost.com/software/making-a-computer-to-play-bad-apple
Results: https://www.youtube.com/watch?v=w_mW0DWru-A
### Inspiration
We learned a lot about the basics of computers from the Ben Eater 8 bit CPU playlist:
https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU
Bad Apple!:
https://www.youtube.com/watch?v=FtutLA63Cp8



## Requirements:
* ffmpeg is installed
* using a UNIX system
* youtube-dl is installed
* python and java is installed
* can run Makefiles

## Use:
Open the virtual environment within this repo through the following: ```. ~/path/to/repo/video_conversion/bin/activate

Run ```sudo Make download ARGS='{url_to_video_desired}'```

Ex: ```sudo Make download ARGS='https://www.youtube.com/watch?v=EGohSsaCJOU'```

## How do use to computer itself (opening the .dig files)
First you need to download Digital logic sim: https://github.com/hneemann/Digital

After setting it up, there are 2 .dig files inside of the directory Digital

BadApple.dig - The computer modified to play "Bad Apple!"
  -> If you want to speed up the video, increase the clock frequency
  -> Loading the badapple.hex into the 5 ROMS (top to bottom) will load the data.

YU1v2.dig - The original computer without modificiations
  -> By editing the ROM (the one next to the RAM) you can write small programs for this computer
  -> If you address a value above 32767, you will acsess RAM. Below that value are addresses to ROM.
  
 OPCODES can be found in OPCODES.py
 Running OPCODES.py will write to a file that contains the opcode data that the computer uses.



