import re

from fuzzywuzzy import fuzz
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

def similar(s1, s2, threshold):
	s1 = re.sub(r'[^\w\s]', '', s1)
	s2 = re.sub(r'[^\w\s]', '', s2)
	s1 = str(s1).lower().split()
	s2 = str(s2).lower().split()
	s1_words = [w for w in s1 if w not in stop_words]
	s2_words = [w for w in s2 if w not in stop_words]
	s1 = ' '.join(s1_words)
	s2 = ' '.join(s2_words)
	similarity_score = fuzz.ratio(s1, s2)
	print('======================')
	print(s1, s2)
	print(similarity_score)
	print('======================')
	if similarity_score > threshold:
		return True
	return False