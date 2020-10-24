import argparse
import os
import re

def main():
	parser = argparse.ArgumentParser()
	file_selection_group = parser.add_mutually_exclusive_group()
	file_selection_group.add_argument("-d", type=str, help="directory with all the encrypted files only", metavar="dir")
	file_selection_group.add_argument("-f", type=str, nargs='+', help="list of files", metavar=("file1", "file2"))
	parser.add_argument("-o", help="output directory", metavar="out_dir", default="./crypt_analysis")
	args = parser.parse_args()

	test_file_pattern = re.compile(r'.*test[0-9]*\b')
	
	files = None
	if args.f is None:
		if args.d is None:
			files_temp = [os.path.join("./tests", file) for file in os.listdir("./tests")]
		else:
			files_temp = [os.path.join(args.d, file) for file in os.listdir(args.d)]
		files = [filename for filename in files_temp if test_file_pattern.match(filename)]
	else:
		files = args.f

	print(files)


if __name__ == "__main__":
	main()
