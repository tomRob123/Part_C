class Document:

    def __init__(self, tweet_id=None,tokenized_text=None,term_doc_dictionary=None): #todo added in part c
        """
        :param tweet_id: tweet id
        :param tweet_date: tweet date
        :param tokenized_text: tokenized_text
        :param term_doc_dictionary: dictionary of term and documents.
        :param buzzwords_coefficient: measurement of entities in tweet
        :param doc_length: doc length
        """
        self.tweet_id = tweet_id
        self.tokenized_text = tokenized_text
        self.term_doc_dictionary = term_doc_dictionary

