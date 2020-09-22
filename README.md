# process_CHILDES
This repo contains scripts to process CHILDES data, with POS and syntactic dependency relations


## Notes on in-house data generation

1. Gloss inconsistency: many many cases of “wanna” changed into “want to”; I was wondering if to some extent childes-db was looking at stem (or minor bug in their code)

1. Childes-db ‘ s way of handling repetition
   1. my [/] my paper (they treated it as 3 tokens with the gloss being “my my paper”
   1. Childes-db ‘s way of handling “explanations

1. There’s no specific documentation of how cases such as “<that> dat book” should be treated
   1. Therefore this potentially leads to different estimation of number of tokens
   1. In general, glosses associated with these codes: [/?], [/-], [/], [//], and [///] are not clearly defined

1. POS does not match
   1. Based on CHILDES annotation, “what dat” has a pos sequence of “pro:int, adv”
   1. Based on childes-db, it’s “pro:int, det”; which is potentially more accurate, but still in consistent (and I’m hesitant to make my own subject decisions)

1. Whether unintelligible tokens should be counted as separate number of tokens
   1. Although this was handled in our data generation process where I added a separate column of number of unintelligible tokens

1. POS information in childes-db is not complete; this was handled in our data generation process as well

1. Annotation errors (some examples)
   1. gloss: what else is on there ?
      stem: what else be&3S on there
      pos: pro:int post aux prep 
      dependenc relations: 1|0|INCROOT **2|1|PUNCT** 3|2|INCROOT 4|3|JCT 5|4|POBJ 6|3|PUNCT
