import struct, os
import zlib

#layout for LDZ file:
#
#16 byte file header
#   FCAT (magic id)
#   version (1)
#   filesize
#   entry count
#32 byte descriptor for each entry file
#   mystery number 001014D3 (3541307392) or file type/flags?
#   offset of the data in this file
#   size of the compressed data
#   size of the uncompressed data?
#   filename (16 bytes)
#...
#compressed data
#...

def rebuild(indir, outpath):
    entries = []
    data_blob = bytearray()
    
    utfdir = os.path.join(indir, "utf8")
    rawdir = os.path.join(indir, "raw")

    files = sorted(os.listdir(rawdir))

    header_size = 16 + len(files) * 32
    offset = header_size

    for name in files:
        print("compressing "+name)
        # text_utf = open(f"{utfdir}/{name}", "r", encoding="utf-8", newline="\r\n").read()
        # text_cp = text_utf.encode("cp932")
        text_cp = open(f"{rawdir}/{name}", "rb").read()
        # sjis = text.encode("shift_jis")

        # with open("test_dump_cp.txt", "wb") as f:
        #     f.write(text_cp)

        comp = zlib.compress(text_cp, level=zlib.Z_BEST_COMPRESSION)

        entries.append((3541307392, offset, len(comp), len(text_cp), name))
        data_blob += comp
        offset += len(comp)

    print(f"Parsed {len(entries)} valid entries")
    print(entries)

    with open(outpath, "wb") as f:
        target_size = 290801 #size of TEXT.LDZ in the original ISO, as this file will be smaller and then padded to match
        outsize=16+len(entries)*32+len(data_blob)
        print("writing output file...")
        print("output size: "+str(outsize))
        print("target size: 290801")
        #16 byte header
        f.write(b"FCAT")
        f.write(struct.pack("<I", 1)) #version
        f.write(struct.pack("<I", target_size)) #total filesize
        f.write(struct.pack("<I", len(entries))) #entry count

        #32 byte file descriptor
        for flag, off, csize, usize, name in entries:
            f.write(struct.pack("<IIII", flag, off, csize, usize))
            f.write(name.encode("ascii"))
            f.write(b"\x00" * (16-len(name)))

        f.write(data_blob)
        padding_len = target_size-outsize
        print("padding size: "+str(padding_len))
        f.write(b"\x00" * (padding_len))

        print("output file created")

if __name__ == "__main__":
    rebuild("translation", "TEXT_NEW.LDZ")
