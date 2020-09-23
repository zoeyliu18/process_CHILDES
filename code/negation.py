import pandas as pd
import networkx as nx
import io, argparse


def load_file(filename):
	df = pd.read_csv(filename)
	return df


### Function to combine gloss, POS, and dependency relations together #####

def combine(stem, pos, dependency):

	info = []

	new_stem = []
	new_pos = []
	new_dependency = []

	lemma = []

	for w  in stem.split():
		if '~' in w:
			for t in w.split('~'):
				new_stem.append(t)
			
			#### As of now, lemma is the same as stem; except for n't ###

				if t != 'not':
					lemma.append(t)
				else:
					lemma.append("n't")
		else:
			new_stem.append(w)
			lemma.append(w)


	for p in pos.split():
		if '~' in p:
			for t in p.split('~'):
				new_pos.append(t)
		else:
			new_pos.append(p)

	dependency = dependency.split()
	for d in dependency[ : -1]:
		new_dependency.append(d)

	last_d = dependency[-1].split('|')

	if last_d[-1] != 'PUNCT' and int(last_d[0]) == len(new_stem):
		new_dependency.append(last_d)
	if last_d[-1] != 'PUNCT' and int(last_d[0]) != len(new_stem):
		new_dependency[-1] = new_dependency[-1] + ' ' + last_d[-1]
	

	c = 0

	if len(new_stem) != len(new_pos) or len(new_stem) != len(new_dependency) or len(new_pos) != len(new_dependency):
		c += 1
		print(stem, pos, dependency)
	#	print(new_stem, new_pos, new_dependency)

	if c == 0:
		return [new_stem, new_pos, new_dependency, lemma]


def toCoNLL(sent_info):

########### CoNLL-U format ###########

# ID: Word index, integer starting at 1 for each new sentence; may be a range for tokens with multiple words.
# FORM: Word form or punctuation symbol.
# LEMMA: Lemma or stem of word form.
# UPOSTAG: Universal part-of-speech tag drawn from our revised version of the Google universal POS tags.
# XPOSTAG: Language-specific part-of-speech tag; underscore if not available.
# FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
# HEAD: Head of the current token, which is either a value of ID or zero (0).
# DEPREL: Universal Stanford dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
# DEPS: List of secondary dependencies (head-deprel pairs).
# MISC: Any other annotation.

######################################
	
	id_list = []
	form_list = []
	lemma_list = []
	upostag = []
	xpostag = []
	feats = []
	head = []
	deprel = []
	deps = []
	misc = []

	conll_toks = []

	stem = sent_info[0]
	pos = sent_info[1]
	dependency = sent_info[2]
	lemma = sent_info[3]

	start = 1

	for i in range(len(stem)):
		id_list.append(start)

	#### As of now, treating form and lemma as the same to deal with lots of punctuation idiosyncrasy in CHILDES #####

		form_list.append(stem[i])
		lemma_list.append(lemma[i])
		upostag.append(pos[i])
		xpostag.append('_')

	#### Eventually would combine with things like ~3sg ####
		
		feats.append('_')

		head.append(dependency[i].split('|')[1])

		deprel.append(dependency[i].split('|')[-1])

		deps.append('_')

		misc.append('_')

		start += 1

#	print(stem)
#	print(dependency)
#	print(feats)
#	print(len(id_list))
#	print(len(form_list))
#	print(len(lemma_list))
#	print(len(upostag))
#	print(len(xpostag))
#	print(len(feats))
#	print(len(head))
#	print(len(deprel))
#	print(len(deps))
#	print(len(misc))

	for i in range(len(id_list)):
		conll_toks.append([id_list[i], form_list[i], lemma_list[i], upostag[i], xpostag[i], feats[i], head[i], deprel[i], deps[i], misc[i]])

	return conll_toks


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--corpus', type = str, help = 'corpus_name')
	parser.add_argument('--output', type = str, help = 'output CoNLL formatted file')

	args = parser.parse_args()

	data = load_file(args.corpus)

	outfile = io.open(args.output, 'w', encoding = 'utf-8')

	utterance_order = data['utterance_order']
	collection_name = data['collection_name']
	language = data['language']
	corpus_name = data['corpus_name']
	
	speaker_code = data['speaker_code']
	speaker_role = data['speaker_role']

	target_child_sex = data['target_child_sex']
	target_child_age = data['target_child_age']
	target_child_type = data['target_child_type']

	gloss_list = data['gloss']
	num_tokens_list = data['num_tokens']
	stem_list = data['stem']
	pos_list = data['part_of_speech']
	dependencies_list = data['dependency']

	### English-NA; eng
	### Brown
	### Adam; Target_Child; sex; age; type
	### utterance_order: gloss

	for i in range(len(data)):

		gloss = str(gloss_list[i])
		stem = str(stem_list[i])
		pos = str(pos_list[i])
		dependency = str(dependencies_list[i])

		if stem != 'nan':
			info = combine(stem, pos, dependency)
			conll = toCoNLL(info)

			outfile.write('### ' + collection_name[i] + ' ' + language[i] + '\n')
			outfile.write('### ' + corpus_name[i] + '\n')
			outfile.write('### ' + speaker_code[i] + ' ' + speaker_role[i] + ' ' + target_child_sex[i] + ' ' + str(target_child_age[i]) + ' ' + target_child_type[i] + '\n')
			outfile.write('### ' + str(utterance_order[i]) + ' ' + gloss + '\n')

			for tok in conll:
				outfile.write('\t'.join(str(w) for w in tok) + '\n')

			outfile.write('\n')

