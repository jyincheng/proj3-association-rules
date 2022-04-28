import csv
from itertools import combinations, chain


def read_data():
    rows = []        # list of list
    row_sets = []    # list of set
    with open("INTEGRATED-DATASET.csv", 'r') as file:
        csvreader = csv.reader(file)
        included_cols = [0, 3, 4, 5]
        header = next(csvreader)
        for row in csvreader:
            content = list(row[i] for i in included_cols)
            rows.append(content)
            row_sets.append(set(content))

    file.close()

    return rows, row_sets


def create_next_candidates(prev_candidates, length):
    """
    Returns the next candidates(next_Ck) as a list.
    Arguments:
        prev_candidates -- Previous candidates as a list.
        length -- The lengths of the next candidates.
    """
    items = sorted(frozenset(chain.from_iterable(prev_candidates)))

    # join
    tmp_next_candidates = (frozenset(x) for x in combinations(items, length))

    if length < 3:
        return list(tmp_next_candidates)

    # prune
    next_candidates = [
        candidate for candidate in tmp_next_candidates
        if all(
            frozenset(x) in prev_candidates
            for x in combinations(candidate, length - 1))
    ]

    return next_candidates


def find_all_items(rows):
    """
    Returns the distince items as a set
    Arguments:
        rows -- all the transactions from raw data
    """
    items = set()
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            items.add(rows[i][j])

    return items


def construct_L1(items, row_sets, items_to_support):
    """
    Returns the one-item large frequency set(L1) as a list.
    Arguments:
        items -- distinct items
        row_sets -- all the transactions from raw data in set type
        items_to_support -- support values for all items above the MIN_SUPPORT as a dictionary
    """
    L1 = []
    for item in sorted(items):
        cnt = 0
        for row_set in row_sets:
            if item in row_set:
                cnt += 1
        support = round(cnt/len(row_sets), 4)
        
        if support >= MIN_SUPPROT:
            item = tuple([item])
            items_to_support[item] = support
            L1.append(item)

    return L1


def apriori(Lk, k, items_to_support):
    """
    Returns support values for all items above the MIN_SUPPORT as a dictionary
    Arguments:
        Lk -- k-items large frequency set
        k -- iteration index
    """
    while Lk:
        print("k:", k)
        print("size of Lk:", len(Lk))

        next_Ck = create_next_candidates(Lk, k+1)
        print("size of next_Ck:", len(next_Ck))
        
        next_Lk = []
        for candidate in next_Ck:
            cnt = 0
            for row_set in row_sets:
                if candidate.issubset(row_set):
                    cnt += 1
            support = round(cnt/len(row_sets), 4)

            if support > MIN_SUPPROT:
                candidate = tuple(sorted(candidate))
                items_to_support[candidate] = support
                next_Lk.append(candidate)

        k += 1
        Lk = next_Lk
        print("size of next_Lk:", len(Lk))
        print('==============================')
    
    return items_to_support
    

def find_associate_rules(items_to_support):
    """
    Returns associate_rules as a list
    Arguments:
        items_to_support -- support values for all items above the MIN_SUPPORT as a dictionary
    """
    associate_rules = []
    for combo in items_to_support:
        # ignore when combo have only one element
        if len(combo) <= 1:
            continue

        # rules should have exactly one item on RHS
        combines = list(combinations(combo, len(combo)-1))
        
        for combine in combines:
            lhs = set(combine)
            rhs = set(combo).difference(lhs)
            lhs = tuple(sorted(lhs))
            rhs = tuple(sorted(rhs))
            lhs_and_rhs = combo

            # print("lhs:", lhs)
            # print("rhs:", rhs)
            # print(lhs_and_rhs)

            confidence = items_to_support[lhs_and_rhs]/items_to_support[lhs]
            if confidence > 1:
                print(confidence)
                print(lhs_and_rhs)
                print(items_to_support[lhs_and_rhs])
                print(lhs)
                print(items_to_support[lhs])
            if confidence >= MIN_CONFIDENCE:
                    associate_rules.append([f'{lhs} -> {rhs}', round(confidence, 4)])

    return associate_rules


def print_associate_rules(associate_rules, MIN_SUPPORT, MIN_CONFIDENCE):
    print(f'Associate Rules (MIN_SUPPORT = {MIN_SUPPORT}, MIN_CONFIDENCE = {MIN_CONFIDENCE})\n')
    associate_rules.sort(key=lambda x: x[1], reverse=True)
    for rule, confidence in associate_rules:
        print(f'{rule}: {round(confidence*100, 2)}%')


def output_example_txt(items_to_support, associate_rules, MIN_SUPPROT, MIN_CONFIDENCE):
    with open('example-run.txt', 'w') as f:
        items_to_support_list = [[items, support] for items, support in items_to_support.items()]
        items_to_support_list.sort(key=lambda x: x[1], reverse=True)
        f.write(f'==Frequent itemsets (min_sup={MIN_SUPPROT*100}%)')
        for items, support in items_to_support_list:
            f.write(f'{items}: {round(support*100, 2)}%\n')

        f.write(f'==High-confidence association rules (min_conf={MIN_CONFIDENCE*100}%)')
        for rule, confidence in associate_rules:
            f.write(f'{rule}: {round(confidence*100, 2)}%\n')


if __name__ == '__main__':

    # read data
    rows, row_sets = read_data()
    print('==============================')
    print("size of rows:", len(rows))
    print("size of row_sets:", len(row_sets))
    print('==============================')

    # variables
    MIN_SUPPROT = 0.01
    MIN_CONFIDENCE = 0.6
    items_to_support = dict()    # {items: support val}

    # find all distinct items from dataset
    items = find_all_items(rows)
    print("size of items:", len(items))

    # construct largest one-item set
    L1 = construct_L1(items, row_sets, items_to_support)
    print(f'size of initial large itemsets: {len(L1)}')
    print('==============================')

    k = 1
    Lk = list(L1)

    # calculate support value
    items_to_support = apriori(Lk, k, items_to_support)
    
    # find associate rules above min confidence
    associate_rules = find_associate_rules(items_to_support)
    
    # display associate rules and output the results
    print_associate_rules(associate_rules, MIN_SUPPROT, MIN_CONFIDENCE)
    output_example_txt(items_to_support, associate_rules, MIN_SUPPROT, MIN_CONFIDENCE)
