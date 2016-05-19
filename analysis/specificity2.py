
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from pprint import pprint

# thanks http://stackoverflow.com/questions/27591621/nltk-convert-tokenized-sentence-to-synset-format

def penn_to_wn(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None

def tag(text):
	return pos_tag(word_tokenize(text))

def calcSpecificity(text):
	tagged = tag(text)

	synsets = []
	lemmatizer = WordNetLemmatizer()

	sum = 0
	count = 0

	for token in tagged:
		wn_tag = penn_to_wn(token[1])

		if not wn_tag:
			print "Could not be tagged "
			pprint(token[0])
			continue

		lemma = lemmatizer.lemmatize(token[0], pos=wn_tag)
		syns = wn.synsets(token[0], wn_tag)
		#else:
		#	lemma = lemmatizer.lemmatize(token[0])	
		#	syns = wn.synsets(token[0])	

		#pprint(lemma)
		#pprint(wn.synsets(token[0], wn_tag))
	

		if len(syns) <= 0:
			print "No synonyms: " + token[0]
			continue

		synset = syns[0]
		depth = (0.0 + synset.min_depth() + synset.max_depth())/2
		#depth = synset.max_depth()

		if depth < 0:
			print "No max depth: " + token[0]
			pprint(token[0])
			continue

		sum += depth
		count += 1

	if count == 0:
		return None

	return (sum + 0.0)/count

def countAvgHypernyms(text):
	tagged = tag(text)

	synsets = []
	lemmatizer = WordNetLemmatizer()

	sum = 0
	count = 0

	for token in tagged:
		wn_tag = penn_to_wn(token[1])

		if not wn_tag:
			print "Could not be tagged "
			pprint(token[0])
			continue

		lemma = lemmatizer.lemmatize(token[0], pos=wn_tag)
		syns = wn.synsets(token[0], wn_tag)
		#else:
		#	lemma = lemmatizer.lemmatize(token[0])	
		#	syns = wn.synsets(token[0])	

		#pprint(lemma)
		#pprint(wn.synsets(token[0], wn_tag))
	

		if len(syns) <= 0:
			print "No synonyms: " + token[0]
			continue

		synset = syns[0]
		#depth = synset.max_depth()

		hypernyms = synset.hypernyms()


		pprint(synset)
		pprint(hypernyms)



		if len(hypernyms) < 0:
			print "No hypernyms: " + token[0]
			pprint(token[0])
			continue

		sum += len(hypernyms)
		count += 1

	if count == 0:
		return None
		
	return (sum + 0.0)/count




text = "These boxes being stacked vertically looks unappealing. The grid view is not good What is this blank space for? The color doesn't match anything either Campus events and In the news section is nice but hyperlinks could use more information other than just headlines"
if __name__ == "__main__":
	print countAvgHypernyms(text)
