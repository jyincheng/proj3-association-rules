import csv
from itertools import combinations, chain

# read csv file
rows = []
row_sets = []
with open("INTEGRATED-DATASET2.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)
        row_sets.append(set(row))
print("size of rows:", len(rows))
print("size of row_sets:", len(row_sets))

# variables
MIN_SUPPROT = 0.01
MIN_CONFIDENCE = 0.3
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

k = 1
items = set()
for i in range(len(rows)):
    for j in range(len(rows[i])):
        items.add(rows[i][j])

print("size of items:", len(items))

L1 = []
cnt = 0
for item in sorted(items):
    for row_set in row_sets:
        if item in row_set:
            cnt += 1
    support = cnt/len(row_sets)
    # print(item, support)
    if support >= MIN_SUPPROT:
        item = tuple([item])
        items_to_support[item] = support
        L1.append(item)

print(f'size of initial large itemsets: {len(L1)}')

Lk = list(L1)

# Apriori
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
        support = round(cnt/len(rows), 4)

        if support > MIN_SUPPROT:
            candidate = tuple(sorted(candidate))
            items_to_support[candidate] = support
            next_Lk.append(candidate)

    k += 1
    Lk = next_Lk
    print("size of next_Lk:", len(Lk))
    print()

# find rules above min confidence
associate_rules_list = []
for combo in items_to_support:
    # ignore when combo have only one element
    if len(combo) < 1:
        continue

    for length in range(1, len(combo)):
        combines = list(combinations(combo, length))
        # print("combinations:", combines)
        for combine in combines:
            lhs = set(combine)
            rhs = set(combo).difference(lhs)
            lhs = tuple(lhs)
            rhs = tuple(rhs)
            lhs_and_rhs = combo

            # print("lhs:", lhs)
            # print("rhs:", rhs)

            confidence = items_to_support[lhs_and_rhs]/items_to_support[lhs]
            if confidence >= MIN_CONFIDENCE:
                  associate_rules_list.append([f'{lhs} -> {rhs}', round(confidence, 4)])

# print out association result
associate_rules_list.sort(key=lambda x: x[1], reverse=True)
for rule, confidence in associate_rules_list:
    print(f'{rule}: {confidence}')

file.close()