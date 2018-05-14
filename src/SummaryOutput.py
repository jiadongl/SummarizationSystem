import os

OutputDir = '../outputs/D3/'


def output(topic_id, summary):
    id_part1 = topic_id[:-1]
    id_part2 = topic_id[-1:]
    file_name = ('%s-A.M.100.%s.10.txt' % (id_part1, id_part2))
    output_path = os.path.join(OutputDir, file_name)

    try:
        with open(output_path, "w+") as f:
            f .write(summary)
            print(summary)
    except IOError:
        print("Fail to output summary for " + topic_id)
