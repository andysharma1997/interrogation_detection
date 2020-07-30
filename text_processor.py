from textblob import TextBlob


def sentence_breaker(sentence):
    """
    This method extracts all the sentences present in a single long sentence using TextBlob
    @param sentence: str
    @return: list of sentences present
    """
    if len(sentence.split()) > 0:
        testimonial = TextBlob(sentence)
        sentences = []
        for sent in testimonial.sentences:
            sentences.append(str(sent))
        return sentences
