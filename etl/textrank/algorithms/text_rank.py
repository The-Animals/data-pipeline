import math
import numpy

class Summarizer():
    epsilon = 1e-4
    damping = 0.85
    _delta = 1e-7

    def __init__(self, mla):
        self.mla = mla
        self.ratings = self.rateSentences()

    def rateSentences(self):
        self.matrix = self.createMatrix()
        ranks = self.powerMethod()

        for sentence, rank in zip(self.mla.sentences, ranks):
            sentence.rank = rank

    def createMatrix(self):
        numberOfSentences = self.mla.numberOfSentences
        weights = numpy.zeros((numberOfSentences, numberOfSentences))
        sentences = self.mla.sentences

        for i, sentence_i in enumerate(sentences):
            for j, sentence_j in enumerate(sentences):
                weights[i, j] = self.compareSentences(sentence_i, sentence_j)

        divider = weights.sum(axis=1) # collective weights of each sentence in one dimensional matrix
        divider = divider[:, numpy.newaxis] # make that matrix a 2-dimensional
        divider += self._delta # to ensure there is no zero-division

        weights /= divider # divide by divider. Weights are now between 0 and 1

        return numpy.full((numberOfSentences, numberOfSentences), (1.-self.damping) / numberOfSentences) + self.damping * weights

    def compareSentences(self, s1, s2):
        rank = 0.0
        for w1 in s1.tokens:
            for w2 in s2.tokens:
                if w1 == w2:
                    rank += 1.0

        if rank == 0.0:
            return 0.0

        s1Length = s1.length
        s2Length = s2.length

        norm = math.log(s1Length) + math.log(s2Length)
        if s1Length == s2Length == 1:
            # This should only happen when words1 and words2 only have a single word.
            # Thus, rank can only be 0 or 1.
            return rank
        else:
            return rank / norm

    def powerMethod(self):
        transposed_matrix = self.matrix.T
        sentences_count = len(self.matrix)
        p_vector = numpy.array([1.0 / sentences_count] * sentences_count)
        lambda_val = 1.0

        while lambda_val > self.epsilon:
            next_p = numpy.dot(transposed_matrix, p_vector)
            lambda_val = numpy.linalg.norm(numpy.subtract(next_p, p_vector))
            p_vector = next_p

        return p_vector
