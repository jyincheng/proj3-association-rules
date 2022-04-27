import csv
from itertools import combinations, chain

# read csv file
rows = []        # list of list
row_sets = []    # list of set
with open("INTEGRATED-DATASET.csv", 'r') as file:
    csvreader = csv.reader(file)
    included_cols = [0, 3, 4, 5]
    header = next(csvreader)
    for row in csvreader:
        content = list(row[i] for i in included_cols)
        print(len(content))
        rows.append(content)
        row_sets.append(set(content))
print("size of rows:", len(rows))
print("size of row_sets:", len(row_sets))

# variables
MIN_SUPPROT = 0.01
MIN_CONFIDENCE = 0.6

# {items: support val}
items_to_support = dict()

def create_next_candidates(prev_candidates, length):
    """
    Returns the apriori candidates as a list.
    Arguments:
        prev_candidates -- Previous candidates as a list.
        length -- The lengths of the next candidates.
    """
    # Solve the items.
    items = sorted(frozenset(chain.from_iterable(prev_candidates)))

    # Create the temporary candidates. These will be filtered below.
    tmp_next_candidates = (frozenset(x) for x in combinations(items, length))

    # Return all the candidates if the length of the next candidates is 2
    # because their subsets are the same as items.
    if length < 3:
        return list(tmp_next_candidates)

    # Filter candidates that all of their subsets are
    # in the previous candidates.
    next_candidates = [
        candidate for candidate in tmp_next_candidates
        if all(
            frozenset(x) in prev_candidates
            for x in combinations(candidate, length - 1))
    ]
    return next_candidates

# find all distinct items from dataset
items = set()
for i in range(len(rows)):
    for j in range(len(rows[i])):
        items.add(rows[i][j])

print("size of items:", len(items))

# construct large 1-itemsets
L1 = []
for item in sorted(items):
    cnt = 0
    for row_set in row_sets:
        if item in row_set:
            cnt += 1
    support = round(cnt/len(row_sets), 4)
    # print(item, support)
    if support >= MIN_SUPPROT:
        item = tuple([item])
        items_to_support[item] = support
        L1.append(item)

print(f'size of initial large itemsets: {len(L1)}')

# initialization
k = 1
Lk = list(L1)

print()

# Apriori
while Lk:
    print("k:", k)
    print("size of Lk:", len(Lk))
    # print(Lk)
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
    print()

print()
# find rules above min confidence
associate_rules_list = []
for combo in items_to_support:
    # ignore when combo have only one element
    if len(combo) <= 1:
        continue

    # rules should have exactly one item on RHS
    combines = list(combinations(combo, len(combo)-1))
    # print("combinations:", combines)
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
                associate_rules_list.append([f'{lhs} -> {rhs}', round(confidence, 4)])

# print out association result
associate_rules_list.sort(key=lambda x: x[1], reverse=True)
for rule, confidence in associate_rules_list:
    print(f'{rule}: {confidence}')

file.close()