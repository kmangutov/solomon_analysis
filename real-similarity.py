# -*- coding: utf-8 -*-


from pattern.vector import Document, Vector, distance, normalize

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

def similarity(a, b):

  docA = Document(a)
  docB = Document(b)

  vecA = normalize(docA.vector)
  vecB = normalize(docB.vector)

  #print docA.vector
  return 1 - distance(vecA, vecB)

for i in range(0, len(feedbacks)):
  print similarity(feedbacks[i], feedbacks2[i])



print similarity('a little bird', 'a little bird')
print similarity('a little bird', 'a little bird chirps')
print similarity('a little bird', 'a big dog barks')