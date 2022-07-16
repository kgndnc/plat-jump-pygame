def read_hi_scores():
    try:
        file = open("hi_scores.txt", "r")
        sline_text = file.readline()
        if sline_text == "":
            score_list = [0] * 10

        elif not (sline_text.startswith("[") and sline_text.endswith("]")):
            score_list = [0] * 10
            write_hi_score(score_list)
            return score_list
        else:
            score_list = sline_text[1:-1].split(", ")
            score_list = [int(e) for e in score_list]

        file.close()
    except:
        try:
            create_file = open("hi_scores.txt", "x")
            score_list = [0] * 10
            create_file.close()
        except:
            print("Something went wrong")
            return False

    return score_list


def check_hi_score(curr_score: int):
    score_list = read_hi_scores()

    is_hi_score = False

    if curr_score > score_list[-1]:
        is_hi_score = True

    score_list.append(curr_score)
    score_list.sort(reverse=True)
    score_list = score_list[:10]

    write_hi_score(score_list)

    return is_hi_score


def write_hi_score(score_list):
    open("hi_scores.txt", "w").write(str(score_list))
