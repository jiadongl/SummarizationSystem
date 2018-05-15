import operator


def order(selected_sentences):
    summary = ''
    # last_sentence = selected_sentences.pop()
    selected_sentences = sorted(selected_sentences, key=operator.itemgetter(0))
    for sentence in selected_sentences:
        summary += sentence[3]+'\n'
    # summary += last_sentence[3]
    return summary
