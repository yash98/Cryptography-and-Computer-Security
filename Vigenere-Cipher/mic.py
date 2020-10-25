#!/usr/bin/env python
mic_english = 0.065
freq_english = [0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,0.06749,0.07507,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.02360,0.00150,0.01974,0.00074]

def letter_to_shift(c: str) -> int:
	return ord(c) - ord('A')

def shift_to_letter(i: int) -> str:
	return chr(ord('A')+i)

def mutual_index_of_coincidence(encrypted_text: str, key_length: int) -> str:
	sequence_bins = {}
	for i in range(key_length):
		sequence_bins[i] = {}
	sequence_length = [0.0 for i in range(key_length)]

	text_iter = iter(encrypted_text)
	try:
		while True:
			for i in range(key_length):
				character = next(text_iter)
				if character in sequence_bins[i]:
					sequence_bins[i][character] += 1
				else:
					sequence_bins[i][character] = 1
				sequence_length[i] += 1
	except StopIteration:
		pass
	
	key = ""
	for seq_id in sequence_bins:
		mic_divisor = float(sequence_length[seq_id])
		best_mic_diff = mic_english
		best_g = None
		for g in range(26):
			mic_g_sum = 0.0
			for i in range(26):
				freq_i = freq_english[i]
				freq_i_g = 0
				c_i_g = shift_to_letter((i+g)%26)
				if c_i_g in sequence_bins[seq_id]:
					freq_i_g = sequence_bins[seq_id][c_i_g]
				mic_g_sum += freq_i*freq_i_g

			mic_g = mic_g_sum/mic_divisor
			mic_diff = abs(mic_english-mic_g)
			if best_mic_diff > mic_diff:
				best_mic_diff = mic_diff
				best_g = g
		
		key += shift_to_letter(best_g)
	
	return key


