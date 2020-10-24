from functools import reduce
import numpy as np

def gcd_2_helper(a: int, b: int) -> int:
	if a == 0:
		return b
	return gcd_2_helper(b % a, a)

def gcd_n(numbers: list) -> int:
	if len(numbers) == 0:
		return 1
	numbers = list(numbers)
	numbers.sort()
	return reduce(gcd_2_helper, numbers)

def kasiski(encrypted_text: str, str_size: int) -> int:
	str_bin = {}
	for i in range(len(encrypted_text)-str_size):
		str_ngram = encrypted_text[i:i+str_size]
		if str_ngram in str_bin:
			str_bin[str_ngram] = np.append(str_bin[str_ngram], i)
		else:
			str_bin[str_ngram] = np.array([i])

	distance_set = set()
	for ngram_distances in str_bin:
		for i in range(len(str_bin[ngram_distances])):
			for j in range(i+1, len(str_bin[ngram_distances])):
				distance_set.add(str_bin[ngram_distances][j] - str_bin[ngram_distances][i])
	
	return gcd_n(distance_set)
