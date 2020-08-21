#!/bin/python3

import os
import string

UPPERS = string.ascii_uppercase


# Complete the abbreviation function below.
def abbreviation(a, b):
    if can_match(b, a):
        return 'YES'
    else:
        return 'NO'


def has_capital_letter(s):
    # check if there is any capital letter in string s
    for ch in s:
        if ch in UPPERS:
            return True
    return False


def is_match(c1, c2):
    # given two letters c1, c2, return if c1 matches c2, where a match = (c1==c2) or (c1.upper()==c2)
    return (c1 == c2) or (c1.upper() == c2)


def can_match(b, a):
    # In general, we will match b[k:] to a[j:] and dups will happen, bc when we match b[k-1:] with a[j':],
    # whre j' < j, we already check if b[k:] can be matched with a[j:].
    # To avoid dups, we will use an array to store the finished matches and go backward
    # Let match[k][j] be the result of matching b[-k:] against a[-j:],
    # ie. k last chars of b against UP TO j last chars of a,
    # NOTE: b[-k:] may match with just a[-j':], j' <= j, then extend to a[-j:]
    # Then final result is match[m][n], m = len(b), n = len(a).

    # init match array
    print('\nMatch str', b, 'against str', a)
    n, m = len(a), len(b)
    rows, cols = m + 1, n + 1
    match = [[False for j in range(cols)] for i in range(rows)]
    match[0][0] = True
    for i in range(1, cols):
        # an empty b can only be matched with a[-i:] if a[-i:] contain all lowercases
        match[0][i] = not has_capital_letter(a[-i:])

    # match last k letters of b, given that last its k-1 letters are matchable
    for k in range(1, rows):
        print('\tmatching last {} letters of b'.format(k))
        # pick the shortest match of b[-(k-1):], as longer matches may pass an occurence of b[-k]
        # it will be the first i s.t. match[k-1][i] = 1
        i = match[k - 1][:].index(True)
        print('\ti:', i)

        # find the shortest match for b[-k:], ie. match b[-k:]  with a[-j:]
        #  s.t. all below conds are met:
        # i) is_match(a[-j], b[-k])
        # ii) no capital letter between a[-(j-1):-i],
        shortest_match = None
        for j in range(i + 1, cols):
            mid = get_in_between(a, j, i)
            no_capital_in_between = not has_capital_letter(mid)
            if is_match(a[-j], b[-k]) and no_capital_in_between:
                match[k][j] = True
                shortest_match = j
                break
        # if found shortest match then
        # continue to extend by adding lower letters until not possible, ie. hitting a capital
        if shortest_match:
            for r in range(shortest_match + 1, cols):
                if a[-r] not in UPPERS:
                    match[k][r] = True
                else:
                    break
            print('\trow', k, 'of match matrix:', match[k][:])
        else:
            # no match, so even a substr of b cannot match,
            #  so full b also fails, must exit here
            print('Fail to match', k, 'last letters of b. False')
            return False

    res = match[m][n]
    print(res)
    return res


def get_in_between(a, j, i):
    # return the part in between a[-j] and a[-i], excluding two ends
    if i > 0:
        in_between = a[-(j - 1): -i]
    # if i=0 the above wrongly return '', instead need a[-(j - 1):]
    if i == 0 and j == 1:
        in_between = ''
    if i == 0 and j > 1:
        in_between = a[-(j - 1):]
    print('\tsubstr of a from', -(j - 1), 'to', -(i + 1), ':', in_between)
    return in_between


if __name__ == '__main__':
    try:
        fptr = open(os.environ['OUTPUT_PATH'], 'w')
    except PermissionError:
        test = int(input())
        fptr = open('../abbr-testcases/output/my_out_{}.txt'.format(test), 'w')

    q = int(input())

    for q_itr in range(q):
        a = input()

        b = input()

        result = abbreviation(a, b)

        fptr.write(result + '\n')

    fptr.close()
