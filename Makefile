default:
	echo "To download a file use :____"
	echo "To convert your video to hex, use _______"

download:

	rm in.mp4
	python3 retrieve_video.py $(ARGS)
	ffmpeg -i in.mp4 -vf scale=16:16 out.mp4
	rm -r bin
	rm -r hex
	mkdir bin
	mkdir hex
	ffmpeg -i "out.mp4" -f image2 "bin/%05d.png"
	python3 video_to_bits.py