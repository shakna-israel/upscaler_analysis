import time
import math
import json

import cart_repair

import cv2
import numpy as np

def append_horizontal(images):
	max_height = 0
	total_width = 0
	padding = 1

	for image in images:
		image_height = image.shape[0]
		image_width = image.shape[1]

		if image_height > max_height:
			max_height = image_height

		total_width = total_width + image_width

	final_image = np.zeros((max_height, (len(images)-1)*padding + total_width, 3), dtype=np.uint8)

	current_x = 0
	for image in images:
		image_height = image.shape[0]
		image_width = image.shape[1]
		final_image[:image_height,current_x :image_width+current_x, :] = image
		current_x += image_width+padding

	return final_image

def create_row_cart(image):
	height = image.shape[0]
	width = image.shape[1]
	base = cv2.resize(image, (math.floor(width / 10), math.floor(height / 10)), interpolation = cv2.INTER_LANCZOS4)

	r = base.copy()

	height = base.shape[0]
	width = base.shape[1]

	for scale in range(2, 5):
		x = cart_repair.process_frame(base.copy(), scale)
		r = append_horizontal([r, x])

	zeros = np.zeros((height, width * 2, 3), dtype=np.uint8)
	r = append_horizontal([zeros, r])

	cv2.putText(r, "cart_repair", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255, 255), 1)

	return r

def create_row(image, interp=cv2.INTER_CUBIC, text="Cubic"):
	height = image.shape[0]
	width = image.shape[1]
	base = cv2.resize(image, (math.floor(width / 10), math.floor(height / 10)), interpolation = cv2.INTER_LANCZOS4)

	r = base.copy()

	height = base.shape[0]
	width = base.shape[1]

	for scale in range(2, 5):
		x = cv2.resize(base.copy(), (math.floor(width * scale), math.floor(height * scale)), interpolation = interp)
		r = append_horizontal([r, x])

	zeros = np.zeros((height, width * 2, 3), dtype=np.uint8)
	r = append_horizontal([zeros, r])

	cv2.putText(r, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255, 255), 1)

	return r

def process_frame(image):

	cubic_row = create_row(image, cv2.INTER_CUBIC, text="Bicubic")
	nearest_row = create_row(image, cv2.INTER_NEAREST, text="Nearest")
	linear_row = create_row(image, cv2.INTER_LINEAR, text="Linear")
	area_row = create_row(image, cv2.INTER_AREA, text="Area")
	lanczos_row = create_row(image, cv2.INTER_LANCZOS4, text="Lanczos v4")
	cart_row = create_row_cart(image)

	final = cv2.vconcat([cubic_row, nearest_row, linear_row, area_row, lanczos_row, cart_row])

	#cv2.imshow("Base", base)
	#cv2.waitKey()
	#cv2.destroyAllWindows()
	return final

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="Input file (image or video)")
	parser.add_argument("-o", "--output-prefix", help="Output file prefix. (File extension is automatically chosen.)")

	args = parser.parse_args()

	if not args.input:
		raise RuntimeError("Arguments not given.")

	image = cv2.imread(args.input)
	d = process_frame(image)
	cv2.imwrite("{}.png".format(args.output_prefix), d)
