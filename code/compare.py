import pandas as pd
import io, argparse


def load_file(filename):
	df = pd.read_csv(filename)
	return df


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--house', type = str, help = 'in-house data')
	parser.add_argument('--db', type = str, help = 'db data')
	parser.add_argument('--output', type = str, help = 'output difference file')

	args = parser.parse_args()

	print('Loading utterances')

	neverland = load_file(args.house)
	db = load_file(args.db)

	print('Generating list of data')

	neverland_data = neverland.values.tolist()
	db_data = db.values.tolist()

	neverland_gloss = neverland['gloss']
	db_gloss = db['gloss']

	neverland_num_tokens = neverland['num_tokens']
	db_num_tokens = db['num_tokens']

	neverland_gloss = neverland['gloss']
	db_gloss = db['gloss']

	diff = io.open(args.output, 'w', encoding = 'utf-8')

	for i in range(len(neverland_num_tokens)):
#		if neverland_gloss[i] != db_gloss[i]:
#			diff.write('GLOSS' + '\n')
#			diff.write('\t'.join(str(tok) for tok in neverland_data[i]) + '\n')
#			diff.write('\t'.join(str(tok) for tok in db_data[i]) + '\n')
#			diff.write('\n')

		if neverland_num_tokens[i] != db_num_tokens[i]:
			if 'wanna' in neverland_gloss[i] and 'want to' in db_gloss[i] and db_num_tokens[i] - neverland_num_tokens[i] == 1:
				continue
			else:
				diff.write('NUM_TOKENS' + '\n')
				diff.write('\t'.join(str(tok) for tok in neverland_data[i]) + '\t' + str(neverland_num_tokens[i]) + '\n')
				diff.write('\t'.join(str(tok) for tok in db_data[i]) + '\t' + str(db_num_tokens[i]) + '\n')

		#	diff.write('\n')
