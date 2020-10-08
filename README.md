# process_CHILDES
This repo contains scripts to process CHILDES data, with POS and syntactic dependency relations


## Notes on in-house data generation

1. **Gloss inconsistency: many many cases of “wanna” changed into “want to”; I was wondering if to some extent childes-db was looking at stem (or minor bug in their code)**

1. **Childes-db ‘ s way of handling repetition**
   1. ```my [/] my paper``` (they treated it as 3 tokens with the gloss being “my my paper”

1. **There’s no specific documentation of how cases such as ```<that> dat book``` should be treated**
   1. Therefore this potentially leads to different estimation of number of tokens
   1. In general, glosses associated with these codes: ```[/?], [/-], [/], [//], and [///]``` are not clearly defined

1. **POS does not match***
   1. Based on CHILDES annotation, ```what dat``` has a pos sequence of ```pro:int, adv```
   1. Based on childes-db, it’s ```pro:int, det```; which is potentially more accurate, but still in consistent (and I’m hesitant to make my own subject decisions)

1. **Whether unintelligible tokens should be counted as separate number of tokens**
   1. Although this was handled in our data generation process where I added a separate column of number of unintelligible tokens

1. **POS information in childes-db is not complete; this was handled in our data generation process as well**

1. **Overall, the scripts here count number of tokens based on stem**

1. **Annotation errors (some examples)**
   1. gloss: ```what``` **else** ```is on there ?``` <br/>
      stem: ```what``` **else** ```be&3S on there``` <br/>
      pos: ```pro:int``` **post** ```aux prep n``` <br/>
      dependenc relations: ```1|0|INCROOT``` **2|1|PUNCT** ```3|2|INCROOT 4|3|JCT 5|4|POBJ 6|3|PUNCT```
   1. gloss: ```does your writing look like his ?``` <br/>
      stem: ```do&3S your write-PRESP look like his``` <br/>
      pos: ```mod det:poss n:gerund v conj det:poss``` <br/>
      dependency relations: ```1|4|AUX 2|3|DET 3|4|SUBJ 4|0|ROOT 5|4|JCT 6|7|DET``` **7|5|POBJ**
   1. gloss: ```⌊come on , let's go→⌋```
      stem: ```come on cm let~us go```
      pos: ```v adv cm v~pro:obj v```
      dependency relations: ```1|0|ROOT 2|1|JCT 3|1|LP 4|1|ENUM 5|4|OBJ 6|1|PUNCT``` (Sprott/01Goldilocks.cha)
   1. more dependency relations than the number of tokens

1. **Manually added target_child_sex in 020010.cha and 020324.cha in Bloom/Peter**

1. **Lacking morphosyntactic and dependency annotation in 2014-Indiff folder in Gelman corpus**

1. **⌈nay , nay , nay , nay , nay⌉ (Sprott/01Goldilocks.cha)---- What do?**

1. **dependency relation between auxiliaries and head verb

## Notes on CoNLL-U format file generation 

1. **Each sentences starts with two lines of additional information**
   1. file name + speaker name ```### 020304.cha Adam``` (for comparison to original .cha file)
   1. utterance order + gloss ```### 1 play checkers .```
   
1. **format follows the 10 column tab-delimited format of Universal Dependencies**
   1. ID: Word index
   1. FORM: Word form or punctuation symbol. **currently, it is lemma based on tokenization from CHILDES**
   1. lemma: **currently it's the same as FORM; except for cases with n't (not as form, n't as lemma for ease of identification(**
   1. POS
   1. Left empty
   1. FEATS: empty
   1. HEAD: index of syntactic head
   1. DEPREL: dependency relation with the syntactic head
   1. Speaker name + Speaker code + Speaker role (e.g. Adam CHI Target_Child); separated by space
   1. Child gender + age + type (e.g. male 27 TD); separated by space

1. **gloss not matched yet (see notes above); but does not necessarily affect current work on negation per se**




## Eventually train a parser and annotate the rest of the data (?) ##
