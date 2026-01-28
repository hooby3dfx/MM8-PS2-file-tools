import struct
from PIL import Image, ImageOps

def packbits_decode(data):
    decoded = bytearray()
    i = 0
    while i < len(data):
        n = data[i]
        if n > 127: n -= 256
        i += 1
        if 0 <= n <= 127:
            decoded.extend(data[i:i + n + 1])
            i += n + 1
        elif -127 <= n <= -1:
            fill_byte = data[i:i + 1]
            decoded.extend(fill_byte * (1 - n))
            i += 1
    return decoded

def reconstruct_final(filename, width):
    channels = {0x4B: [], 0x43: [], 0x4D: [], 0x59: []}
    
    with open(filename, 'rb') as f:
        content = f.read()

    i = 0
    while i < len(content):
        if content[i:i+3] == b'\x1b\x28\x41':
            length = struct.unpack('<H', content[i+3:i+5])[0]
            c_code = content[i+5]
            payload = content[i+6 : i+5+length]
            if c_code in channels:
                channels[c_code].append(packbits_decode(payload))
            i += 5 + length
        else:
            i += 1

    height = min(len(v) for v in channels.values() if v)
    stride = (width + 7) // 8

    # Create channels - Initialize as WHITE (0 ink)
    layers = {}
    for code, name in [(0x43,'C'), (0x4D,'M'), (0x59,'Y'), (0x4B,'K')]:
        flat_data = bytearray()
        for row in channels[code][:height]:
            flat_data.extend(row[:stride].ljust(stride, b'\x00'))
        
        # Mode '1' logic: 0 is usually black, 1 is white.
        # We want to map printer bits to 0-255 (ink density)
        img = Image.frombytes('1', (width, height), bytes(flat_data)).convert('L')
        layers[name] = img

    # Merge and Rotate
    cmyk = Image.merge('CMYK', (layers['C'], layers['M'], layers['Y'], layers['K']))
    
    # Rotate and Flip to fix "Bottom-up" and "90-degree" issues
    # Try ROTATE_90 if ROTATE_270 is mirrored
    # final = cmyk.transpose(Image.ROTATE_90) #.transpose(Image.FLIP_TOP_BOTTOM)
    final = cmyk

    # Convert to RGB for screen viewing
    rgb_output = final.convert('RGB')
    rgb_output.save("corrected_render.png")
    print("Check corrected_render.png")

# TODO exact width from stream
reconstruct_final('popegg_dump.bin', width=1275)
