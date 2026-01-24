import os, sys
import zlib
import argparse

def compress(in_path, out_path, target_size=None):
    with open(in_path, "rb") as in_f:
        data = in_f.read()

        #See 
        #Z_BEST_SPEED (1), 
        #Z_BEST_COMPRESSION (9; 0x78DA), 
        #Z_NO_COMPRESSION (0),
        #Z_DEFAULT_COMPRESSION (-1; 0x789C) 
        #for more information about these values.

        comp = zlib.compress(data, level=zlib.Z_DEFAULT_COMPRESSION) #zlib.Z_BEST_COMPRESSION

        with open(out_path, "wb") as out_f:
            out_f.write(comp)

            if target_size:
                # padding_len = target_size-len(comp)
                # print("padding size: "+str(padding_len))
                # out_f.write(b"\x00" * (padding_len))
                padding_len = target_size-len(comp)
                if (padding_len>0):
                    print("padding size: "+str(padding_len))
                    out_f.write(b"\x00" * (padding_len))
                elif (padding_len<0):
                    print("WARNING: zlib output exceeds target size! "+str(padding_len))
                #     print("removing size: "+str(padding_len))
                #     out_f.seek(padding_len, os.SEEK_END)
                #     out_f.truncate()
                # out_f.close()
            else:
                print("compressed size: "+str(len(comp)))

if __name__ == "__main__":
    # compress(sys.argv[1], sys.argv[2])

    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='Compresses file with zlib and adds optional padding',
                    epilog='Have a nice day!')

    parser.add_argument('filename') #file to be compressed
    parser.add_argument('outfile') #output file
    parser.add_argument('-t', '--targetsize') #target size to pad to

    args = parser.parse_args()

    if args.targetsize:
        compress(args.filename, args.outfile, int(args.targetsize))

    else:
        compress(args.filename, args.outfile)



