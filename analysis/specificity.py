# -*- coding: utf-8 -*-


from pattern.en import mood, wordlist, wordnet, Sentence, parse, VERB, NOUN, ADJECTIVE, ADVERB, tag
from pattern.vector import stem, PORTER, LEMMA, count, words, Document

def wordnet_depth_simple(word):

  string = word.string
  synsets = wordnet.synsets(string)

  if len(synsets) < 1:
    #print 'No SYNSETS: ' , string
    return -1

  synset = synsets[0]
  hypernyms = synset.hypernyms(True)
  depth = len(hypernyms)
  #print 'Considered: ' , string, ', depth: ' , depth
  #print 'Hypernyms: ' , hypernyms
  return depth


def wordnet_depth(word):

  string = word.string
  stemmed = stem(string, stemmer=PORTER)

  pos = word.type[:2]
  pos_object = None

  #print 'String: ' , string , ' Stemmed:', stemmed, ' POS: ', pos

  if pos == 'NN':
    pos_object = NOUN
  elif pos == 'VB':
    pos_object = VERB
  elif pos == 'JJ':
    pos_object = ADJECTIVE
  elif pos == 'RB':
    pos_object = ADVERB

  if pos_object == None:
    return -1


  synsets = wordnet.synsets(string, pos_object)

  if len(synsets) < 1:
    #print 'No SYNSETS: ' , string
    return -1

  synset = synsets[0]
  #synset = wordnet.synsets(word)[0]
  hypernyms = synset.hypernyms(True)
  depth = len(hypernyms)
  #print 'Considered: ' , string, ', depth: ' , depth
  #print 'Hypernyms: ' , hypernyms
  return depth

def average_specificity2(s):
  sentence = Sentence(parse(s))
  sum = 0
  count = 0
  for word in sentence.words:
    if word.string in wordlist.STOPWORDS:
      continue
    depth = wordnet_depth(word)
    if depth == -1: #or depth == 0:
      continue
    #print word.string + ":" + str(depth)
    sum += depth
    count += 1.0

  if count == 0:
    return -1
  #print '==========Average specificity: ' , sum/count
  return sum/count

feedbacks = [
  'Overall, the layout and design is appealing and eye-catching. I would consider making the plate round instead of an oval as it looks a little odd and I found that distracting. I like the usage of the knife as a replacement for the letter “i”. You could also probably lose the two white things on either side of the phone and simply have the darker blue as a background element.',
  'The text at the top of the page doesn’t really grab my attention. I think this text is very important to be seen because it’s the major problem the app solves. ',
  'The use of tables and alignment here keeps things well organized. It’s nicely designed, and I can’t think of much that would improve it.',
  'This area is well organized, and easy to understand',
  'I think you should speak more to what this app actually does for people. The description is a little vague and I’m not really clear on what this does for me or why I should download it.'
]

feedbacks2 = [
  'I like the design at the bottom because it feels balanced and symmetrical. I would work on the font choice a bit though because it can be a little hard to read.',
  'if you were looking for something to seperate the section of text from the graphic i would use an entire place setting above each side facing eachother to show that there are at least 2 people eating. other than that it looks informative.',
  'I feel like there is too much negative space at the top, and especially in the area between the phone and the facts. I would take out the plate. I like the alignment of the inspiration and results lists.',
  'Too much blue, and words.  The design flow is off as well.  Not sure what the white bars on the sides of the phone are either.  I think more boldness and illustration vs. text would be appealing and easier to look at.',
  'I like the use of alignment in the design and I think it looks very organized and modern. The only thing that I would change about the poster is the long white rectangles on each side of the cell phone. I would make them thin lines and in the same color as the silverware, dark blue, or black.'
]

test = [
  'This would be good information to include if it had a more unique role such as “Haunted Hearse Tours Today@3PM, best to wear a light sweater because it will be sunny but with a light breeze” But because it doesn’t serve much of a role directly to the weather display, it is more information to digest and therefore distracting from what you’re trying to present to the viewer.',
  'Try using text to indicate what type of information we are looking at.'
]

def read_csv():
  import csv 

  with open('feedbacks.csv', 'rU') as f:
    with open('feedbacks_out.csv', 'wb') as out:

      reader = csv.reader(f)
      writer = csv.writer(out)

      for row in reader:
        print row[0].strip() , '\n\n'

        text = row[0].strip()
        val = average_specificity2(text)

        writer.writerow([text, val])
 
#read_csv()


#for t in test:
#  print t + "\nSpecificity: " + str(average_specificity2(t)) + "\n\n"

#s = 'I like the use of alignment in the design and I think it looks very organized and modern. The only thing that I would change about the poster is the long white rectangles on each side of the cell phone. I would make them thin lines and in the same color as the silverware, dark blue, or black.'

#sum = 0.0
#count = 0.0
#for s in feedbacks2:
#  sum += average_specificity2(s)
#  count += 1

#print "avg: " , sum/count

#hi_spef = 'This would be good information to include if it had a more unique role such as \“Haunted Hearse Tours Today @ 3PM, best to wear a light sweater because it will be sunny but with a light breeze\” But because it doesn\’t serve much of a role directly to the weather display, it is more information to digest and therefore distracting from what you’re trying to present to the viewer.'
#lo_spef = 'Try using text to indicate what type of information we are looking at.'
#med_spef = 'This element is too bright but not as bright as some of the other ones'

#average_specificity2(hi_spef)
#average_specificity2(lo_spef)
#average_specificity2(med_spef)

#indicative, imperative, subjunctive
#active: ratio of non-indicative sentences
#count actionable items
