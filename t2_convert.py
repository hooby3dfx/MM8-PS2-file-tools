import sys, os
import struct
import argparse

from PIL import Image



def read_palette_32_linear(data, num_colors):
	palette = []
	pal_offset = 0
	for i in range(num_colors):
		ix = i*4
		#RGB8888?
		r = (data[ix])
		g = (data[ix+1])
		b = (data[ix+2])
		# a = data[ix+3] #always 0x80 (128)
		a = 255

		palette.append((r,g,b,a))

	return palette

#https://github.com/bartlomiejduda/ReverseBox/blob/main/reversebox/image/swizzling/swizzle_ps2.py
def _convert_ps2_palette(palette_data: bytes, bpp: int) -> bytes:
	if bpp == 32:
		bytes_per_palette_pixel: int = 4
	elif bpp == 16:
		bytes_per_palette_pixel: int = 2
	else:
		raise ValueError(f"Bpp {bpp} not supported!")

	converted_palette_data: bytes = b""
	# palette_handler = BytesHandler(palette_data)

	parts: int = int(len(palette_data) / 32)
	stripes: int = 2
	colors: int = 8
	blocks: int = 2
	index: int = 0

	for part in range(parts):
		for block in range(blocks):
			for stripe in range(stripes):
				for color in range(colors):
					palette_index: int = (
						index
						+ part * colors * stripes * blocks
						+ block * colors
						+ stripe * stripes * colors
						+ color
					)
					palette_offset: int = palette_index * bytes_per_palette_pixel
					# palette_entry = palette_handler.get_bytes(palette_offset, bytes_per_palette_pixel)
					palette_entry = palette_data[palette_offset: palette_offset+bytes_per_palette_pixel]
					converted_palette_data += palette_entry

	return converted_palette_data


def t2_convert(in_path):
	with open(in_path, "rb") as f:
		header = f.read(16)

		width, height = struct.unpack_from("<HH", header, 12)
		t1, t2 = struct.unpack_from("<BB", header, 2)

		# raw = f.read()

		if t1 == 81: #'Q'
			palette_size = 16 #4bpp
			width_align = 16
		elif t1 == 83: #'S'
			palette_size = 256 #8bpp
			width_align = 8
		else:
			print("Not T2 Q/S")
			return

		print(f"Image dimens raw: {width}x{height}")
		# if width==16728 and height==16728:
		# 	width=344
		# 	height=344
		if width>6000:
			mask = 0x01FF
			width = width & mask
			height = height & mask
			print(f"Image dimens bit masked: {width}x{height}")

		if width % width_align:
			width += width_align-width%width_align
		print(f"Image dimens aligned: {width}x{height}")

		print(f"Pixel ct: {width*height}")

		# print(f"Raw data size: {len(raw)} bytes")
		print(f"File size: {os.path.getsize(in_path)} bytes")

		print(f"Header t1: {t1}")
		print(f"Header t2: {t2}")


		print(f"Palette size: {str(palette_size)} colors")

		clut_data = f.read(palette_size*4)
		print(f"CLUT data size: {len(clut_data)} bytes")

		if palette_size == 16:
			pixel_data = f.read(width*height//2)
		else:
			pixel_data = f.read(width*height)
			clut_data = _convert_ps2_palette(clut_data, 32)

		print(f"pixel_data length: {len(pixel_data)}")

		palette = read_palette_32_linear(clut_data, palette_size)		

		print("Palette:")
		print(palette)

		if palette_size == 16:
			# deswizzle?
			# pixel_data = _ps2_unswizzle4(pixel_data, width, height)
			# pixel indexing for 4bpp
			indices = []
			for i in range(width*height):
				b = pixel_data[i // 2]
				if i & 1:
					# indices.append(b & 0x0F)
					indices.append(b >> 4)
				else:
					indices.append(b & 0x0F)
					# indices.append(b >> 4)

			# print(len(indices))
			# print(indices)

		else:
			#pixel indexing for 8bpp
			indices = pixel_data

		pixels = [palette[i] for i in indices]


		img = Image.new("RGB", (width, height))
		img.putdata(pixels)

		# img.save("T2OUT.png")
		newname = "t2convert/"+os.path.basename(f.name) + "_out.png"
		img.save(newname)

		print("Saved "+newname)



def convert_bmp_to_t2(t2_path, bmp_path):

	img = Image.open(bmp_path)

	# Get the palette (returns a flat list [R,G,B,R,G,B...])
	if img.mode == 'P':

		colors = 256 #16

		# palette_og = img.getpalette()
		
		# Get pixel indexes as a list
		# pixel_indexes_og = list(img.getdata())

		# print("bmp palette (initial):")
		# print(palette)

		# print("bmp pixel_indexes:")
		# print(pixel_indexes)

		if colors == 16:
			# Quantize to 16 colors
			# colors=16: The target number of colors
			# method=2: Uses the 'libimagequant' (high quality) if available, or median cut
			# dither=1: Keeps transitions smooth (set to 0 for flat colors)
			image_bpp = img.quantize(colors=16, method=2, dither=1)
		else:
			image_bpp = img
			

		palette = image_bpp.getpalette()
		
		pixel_indexes = list(image_bpp.getdata())

		#PS2 "RGB8888" format
		ps2_palette = []
		for i in range(colors):
			ix=i*3
			r = palette[ix+0]
			g = palette[ix+1]
			b = palette[ix+2]
			a = 128 #alpha 0x80
			ps2_palette.append((r,g,b,a))

		ps2_palette_bytes = bytearray()
		for color in ps2_palette:
			ps2_palette_bytes += bytes(color)

		if colors == 256:
			#swizzle the palette!!!
			print("swizzling palette... ")
			ps2_palette = _convert_ps2_palette(ps2_palette_bytes, 32)


		print("ps2_palette:")
		print(ps2_palette)


		# canvas_width = 112
		# canvas_height = 37
		canvas_width = 112
		canvas_height = 32

		canvas = Image.new('P', (canvas_width, canvas_height))
		canvas.putpalette(palette)#needed??
		canvas.paste(image_bpp, (0, 0))

		canvas.save(f'bmp-{colors}-out.bmp')
		
		#create T2:
		#header:
		#	T2XX
		#	padding
		#	dimens
		#palette
		#indexes
		#file size and properties must match the original T2

		#basic approach - surgically insert the bytes from provided bmp into the T2 
		#for palette & pixel indexes
		with open(t2_path, "rb") as tf:
			t2header = tf.read(16)
			t2_blob = bytearray()
			
			t2_blob += t2header
			t2_blob += ps2_palette
			indices_8bpp = bytes(canvas.getdata())
			# print(list(canvas.getdata()))

			if colors == 16:
				for i in range(0, len(indices_8bpp), 2):
					p1 = indices_8bpp[i]
					# Handle odd-numbered total pixels by using 0 as a placeholder
					p2 = indices_8bpp[i+1] if (i+1) < len(indices_8bpp) else 0
					
					# print(p1)
					# print(p2)

					# Pack p1 into the high nibble and p2 into the low nibble
					packed_byte = (p1 << 4) | (p2 & 0x0F)
					# print(packed_byte)
					t2_blob.append(packed_byte)
			else:
				t2_blob += indices_8bpp
			

			outpath = 'bmpt2out'
			with open(outpath, "wb") as of:
				of.write(t2_blob)
				print("Saved "+outpath)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
					prog='ProgramName',
					description='Parses T2 image files and/or converts BMP to T2',
					epilog='Have a nice day!')

	parser.add_argument('filename') #T2 file to be converted
	parser.add_argument('-b', '--bmp')#, action='store_true') #input bmp

	args = parser.parse_args()

	if args.bmp:
		convert_bmp_to_t2(args.filename, args.bmp)

	else:
		t2_convert(args.filename)



