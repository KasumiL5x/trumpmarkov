import pandas as pd
import markovify

class TrumpGenerator(object):
	def __init__(self):
		self.__load_tweets()
		self.__clean_tweets()
		self.__create_model()
	#end

	def __load_tweets(self):
		self.__tweets = pd.read_json('./tweets.json')
	#end

	def __clean_tweets(self):
		# Retain all non-retweet entries (value is 0/1 as a float).
		self.__tweets = self.__tweets[self.__tweets.is_retweet < 1.0]

		# Some values may be treated as floats, so cast all to string.
		self.__tweets['text'] = self.__tweets.text.astype('str')

		# Fix `&amp;`.
		self.__tweets['text'] = self.__tweets.text.str.replace(r'&amp;', '&')

		# Replace inverted quotes.
		self.__tweets['text'] = self.__tweets.text.str.replace('“', '"')
		self.__tweets['text'] = self.__tweets.text.str.replace('”', '"')

		# Replace strange hyphens.
		self.__tweets['text'] = self.__tweets.text.str.replace('–', '-')
		self.__tweets['text'] = self.__tweets.text.str.replace('—', '-')

		# Replace strange apostrophes.
		self.__tweets['text'] = self.__tweets.text.str.replace('’', "'")
		self.__tweets['text'] = self.__tweets.text.str.replace('‘', "'")
		self.__tweets['text'] = self.__tweets.text.str.replace('\x92', "'")

		# Replace latin space.
		self.__tweets['text'] = self.__tweets.text.str.replace('\xa0', ' ')
		# Zero width space.
		self.__tweets['text'] = self.__tweets.text.str.replace('\u200b', ' ')

		# l2r and r2l marks.
		self.__tweets['text'] = self.__tweets.text.str.replace('\u200e', '')
		self.__tweets['text'] = self.__tweets.text.str.replace('\u200f', '')

		# Fix bad unicode.
		self.__tweets['text'] = self.__tweets.text.str.replace('\U0010fc00', '')

		# Join all lines for the model.
		self.__tweets_text = '\n'.join(self.__tweets.text.values)
	#end

	def __create_model(self):
		self.__text_model = markovify.Text(self.__tweets_text)
	#end

	def generate(self):
		return self.__text_model.make_short_sentence(280)
		# return self.__tweets['text'].values[0]
	#end
#end
