import pandas as pd
import csv


def read_file_to_df(file):
    name = ('data/' + file)
    data = pd.read_csv(name)
    return data


def qp_to_word_list(data):
    # "","Id","StateAbbr","QuestionUno","CreatedUtc","PostText"
    my_array = [[]]
    count = 0
    texty_text = []
    qUnos = []
    for i in range(len(data)):
        state = data.iloc[i, 2]
        qUno = data.iloc[i, 3]
        text = data.iloc[i, 5]
        if issubclass(type(text), str):
            split_text = text.lower().split()
            print(i)
            if qUno in qUnos:
                my_state = my_array[qUnos.index(qUno)][1]
                count = count + 1
                for word in split_text:
                    my_array[qUnos.index(qUno)][3].append(word)
                    texty_text = my_array[qUnos.index(qUno)][3]
                my_array[qUnos.index(qUno)] = (qUno, my_state, count, texty_text)
            else:
                count = 0
                new_array = (qUno, state, count, split_text)
                my_array.append(new_array)
                qUnos.append(qUno)
    return my_array


def split_by_resp(data):
    web_dic = load_the_dictionary()
    res_arr = []
    no_res_arr = []
    for i in data:
        if is_picked_up(i[0], web_dic):
            res_arr.append(i)
        else:
            no_res_arr.append(i)
    return res_arr, no_res_arr


def dic_state(arr_init):
    dic = {}
    for line in arr_init:
        state = line[1]
        if state not in dic:
            dic[state] = []
        for j in line[3]:
            dic[state].append(j)

    return dic


def isnan(value):
    try:
        import math
        return math.isnan(float(value))
    except:
        return False

def load_the_dictionary():
    the_one_and_only = read_file_to_df('/questions.csv')
    the_cooler_dave = the_one_and_only.iloc[:, 8:11]
    question_uno = the_one_and_only.iloc[:, 2:3]
    asked_on_utc = the_cooler_dave.iloc[:, 0:1]
    list_of_attorney_taken = the_cooler_dave.iloc[:, 1:2]
    list_of_date_taken = the_cooler_dave.iloc[:, 2:3]

    the_webster_dictionary = {}
    for i in range(len(question_uno)):
        list_temp = [asked_on_utc.iloc[i, 0], list_of_attorney_taken.iloc[i, 0], list_of_date_taken.iloc[i, 0]]
        the_webster_dictionary[question_uno.iloc[i, 0]] = list_temp

    return the_webster_dictionary


def is_picked_up(question_id, the_webster_dictionary):
    element_list = the_webster_dictionary[question_id]
    if isnan(element_list[1]) and isnan(element_list[2]):
        return False
    else:
        return True


def concat_the_states(data):
    grouped = data.groupby('StateAbbr')
    df = pd.DataFrame({})
    list_of_state_abbr = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CT', 'FL', 'GA',
                          'IL', 'HI', 'IA', 'IN', 'KS', 'LA', 'MA', 'MD',
                          'ME', 'MI', 'MO', 'MS', 'NC', 'NE', 'NH', 'NJ',
                          'NM', 'NY', 'OK', 'PA', 'SC', 'SD', 'TN', 'TX',
                          'UT', 'US', 'VA', 'VT', 'WI', 'WV', 'WY']
    for state_abbr in list_of_state_abbr:
        subset = grouped.get_group(state_abbr).head(150)
        df = pd.concat([df, subset])
    return df


def word_counter(d):
    dict_word_count = {'AK': {}, 'AL': {}, 'AR': {}, 'AZ': {}, 'CA': {}, 'CT':{}, 'FL':{}, 'GA':{},
                          'IL':{}, 'HI':{}, 'IA':{}, 'IN':{}, 'KS':{}, 'LA':{}, 'MA':{}, 'MD':{},
                          'ME':{}, 'MI':{}, 'MO':{}, 'MS':{}, 'NC':{}, 'NE':{}, 'NH':{}, 'NJ':{},
                          'NM':{}, 'NY':{}, 'OK':{}, 'PA':{}, 'SC':{}, 'SD':{}, 'TN':{}, 'TX':{},
                          'UT':{}, 'US':{}, 'VA':{}, 'VT':{}, 'WI':{}, 'WV':{}, 'WY':{}}
    for state in d.keys():
        for value in d[state]:
            a = dict_word_count[state].keys()
            if value in a:
                dict_word_count[state][value] = dict_word_count[state][value] + 1
            else:
                value_dic = dict_word_count[state]
                value_dic[value] = 1
                dict_word_count[state] = value_dic

    return dict_word_count


def org(d):
    sorted_dic = {k: dict(sorted(v.items(), key=lambda item: -item[1])) for k, v in d.items()}
    return sorted_dic


def main():
    the_og = read_file_to_df("no_res_count_dic.csv")
    df = read_file_to_df("04_questionposts_corrected_full.csv")
    # call the concat states method
    talisman = concat_the_states(df)
    words_array = qp_to_word_list(talisman)
    words_array = words_array[1:]
    res_arr, no_res_arr = split_by_resp(words_array)
    res_state_dic = dic_state(res_arr)
    no_res_state_dic = dic_state(no_res_arr)
    yes_word = word_counter(res_state_dic)
    yes_arr = org(yes_word)
    no_arr = org(word_counter(no_res_state_dic))

    with open('data/res_count_dic.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(yes_arr.keys())
        writer.writerow(yes_arr.values())
    with open('data/no_res_count_dic.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(no_arr.keys())
        writer.writerow(no_arr.values())


if __name__ == '__main__':
    main()
