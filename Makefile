default:
	echo "To download a file use :____"
	echo "To convert your video to hex, use _______"

download:

	retrieve_video.py $(ARGS)
	ffmpeg -i $(ARGS) -vf scale=16:16 out.mp4
	rm -r bin
	rm -r hex

	ffmpeg -i "out.mp4" -f image2 "bin/%05d.png"

	video_to_bits.py 'out.mp4'