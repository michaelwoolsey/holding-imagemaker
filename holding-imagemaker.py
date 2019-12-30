from PIL import Image, ImageColor

#the names of the file, must be in the current directory
IMAGE_NAME = "base_img.png"
MASK_NAME = "base_img_cutout.png"
INNER_NAME = "input.png"

#try loading each image
try:
	cnt = 0
	im = Image.open(IMAGE_NAME)
	cnt = 1
	im_mask = Image.open(MASK_NAME)
	cnt = 2
	inner = Image.open(INNER_NAME)
except FileNotFoundError:
	passval = 0
	if cnt == 0:
		nm = IMAGE_NAME
	elif cnt == 1:
		nm = MASK_NAME
	else:
		nm = INNER_NAME
		try: #tests if the input image is a jpg instead of a png
			inner = Image.open(INNER_NAME[:-3] + "jpg")
			passval = 1
		except FileNotFoundError:
			nm = INNER_NAME + "/jpg"
	if passval == 0:
		print("hey no image was found with the name " + nm)
		exit()

#ratio of width/height, but multiplied by 1000 and floored
#if its over 1000, the width is larger than the height
#used for the scaling, honestly could probably be removed
xyratio = (inner.size[0]/inner.size[1]) * 1000 // 1

#the dimension of the inner image's sizes in pixels
IM_SIZE = 260
#creates the square image to be placed inside by resizing, cropping, and rotating the input image
inside_img = inner.copy()
if xyratio > 1000:
	inside_img = inside_img.resize((int(xyratio*IM_SIZE/1000)//1, IM_SIZE), Image.BILINEAR)
else:
	inside_img = inside_img.resize((IM_SIZE, int(IM_SIZE*1000/xyratio)//1), Image.BILINEAR)
inside_img = inside_img.crop(((inside_img.size[0] - IM_SIZE)/2, (inside_img.size[1] - IM_SIZE)/2, (inside_img.size[0] + IM_SIZE)/2, (inside_img.size[1] + IM_SIZE)/2))
inside_img_prerotate = inside_img.copy()
inside_img = inside_img.rotate(17,Image.BILINEAR, expand=True)
inside_img.putalpha(Image.new("L", inside_img_prerotate.size, "white").rotate(17, expand=True))

#the pixel position of the placed image on the background image
P1, P2 = 123, 232 

#creates the image the same size as the template and places the inside image in the correct location
bg = Image.new("RGBA", im.size, "rgb(0,0,0)")
bg.paste(inside_img, box=(P1,P2, inside_img.size[0]+P1, inside_img.size[1]+P2), mask = Image.new("L", inside_img_prerotate.size, "white").rotate(17, expand=True))

#the final version of the image, with 
im_final = bg.copy()
im_final.paste(im, mask=im_mask)
im_final.save("image_tests/place_img_test.png")

