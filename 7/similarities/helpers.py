from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    file1_lines = set(a.splitlines())
    file2_lines = set(b.splitlines())
    similarities = [str(i) for i in file1_lines.intersection(file2_lines)]
    return similarities


def sentences(a, b):
    """Return sentences in both a and b"""
    file1_sentences = set(sent_tokenize(a))
    file2_sentences = set(sent_tokenize(b))
    similarities = [str(i) for i in file1_sentences.intersection(file2_sentences)]
    return similarities


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    def substr(string, n):
        return [string[i:n + i] for i in range(len(string) - n + 1)]
    file1_substrings = set(substr(a, n))
    file2_substrings = set(substr(b, n))
    similarities = [str(i) for i in file1_substrings.intersection(file2_substrings)]
    return similarities

