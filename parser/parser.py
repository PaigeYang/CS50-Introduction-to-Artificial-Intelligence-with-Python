import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP PP Conj VP | NP VP Conj VP | NP VP Conj NP VP |
VP -> V | V NP | V NP PP | V P NP | V PP | V PP PP | Adv V NP | V Det NP | V PP Adv| Adv V Det NP | V Adv
NP -> N | Det NP | Det Adj NP | Det Adv Adj N | Adj NP
PP -> P NP | PP PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # to perform tokenization
    words = nltk.word_tokenize(sentence.lower())

    # exclude any word that doesn’t contain at least one alphabetic character
    for word in words:
        print (len(words))
        if word.isalpha():
            continue
        else:
            words.remove(word)

    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    NP_chunks = []
    tem = []

    #decode the tree to get NP subtree
    for s in tree.subtrees():

        if s.label() == "NP":

            # if NP is not the same as it's parent tree, add to NP_chunks list
            if not all(word in tem for word in s.leaves()):
                NP_chunks.append(s)

                # add to temporary list
                tem = tem + s.leaves()

    return NP_chunks

if __name__ == "__main__":
    main()
