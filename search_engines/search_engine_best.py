import pandas as pd

from configurations import utils
from parser_classes.parsers.parser_module import Parse
from indexers.indexer import Indexer
from query_expanders.thesaurus_expander import thesaurus_expander
from searchers.searcher import Searcher
from configurations.configuration import ConfigClass


# DO NOT CHANGE THE CLASS NAME

class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse(config.get_stemming())
        self._indexer = Indexer(config)
        self._model = None

        config.set_spell_checker(spell_checker=None)
        config.set_query_expander(query_expandor=thesaurus_expander())

        # create parent directories for postings
        utils.create_parent_dir(config.get_stemming_dir_path())
        utils.create_parent_dir(config.get_tweets_postings_path())

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def build_index_from_parquet(self, fn):
        """
        Reads parquet file and passes it to the parser, then indexer.
        Input:
            fn - path to parquet file
        Output:
            No output, just modifies the internal _indexer object.
        """
        df = pd.read_parquet(fn, engine="pyarrow")
        documents_list = df.values.tolist()
        # Iterate over every document in the file
        number_of_documents = 0
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document)
            number_of_documents += 1
            # index the document data
            self._indexer.add_new_doc(parsed_document)
        # print('Finished parsing and indexing. commencing post processing...')

        # make sure the postings and indexer are up to date
        self._indexer.post_process()

        # print('Finished post processing.')

        # self._indexer.save_index(fn=self._indexer.get_config().get_index_name())

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        self._indexer.load_index(fn)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_precomputed_model(self, model_dir=None):
        """
        Loads a pre-computed model (or models) so we can answer queries.
        This is where you would load models like word2vec, LSI, LDA, etc. and 
        assign to self._model, which is passed on to the searcher at query time.
        """
        pass

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query):
        """ 
        Executes a query over an existing index and returns the number of 
        relevant docs and an ordered list of search results.
        Input:
            query - string.
        Output:
            A tuple containing the number of relevant search results, and 
            a list of tweet_ids where the first element is the most relevant
            and the last is the least relevant result.
        """
        searcher = Searcher(self._parser, self._indexer, model=self._model)
        # print('Commencing searching and ranking...')
        n_res,res = searcher.search(query)
        # print('Finished searching and ranking...')
        return n_res,res

def main():
    config = ConfigClass()

    se = SearchEngine(config)
    se.build_index_from_parquet(config.get_corpusPath())

    n_res, res = se.search('operation lockstep rockefeller')
    print("Tweet id: {}".format(res))
