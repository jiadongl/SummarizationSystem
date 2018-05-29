import operator


def order(selected_sentences):
    summary = ''
    selected_sentences = sorted(selected_sentences, key=operator.itemgetter(0))
    for sentence in selected_sentences:
        summary += sentence[5]+'\n'
    return summary
