import os, sys

#.STR files per level/area
#English: delimited with CRLF
#Japanese: delimited with NUL

#assumes all files are in uppercase
def convert_e2j(indir_en, indir_js, outdir):

    files = sorted(os.listdir(indir_en))
    pfcount = 0

    for name in files:

        print("procesing "+name)

        text_en_og = open(f"{indir_en}/{name}", "rb").read()

        try:
            text_js_og = open(f"{indir_js}/{name}", "rb").read()
            target_size = len(text_js_og)
            print("target_size: "+str(target_size))
        except:
            print("skipping; no js for "+name)
            continue

        # os.makedirs(indir + "/js", exist_ok=True)

        #replace each CRLF with NUL
        text_en_ps2 = text_en_og.replace(b"\x0D\x0A", b"\x00")

        with open(outdir+"/"+name, "wb") as f:
            f.write(text_en_ps2)
            padding_len = target_size-len(text_en_ps2)
            if (padding_len>0):
                print("padding size: "+str(padding_len))
                f.write(b"\x00" * (padding_len))
            elif (padding_len<0):
                print("removing size: "+str(padding_len))
                f.seek(padding_len, os.SEEK_END)
                f.truncate()
            f.close()
            pfcount+=1

    print("processed files: "+str(pfcount))


if __name__ == "__main__":
    convert_e2j(sys.argv[1], sys.argv[2], sys.argv[3])
