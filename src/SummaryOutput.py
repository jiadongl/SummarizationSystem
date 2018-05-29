import os


def output(output_dir, topic_id, summary):
    id_part1 = topic_id[:-1]
    id_part2 = topic_id[-1:]
    file_name = ('%s-A.M.100.%s.10' % (id_part1, id_part2))
    output_path = os.path.join(output_dir, file_name)

    try:
        with open(output_path, "w+") as f:
            f .write(summary)
    except IOError:
        print("Fail to output summary for " + topic_id)
