import struct, os, sys
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

def read_u32(f):
    return struct.unpack("<I", f.read(4))[0]

def extract(path, outdir):
    with open(path, "rb") as f:
        assert f.read(4) == b"FCAT"
        version = read_u32(f)
        file_size = read_u32(f)
        entry_size = read_u32(f)

        entries = []

        while True:
            block = f.read(32)
            if len(block) < 32:
                break

            # Mixed endian?
            mystery = struct.unpack("<I", block[0:4])[0]    # mystery number/flag?
            offset = struct.unpack("<I", block[4:8])[0]  # offset
            csize = struct.unpack("<I", block[8:12])[0] # len - compressed
            usize = struct.unpack("<I", block[12:16])[0] # len - decompressed

            name = block[16:32].split(b"\x00", 1)[0]
            if not name:
                break
            # print(name)
            try:
                name = name.decode("ascii")
            except UnicodeDecodeError:
                print(name)
                break

            entries.append((mystery, offset, csize, usize, name))

        print(f"file_size={file_size}")
        print(f"entry_size={entry_size}")
        print(f"Parsed {len(entries)} valid entries")
        print(entries)

        os.makedirs(outdir + "/enc", exist_ok=True)
        os.makedirs(outdir + "/raw", exist_ok=True)
        os.makedirs(outdir + "/utf8", exist_ok=True)

        for mystery, offset, csize, usize, name in entries:
            print("extracting "+name)
            print("offset "+str(offset))
            f.seek(offset)
            print("length "+str(csize))
            data = f.read(csize)
            # print("data enc "+str(data))
            enc_path = f"{outdir}/enc/{name}"
            with open(enc_path, "wb") as ef:
                ef.write(data)

            try:
                data = zlib.decompress(data)
                # print("data dec "+str(data))

                raw_path = f"{outdir}/raw/{name}"
                utf_path = f"{outdir}/utf8/{name}"

                with open(raw_path, "wb") as rf:
                    rf.write(data)

                with open(utf_path, "w", encoding="utf-8") as uf:
                    uf.write(data.decode("cp932"))
            except:
                print("error on "+name)

if __name__ == "__main__":
    # extract("TEXT.LDZ", "out")
    extract(sys.argv[1], sys.argv[2])
