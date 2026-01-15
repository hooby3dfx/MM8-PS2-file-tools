import os, sys
import zlib

def extract(in_path, out_path):
    with open(in_path, "rb") as in_f:
        data = in_f.read()
        data = zlib.decompress(data)

        with open(out_path, "wb") as out_f:
            out_f.write(data)

if __name__ == "__main__":
    extract(sys.argv[1], sys.argv[2])
