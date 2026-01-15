import os, sys
from t2_convert import t2_convert


if __name__ == "__main__":

	in_dir = sys.argv[1]
	# out_dir = sys.argv[2]

	files = sorted(os.listdir(in_dir))

	for name in files:

		print("procesing "+name)

		full_path = in_dir+"/"+name

		print(full_path)

		try:
			t2_convert(full_path)
		except Exception as e:
			print(e)




