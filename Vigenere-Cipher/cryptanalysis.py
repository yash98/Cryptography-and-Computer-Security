import argparse
import os
from os import close
import re

from kasiski_method import kasiski
from ic import index_of_coincidence, ic_english

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

	for filename in files:
		file = open(filename, 'r')
		print(filename)
		encrypted_text = file.read()
		key_length_candidates = set()
		ngram_size_list = [3, 4, 5, 6, 7, 8, 9, 10]
		for ngram_size in ngram_size_list:
			key_length_candidates.add(kasiski(encrypted_text, ngram_size))
		print(key_length_candidates)

		best_key_length = None
		best_key_len_diff = ic_english
		for key_length in key_length_candidates:
			ic_key_length = index_of_coincidence(encrypted_text, key_length)
			ic_key_length_diff =  abs(ic_english - ic_key_length)
			print(key_length, ic_key_length, ic_key_length_diff)
			if best_key_len_diff > ic_key_length_diff:
				best_key_len_diff = ic_key_length_diff
				best_key_length = key_length
		print(best_key_length)

		file.close()


if __name__ == "__main__":
	main()
