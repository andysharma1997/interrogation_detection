from spacy.matcher import PhraseMatcher
import spacy

nlp = spacy.load("en_core_web_sm")


def phrase_maker():
    """:returns this method returns the span of the patterns it matches."""
    global nlp
    print("Creating the Phrase matcher using spacy vocab of small model")
    phrase_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    question_terms = ["who", "whom", "whose", "what", "when", "where", "why", "which", "how"]
    patterns = [nlp(text) for text in question_terms]
    phrase_matcher.add("question", None, *patterns)
    return phrase_matcher


def get_doc(sentence):
    """
    :parameter  input sentence
    :returns The doc of input sentence
    """
    global nlp
    return nlp(sentence)
