import operator


def order(selected_sentences):
    # print("*****IO*****")
    summary = ''
    selected_sentences = sorted(selected_sentences, key=operator.itemgetter(0))
    for sentence in selected_sentences:
        # print(sentence)
        summary += sentence[3]+'\n'
    return summary
