import numpy as np
import pandas as pd
from typing import List, Dict, Set, Tuple
from collections import Counter
import math

class InvertedIndex:
    """Efficient inverted index using posting lists."""
    def __init__(self):
        self.index: Dict[str, List[int]] = {}
        self.doc_lengths: Dict[int, int] = {}
        self.num_docs = 0

    def add_document(self, doc_id: int, tokens: List[str]):
        self.num_docs += 1
        self.doc_lengths[doc_id] = len(tokens)
        counts = Counter(tokens)
        for term in counts:
            if term not in self.index:
                self.index[term] = []
            self.index[term].append(doc_id)

    def get_postings(self, term: str) -> List[int]:
        return self.index.get(term, [])

    def get_vocabulary(self) -> Set[str]:
        return set(self.index.keys())

    def get_df(self, term: str) -> int:
        """Document Frequency"""
        return len(self.index.get(term, []))

class VectorSpaceModel:
    """Implements TF-IDF and Cosine Similarity for sentiment analysis."""
    def __init__(self, index: InvertedIndex):
        self.index = index
        self.vocab = sorted(list(index.get_vocabulary()))
        self.term_to_idx = {term: i for i, term in enumerate(self.vocab)}
        self.num_docs = index.num_docs

    def get_tf(self, count: int) -> float:
        """TF = 1 + log2(f_ij) if f_ij > 0 else 0"""
        if count > 0:
            return 1 + math.log2(count)
        return 0

    def get_idf(self, term: str) -> float:
        """IDF = log2(N/n_i)"""
        n_i = self.index.get_df(term)
        if n_i == 0:
            return 0
        idf = math.log2(self.num_docs / n_i)
        # Handle IDF=0 terms (discriminative reduction)
        if idf == 0:
            return 0.0001 # Small weight to avoid total loss but reduce importance
        return idf

    def vectorize(self, tokens: List[str]) -> np.ndarray:
        """Creates a TF-IDF vector for a list of tokens."""
        vector = np.zeros(len(self.vocab))
        counts = Counter(tokens)
        for term, count in counts.items():
            if term in self.term_to_idx:
                tf = self.get_tf(count)
                idf = self.get_idf(term)
                vector[self.term_to_idx[term]] = tf * idf
        return vector

    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0
        return np.dot(v1, v2) / (norm1 * norm2)

    def analyze_sentiment(self, doc_vector: np.ndarray, positive_query_vec: np.ndarray, negative_query_vec: np.ndarray) -> float:
        """Calculates sentiment score based on similarity to seed word vectors."""
        pos_sim = self.cosine_similarity(doc_vector, positive_query_vec)
        neg_sim = self.cosine_similarity(doc_vector, negative_query_vec)
        
        # Combined score (-1 to 1)
        return pos_sim - neg_sim
