#!/bin/python3

import math
import os
import random
import re
import sys


# each person can bribe max two persons directly in front of him, so a person can move forward at most 2 positions, any seq violating this is invalid. at first, i person stay at i index, so i > 2 can only be moved fw to either i-1 or i-2. but i can be moved bw as far as possible, by keep swapping it with the person behind. So i can be only in range [i-2, n]. Esp n can only be at 1 of 3 positions n-2, n-1, n.
# if q_n = n, ie. in final state n is still at last pos, the best way is that he made no bribe at all, so min_bribe(q) = min_bribe(q\n)
# if ...

# CONST = 10**6
def minimumBribes(q):
    res = min_bribe(q)
    if res < 0:
        print('Too chaotic')
    else:
        print(str(res))


def min_bribe(q):
    m = len(q)
    # print('queue length:', m)
    # stop cond
    if m == 1:
        return 0
    if m == 2:
        if q == [1, 2]:
            return 0
        else:
            return 1

    if m > 2:
        q = [0] + q  # add a dummy s.t. actual items are indexed from 1

        def cal_n_bribe(i, queue):
            # during the process, i is always the largest item in queue
            if queue[i] == i:  # i stays at the last pos, no bribe
                queue.pop()
                return 0
            elif queue[i - 1] == i:  # i move fw 1 pos by making 1 bribe
                queue.pop(i - 1)
                return 1
            elif queue[i - 2] == i:  # i move fw 2 pos by making 2 bribes
                queue.pop(i - 2)
                return 2
            else:  # i move fw more than 2 pos, invalid
                # todo: check for some way to exit early
                return -1

        n_bribes = [cal_n_bribe(i, q) for i in range(m, 2, -1)]
        # print('list of bribes made:', n_bribes)
        if -1 in n_bribes:
            return -1
        q.pop(0)
        if q == [2, 1]:
            return sum(n_bribes) + 1
        return sum(n_bribes)


if __name__ == '__main__':
    t = int(input())

    for t_itr in range(t):
        n = int(input())

        q = list(map(int, input().rstrip().split()))

        minimumBribes(q)
