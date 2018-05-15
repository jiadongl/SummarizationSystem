# Alphabetical list of part-of-speech tags used in the Penn Treebank Project:
# N     Tag Description
# 1.	CC	Coordinating conjunction
# 2.	CD	Cardinal number
# 3.	DT	Determiner
# 4.	EX	Existential there
# 5.	FW	Foreign word
# 6.	IN	Preposition or subordinating conjunction
# 7.	JJ	Adjective
# 8.	JJR	Adjective, comparative
# 9.	JJS	Adjective, superlative
# 10.	LS	List item marker
# 11.	MD	Modal
# 12.	NN	Noun, singular or mass
# 13.	NNS	Noun, plural
# 14.	NNP	Proper noun, singular
# 15.	NNPS	Proper noun, plural
# 16.	PDT	Predeterminer
# 17.	POS	Possessive ending
# 18.	PRP	Personal pronoun
# 19.	PRP$	Possessive pronoun
# 20.	RB	Adverb
# 21.	RBR	Adverb, comparative
# 22.	RBS	Adverb, superlative
# 23.	RP	Particle
# 24.	SYM	Symbol
# 25.	TO	to
# 26.	UH	Interjection
# 27.	VB	Verb, base form
# 28.	VBD	Verb, past tense
# 29.	VBG	Verb, gerund or present participle
# 30.	VBN	Verb, past participle
# 31.	VBP	Verb, non-3rd person singular present
# 32.	VBZ	Verb, 3rd person singular present
# 33.	WDT	Wh-determiner
# 34.	WP	Wh-pronoun
# 35.	WP$	Possessive wh-pronoun
# 36.	WRB	Wh-adverb

# PRP and PRP$ is lightly considered in D3, but could be re map to its NN/NNP, then it will be taken account.

POS_tag_weight = {"CD": 1, "JJ": 1, "JJR": 1, "JJS": 1,
                  "NN": 5, "NNS": 5, "NNP": 5, "NNPS": 5, "PRP": 1, "PRP$": 1,
                  "VB": 5, "VBD": 5, "VBG": 5, "VBN": 5, "VBP": 5, "VBZ": 5}

Ignore_words = ['said', 'be', 'is', 'was', 'are', 'were', 'have', 'has', 'had']
