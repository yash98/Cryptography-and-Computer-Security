from numpy import array

ic_english = 0.0686
ic_random = 0.038466

def index_of_coincidence(encrypted_text: str, key_length: int) -> float:
	if len(encrypted_text)/2 < key_length:
		return 0.0
	
	sequence_bins = {}
	for i in range(key_length):
		sequence_bins[i] = {}
	sequence_length = array([0.0 for i in range(key_length)])

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

	ic_sum = 0.0
	for seq_id in sequence_bins:
		ic_divisor = sequence_length[seq_id]*(sequence_length[seq_id]-1)
		seq_ic_sum = 0.0
		for character in sequence_bins[seq_id]:
			char_count = sequence_bins[seq_id][character]
			seq_ic_sum += char_count * (char_count-1)
		seq_ic_sum /= ic_divisor
		ic_sum += seq_ic_sum
	ic_avg = ic_sum / key_length

	return ic_avg

