import time
import math
import json

import cart_repair

from PIL import Image
import imagehash
import cv2

def process_frame(image, scale):
	pil_im = Image.fromarray(image)
	before_hash = imagehash.whash(pil_im)

	processed = cart_repair.process_frame(image, scale)
	pil_im = Image.fromarray(processed)
	after_hash = imagehash.whash(pil_im)

	diff = before_hash - after_hash
	return diff

def compare_frame(image, scale, interp = cv2.INTER_CUBIC):
	height, width, channels = image.shape
	pil_im = Image.fromarray(image)
	before_hash = imagehash.whash(pil_im)
	
	processed = cv2.resize(image, (math.floor(width * scale), math.floor(height * scale)), interpolation = interp)
	pil_im = Image.fromarray(processed)
	after_hash = imagehash.whash(pil_im)
	
	diff = before_hash - after_hash
	return diff

def process_video(video, scale):
	from matplotlib import pyplot as plt

	diffs = []
	diff_bicubic = [] # cv2.INTER_CUBIC
	diff_nearest = [] # cv2.INTER_NEAREST
	diff_linear = [] # cv2.INTER_LINEAR
	diff_area = [] # cv2.INTER_AREA
	diff_lanczos = [] # cv2.INTER_LANCZOS4

	current_frame = 0
	try:
		while(video.isOpened()):
			ret, frame = video.read()
			if ret:
				frame_start = time.time()

				d = process_frame(frame, scale)
				diffs.append(d)
				print("Diff: {}".format(d))

				d = compare_frame(frame, scale, interp = cv2.INTER_CUBIC)
				diff_bicubic.append(d)
				print("Diff Bicubic: {}".format(d))

				d = compare_frame(frame, scale, interp = cv2.INTER_NEAREST)
				diff_nearest.append(d)
				print("Diff Nearest: {}".format(d))

				d = compare_frame(frame, scale, interp = cv2.INTER_LINEAR)
				diff_linear.append(d)
				print("Diff Linear: {}".format(d))

				d = compare_frame(frame, scale, interp = cv2.INTER_AREA)
				diff_area.append(d)
				print("Diff Area: {}".format(d))

				d = compare_frame(frame, scale, interp = cv2.INTER_LANCZOS4)
				diff_lanczos.append(d)
				print("Diff Lanczos v4: {}".format(d))
				
				print("Frame {} took {} seconds.".format(current_frame, math.floor(time.time() - frame_start)))
				current_frame = current_frame + 1
			else:
				break
	except KeyboardInterrupt:
		pass

	plt.plot(diffs, label="Upscaler")
	plt.plot(diff_bicubic, label="Bicubic")
	plt.plot(diff_nearest, label="Nearest Neighbour")
	plt.plot(diff_linear, label="Linear")
	plt.plot(diff_area, label="Area")
	plt.plot(diff_lanczos, label="Lanczos v4")
	plt.legend()
	plt.savefig('diffs.png')

	with open('diffs.json', 'w+') as openFile:
		openFile.write(json.dumps({"upscaler": diffs, "bicubic": diff_bicubic, "nearest": diff_nearest, "linear": diff_linear, "area": diff_area, "lanczos4": diff_lanczos}))

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="Input file (image or video)")
	parser.add_argument('-s', "--scale", help="Scale to increase by", default=2.0, type=float)

	args = parser.parse_args()

	if not args.input:
		raise RuntimeError("Arguments not given.")

	if args.scale < 1.0:
		raise RuntimeError("Scale less than 1.0 not supported. This is an upscaling algorithm. Not downscaling.")

	if args.scale > 3.0:
		print("WARNING: Upscaling above 3.0 may return poor results.")

	print("SCALE:", args.scale)

	import mimetypes

	if 'image' in mimetypes.guess_type(args.input)[0]:
		image = cv2.imread(args.input)
		d = process_frame(image, args.scale)
		print("Diff: {}".format(d))
	else:
		video = cv2.VideoCapture(args.input)
		fps = int(video.get(cv2.CAP_PROP_FPS))
		frame_width = int(video.get(3))
		frame_height = int(video.get(4))

		process_video(video, args.scale)
