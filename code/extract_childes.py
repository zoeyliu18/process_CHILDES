###### This script converts CHILDES English-NA and English-UK to CoNLL format ######

import io, os, glob, argparse, csv, string

punct = list(string.punctuation)


#### Format from Childes-db #####

## Classes 'tbl_df', 'tbl' and 'data.frame':    73431 obs. of  25 variables:
##  $ id               : int  964592 964598 964606 964617 964627 964633 964643 964649 964652 964657 ...
##  $ speaker_id       : int  2949 2949 2953 2949 2949 2949 2949 2953 2949 2953 ...
##  $ utterance_order  : int  1 2 3 4 5 6 7 8 9 10 ...
##  $ transcript_id    : int  3272 3272 3272 3272 3272 3272 3272 3272 3272 3272 ...
##  $ corpus_id        : int  36 36 36 36 36 36 36 36 36 36 ...
##  $ gloss            : chr  "play checkers" "big drum" "big drum" "big drum" ...
##  $ num_tokens       : int  2 2 2 2 2 2 1 1 2 3 ...
##  $ stem             : chr  "play checker" "big drum" "big drum" "big drum" ...
##  $ part_of_speech   : chr  "n n" "adj n" "adj n" "adj n" ...
##  $ speaker_code     : chr  "CHI" "CHI" "MOT" "CHI" ...
##  $ speaker_name     : chr  "Adam" "Adam" NA "Adam" ...
##  $ speaker_role     : chr  "Target_Child" "Target_Child" "Mother" "Target_Child" ...
##  $ target_child_id  : int  2949 2949 2949 2949 2949 2949 2949 2949 2949 2949 ...
##  $ target_child_age : num  27.1 27.1 27.1 27.1 27.1 ...
##  $ target_child_name: chr  "Adam" "Adam" "Adam" "Adam" ...
##  $ target_child_sex : chr  "male" "male" "male" "male" ...
##  $ type             : chr  "declarative" "declarative" "question" "declarative" ...
##  $ media_end        : num  NA NA NA NA NA NA NA NA NA NA ...
##  $ media_start      : num  NA NA NA NA NA NA NA NA NA NA ...
##  $ media_unit       : chr  NA NA NA NA ...
##  $ collection_id    : int  3 3 3 3 3 3 3 3 3 3 ...
##  $ collection_name  : chr  "Eng-NA" "Eng-NA" "Eng-NA" "Eng-NA" ...
##  $ num_morphemes    : int  3 2 2 2 2 2 1 1 2 4 ...
##  $ language         : chr  "eng" "eng" "eng" "eng" ...
##  $ corpus_name      : chr  "Brown" "Brown" "Brown" "Brown" ...


def Expelliarmus(file, corpus, collection_name):

	features = []

	with io.open(corpus + '/' + file, encoding = 'utf-8') as f:
		
		participants = {}

		target_child_name = 'nan'
		target_child_age = 'nan'
		target_child_sex = 'nan'
		target_child_type = 'nan'

		speaker_code_list = []
		speaker_name_list = []
		speaker_role_list = []
	
		gloss_list = []
		stem_list = []
		pos_list = []
		num_of_tokens_list = []
		unintelligible_list = []
		num_of_morphemes_list = []
		mor_list = []
		dependency_list = []
		
		gloss_idx = []

		data = []

		all_data = []

		for line in f:
			all_data.append(line.strip())
	
		##### Getting participants info #####	
		### {'CHI' : ['Adam', 'Target_Child']}

		id_list = []
		participants_idx = 'nan'

		for line in all_data:
			if line.startswith('@Participants'):
				participants_idx = int(all_data.index(line))

			if line.startswith('@ID'):
				id_list.append(int(all_data.index(line)))

		if participants_idx != 'nan':
			participants_info = []
			for info in all_data[participants_idx : sorted(id_list)[0]]:
				info = info
				participants_info.append(info)

			participants_info = ' '.join(info for info in participants_info)
			roles = participants_info.split('\t')[1].split(' , ')

			new_roles = []
			for tok in roles:
				if ',' not in tok:
					new_roles.append(tok)
				else:
					for w in tok.split(', '):
						new_roles.append(w)

			if len(new_roles) == 1:
				new_roles = new_roles[0].split(',')

			for tok in new_roles:
				tok = tok.split()

				if len(tok) == 3:
					participants[tok[0]] = [tok[1], tok[2]]
				else:
					try:
						participants[tok[0]] = ['nan', tok[1]]
					except IndexError:
						print(tok, participants, participants_info, file)


		#	if line.startswith('@Participants'): # and file == '010900a.cha':
			
		#		roles = line.strip().split('\t')[1].split(' , ')

		#		if len(roles) == 1:
		#			roles = roles[0].split(',')

		#		for tok in roles:
		#			tok = tok.split()

		#			if len(tok) == 3:
		#				participants[tok[0]] = [tok[1], tok[2]]
		#			else:
		#				participants[tok[0]] = ['nan', tok[1]]


		for line in all_data:

			if '@ID' in line and 'Target_Child' in line:
				toks = line.split('|')

				if toks[3][0].isdigit() is True:
					age = toks[3]
				
					if ';' in age:
						age = age.split(';')
						target_child_age = int(age[0]) * 12 + int(age[1][0]) * 10 + int(age[1][1])

					else:
						target_child_age = int(age) * 12

				
				if toks[4] in ['female', 'male']:
					target_child_sex = toks[4]


			if line.startswith('@Types'):

				if ' TD' in line:
					target_child_type = 'TD'
				else:
					target_child_type = 'SLD'

			if line.startswith('@') is False:
				data.append(line)
			

	### Based on CHILDES annotation, certain cases have multiple lines for gloss or annotations ###

		for i in range(len(data)):

			### Getting tokens of utterances from all roles ###

			if data[i].startswith('*'):
				gloss_idx.append(i)

	### Getting morphosyntactic information of utterances ###

		gloss_idx.append(len(data))

		for i in range(len(gloss_idx) - 1):
			utterance = ' '.join(u for u in data[gloss_idx[i]: gloss_idx[i + 1]])
			utterance = utterance.split('%')

			mor = 'nan'
			gra = 'nan'
		
			num_of_morphemes = 0
			num_of_tokens = 0
			num_of_unintelliglble = 0

			gloss = 'nan'

			stem = 'nan'
			pos = 'nan'

			for tok in utterance:
			
				if tok.startswith('*'):
					sentence = tok.split()
					speaker_code_list.append(sentence[0][1 : -1])
					gloss = sentence[1 : ]
					gloss_list.append(' '.join(w for w in gloss))

					for w in gloss:
						if w in ['xxx', 'yyy', 'www', 'zzz', 'xx']:
							num_of_unintelliglble += 1

				if tok.startswith('mor:'):
					stem = []
					pos = []
				
					mor = tok.split()[1 : ]

					for m in mor:
						num_of_morphemes += m.count('|')
						num_of_morphemes += m.count('-')

						if '~' not in m and '|' in m:
							m = m.split('|')
							try:
								stem.append(m[1])
								pos.append(m[0])
							except:
								print(mor)


						if '~' in m:
							m_stem = []
							m_pos = []
						
							m = m.split('~')

							for t in m:
								t = t.split('|')
								m_stem.append(t[1])
								m_pos.append(t[0])

							m_stem = '~'.join(w for w in m_stem)
							m_pos = '~'.join(w for w in m_pos)

							stem.append(m_stem)
							pos.append(m_pos)


				if tok.startswith('gra:'):
					gra = tok.split()[1 : ]

				#	for d in gra:
				#		if d.split('|')[-1] != 'PUNCT':
				#			num_of_tokens += 1

	
	#### Counting number of tokens ######

	#		c = 0
	#		for w in gloss:
	#			if w.startswith('&'):
	#				c += 1

	#		if pos != 'nan':
	#			num_of_tokens = len(pos) + num_of_unintelliglble + gloss.count('[//]') + gloss.count('[/]') + c
		
		### cases like 0. ####

	#		if pos == 'nan' and gloss[0] == '0':
	#			num_of_tokens = 0

		#### cases like xxx . ######

	#		if pos == 'nan' and gloss[0] != '0':
	#			num_of_tokens = 1

			if stem != 'nan':
				num_of_tokens = len(stem)
			else:
				num_of_tokens = 0

			unintelligible_list.append(num_of_unintelliglble)

			if 'CHI' in participants:
				target_child_name = participants['CHI'][0]

			if mor != 'nan':
				mor_list.append(mor)
			else:
				mor_list.append('nan')

			if stem != 'nan':
				stem_list.append(' '.join(w for w in stem))
			else:
				stem_list.append('nan')

			if pos != 'nan':
				pos_list.append(' '.join(w for w in pos))
			else:
				pos_list.append('nan')

			if gra != 'nan':
				dependency_list.append(' '.join(d for d in gra))
			else:
				dependency_list.append('nan')

			num_of_morphemes_list.append(num_of_morphemes)
			num_of_tokens_list.append(num_of_tokens)



		order = 1

		for i in range(len(gloss_list)):
			try:
				features.append([collection_name, 'eng', corpus, speaker_code_list[i], participants[speaker_code_list[i]][0], participants[speaker_code_list[i]][1], target_child_age, target_child_name, target_child_sex, target_child_type, file, order, gloss_list[i], num_of_tokens_list[i], unintelligible_list[i], stem_list[i], pos_list[i], num_of_morphemes_list[i], dependency_list[i]])
			except KeyError:
	#			print(participants)
	#			print(speaker_code_list[i])
	#			continue
				print(file)
	#			print(participants)


			order += 1

	return features


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--collection', type = str, help = 'collection_name')
	parser.add_argument('--input', type = str, help = 'path to CHILDES data')
	parser.add_argument('--output', type = str, help = 'output to instances file')

	args = parser.parse_args()

	path = args.input
	os.chdir(path)

	header = ['collection_name', 'language', 'corpus_name', 'speaker_code', 'speaker_name', 'speaker_role', 'target_child_age', 'target_child_name', 'target_child_sex', 'target_child_type', 'file_name', 'utterance_order', 'gloss', 'num_tokens', 'num_unintelligible', 'stem', 'part_of_speech', 'num_morphemes', 'dependency']

	all_data = []

#	for corpus in glob.glob('*'): # English-NA; English-UK
	files = []
	
	for file in os.listdir(path):			
		if file.endswith('.cha'):
			files.append(file)

	for file in sorted(files):
		for tok in Expelliarmus(file, path, args.collection):
			all_data.append(tok)

	child = path.split('/')[-3]

	with io.open(args.output, 'w', newline = '', encoding = 'utf-8') as f:
		writer = csv.writer(f)
	
		writer.writerow(header)

		for tok in all_data:
			tok[2] = child
			writer.writerow(tok)

