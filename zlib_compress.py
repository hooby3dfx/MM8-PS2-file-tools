import os, sys
import zlib

def compress(in_path, out_path):
    with open(in_path, "rb") as in_f:
        data = in_f.read()

        #See Z_BEST_SPEED (1), 
        #Z_BEST_COMPRESSION (9), 
        #Z_NO_COMPRESSION (0),
        #Z_DEFAULT_COMPRESSION (-1) for more information about these values.

        comp = zlib.compress(data, level=zlib.Z_BEST_COMPRESSION)

        

        with open(out_path, "wb") as out_f:
            out_f.write(comp)

            target_size = 3346#1330
            padding_len = target_size-len(comp)
            print("padding size: "+str(padding_len))
            out_f.write(b"\x00" * (padding_len))

if __name__ == "__main__":
    compress(sys.argv[1], sys.argv[2])
