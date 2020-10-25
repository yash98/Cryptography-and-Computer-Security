import argparse
import os
from os import close
import re

from kasiski_method import kasiski
from ic import index_of_coincidence, ic_english
from mic import mutual_index_of_coincidence, letter_to_shift, shift_to_letter

def decrypt(encrypted_text: str, key: str) -> str:
	decrypted_text = ""

	text_iter = iter(encrypted_text)
	try:
		while True:
			for letter_shift in key:
				charecter = next(text_iter)
				decrypted_text += shift_to_letter((letter_to_shift(charecter)-letter_to_shift(letter_shift))%26)
	except StopIteration:
		pass

	return decrypted_text
		

def main():
	parser = argparse.ArgumentParser()
	file_selection_group = parser.add_mutually_exclusive_group()
	file_selection_group.add_argument("-d", type=str, help="directory with all the encrypted files only", metavar="dir")
	file_selection_group.add_argument("-f", type=str, nargs='+', help="list of files", metavar=("file1", "file2"))
	parser.add_argument("-o", help="output directory", metavar="out_dir", default="./crypt_analysis")
	args = parser.parse_args()

	test_file_pattern = re.compile(r'.*(?P<name_end>test[0-9]*)\b')
	
	files = None
	if args.f is None:
		if args.d is None:
			files_temp = [os.path.join("./tests", file) for file in os.listdir("./tests")]
		else:
			files_temp = [os.path.join(args.d, file) for file in os.listdir(args.d)]
		files = [filename for filename in files_temp if test_file_pattern.match(filename)]
	else:
		files = args.f
	
	filename_ends = [test_file_pattern.findall(filename)[-1] for filename in files]
	try:
		os.mkdir(args.o)
	except FileExistsError:
		pass

	for i in range(len(files)):
		print("Starting cryptanalysis for file", files[i])
		encrypted_file = open(files[i], 'r')
		output_file_kasiski = open(os.path.join(args.o, filename_ends[i]+"_kasiski"), 'w+')
		output_file_ic = open(os.path.join(args.o, filename_ends[i]+"_ic"), 'w+')
		output_file_key_mic = open(os.path.join(args.o, filename_ends[i]+"_key_mic"), 'w+')
		encrypted_text = encrypted_file.read()

		key_length_candidates = set()
		ngram_size_list = [3, 4, 5, 6, 7, 8, 9, 10]

		for ngram_size in ngram_size_list:
			key_length_candidates.add(kasiski(encrypted_text, ngram_size))
		output_file_kasiski.write("Kasiski method suggests the key lengths: "+str(key_length_candidates)+'\n')
		output_file_kasiski.write("The following keyword (or n-gram) lengths were checked: "+str(ngram_size_list)+'\n')
		print("Kisaski Done")

		output_file_ic.write("key length, ic for the key length, difference from ic english"+'\n')
		best_key_length = None
		best_key_len_diff = ic_english
		for key_length in key_length_candidates:
			ic_key_length = index_of_coincidence(encrypted_text, key_length)
			ic_key_length_diff =  abs(ic_english - ic_key_length)
			output_file_ic.write(str(key_length) + " " + str(ic_key_length) + " " + str(ic_key_length_diff)+'\n')
			if best_key_len_diff > ic_key_length_diff:
				best_key_len_diff = ic_key_length_diff
				best_key_length = key_length
		output_file_ic.write("Best key length evaluated is " + str(best_key_length)+'\n')
		print("IC done")

		key = mutual_index_of_coincidence(encrypted_text, best_key_length)
		output_file_key_mic.write("Key evaluated from cryptanalysis is \"" + str(key) + "\"\n")
		output_file_key_mic.write("Text obtained from decrypting using the key is \"" + str(decrypt(encrypted_text, key)) + "\"\n")
		print("MIC done")

		encrypted_file.close()
		output_file_kasiski.close()
		output_file_ic.close()
		output_file_key_mic.close()

	print("Output generated in directory", args.o)

if __name__ == "__main__":
	main()
