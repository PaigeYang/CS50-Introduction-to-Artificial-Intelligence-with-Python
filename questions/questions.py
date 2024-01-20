import sys
import nltk
import string
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    files = {}

    # list all files in the directory
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            content = f.read()

            # add file name as a key and file content as value
            files[filename] = content

    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # to perform tokenization
    words = nltk.word_tokenize(document.lower())

    # Filter out punctuation and stopwords
    for word in words.copy():
        if word in string.punctuation:
            words.remove(word)

        if word in nltk.corpus.stopwords.words("english"):
            words.remove(word)

    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # Get all words in all documents
    words = set()
    for filename in documents:
        words.update(documents[filename])

    # Calculate IDFs
    idfs = dict()
    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf


    return idfs



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    # Get all words in files
    words = set()
    for filename in files:
        words.update(files[filename])

    """
    # Calculate IDFs for each word
    idfs = dict()
    for word in words:
        f = sum(word in files[filename] for filename in files)
        idf = math.log(len(files) / f)
        idfs[word] = idf
    """

    # Calculate term frequencies (tf) in each document
    documents = dict()

    for filename in files:
        # Count frequencies
        frequencies = dict()
        for word in files[filename]:
            if word not in frequencies:
                frequencies[word] = 1
            else:
                frequencies[word] += 1

        documents[filename] = frequencies

    # Calculate TF-IDFs based on the query
    tfidfs = dict()
    for filename in files:

        for word in query:
            if word in documents[filename]:
                tf = documents[filename][word]

                if filename not in tfidfs:
                    tfidfs[filename] = tf * idfs[word]

                else:
                    tfidfs[filename] = tfidfs[filename] + tf * idfs[word]

    # sort and get top n TF-IDFs file
    tfidfs = sorted(tfidfs.items(), key=lambda filename: filename[1], reverse=True)[:n]

    top_files = []
    for filename, tfidf in tfidfs:
        top_files.append(filename)

    return top_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # create a list to calcuate each sentence's idf and query term density
    sen_idf = []

    # show the word's idf in the sentences, the word that appears in query
    sen_word_idf = {}
    for sentence in sentences:
        idf = 0
        frequency = 0

        for word in query:
            if word in sentences[sentence]:
                if sentence not in sen_word_idf:
                    sen_word_idf[sentence] = [(word, idfs[word])]
                else:
                    sen_word_idf[sentence].append((word, idfs[word]))

                idf = idf + idfs[word]
                frequency += 1
        sen_idf.append((sentence, (idf, frequency/len(sentences[sentence]))))

    # sort and get top n sentences for the file
    sen_idf.sort(key=lambda x: (x[1][0], x[1][1]), reverse=True)
    sen_idf = sen_idf[:n]

    # get the result
    top_sentences = []
    for sentence, idf in sen_idf:
        top_sentences.append(sentence)
        #print (sen_word_idf[sentence])

    return top_sentences


if __name__ == "__main__":
    main()
