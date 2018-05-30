punctuation = ['.', ',', ';', ':', '?', '!', '(', ')', '_', '--', '-', '...', "''", '``', "'", '`']


def realize(sentence):
    # print(sentence[3])
    # print(len(sentence[4]), sentence[4])
    new_sentence = ''
    queue = []
    last_word_tag = ''
    last_punc = ''
    next_word_tag = ''
    for index in range(len(sentence[4])):
        if index + 1 < len(sentence[4]):
            next_word_tag = sentence[4][index + 1][1]
        else:
            next_word_tag = ''
        tag = sentence[4][index]
        if tag[0] in punctuation:
            new_sentence += process_queue(queue, last_punc, last_word_tag, next_word_tag, tag[0])
            last_punc = tag[0]
            queue = []
        else:
            queue.append(tag)
            last_word_tag = tag[1]

    new_sentence = new_sentence.replace(" 's", "'s")
    new_sentence = new_sentence.replace(" 're", "'re")
    new_sentence = new_sentence.replace(" n't", "n't")
    # print(new_sentence)
    # print(sentence)
    # print()

    sentence.append(new_sentence)
    return sentence


def process_queue(queue, last_punc, last_word_tag, next_word_tag, punc):
    # print(len(queue),queue)
    if len(queue) < 3:
        return ''
    elif last_punc == '--' and punc == '--':
        return ''
    elif last_punc == ',' and 'NN' in last_word_tag and ('VB' in next_word_tag or 'W' in queue[0][1]):
        # print(len(queue), queue)
        if punc == ',':
            return ' '
        else:
            return punc + ' '

    else:
        found_said = False
        for tag in queue:
            if tag[0].lower() == 'said':
                found_said = True

        if found_said and len(queue) < 10:
            # print(len(queue), queue)
            if punc == ',':
                return ' '
            else:
                return punc + ' '
        else:
            sentence = ''
            for tag in queue:
                sentence += tag[0] + ' '
            sentence = sentence.strip()

            if punc == '.' or punc == '?' or punc == '!':
                sentence += punc
            return sentence


def max_similarity(selected_sentences, test):
    max_match = 0
    words = test[5].split()
    if len(words) == 0:
        return 1
    for sentence in selected_sentences:
        similarity = 0
        for word in words:
            if word in sentence[5]:
                similarity += 1
        if similarity > max_match:
            max_match = similarity

    return max_match / len(words)
