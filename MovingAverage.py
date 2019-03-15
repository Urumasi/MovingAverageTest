#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Petr Salaba <salabapetr@email.cz>


def avg(l):
    return sum(l) / len(l)


class MovingAverage:
    def __init__(self, l, r):
        self.list = l
        self.range = r
        self.idx = 0
        self.result = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx >= len(self.list):
            raise StopIteration

        self.result += self.list[self.idx] / self.range

        if self.idx >= self.range:
            self.result -= self.list[self.idx-self.range] / self.range

        self.idx += 1

        # Return true average if window is still incomplete
        if self.idx < self.range:
            return avg(self.list[0:self.idx])

        return self.result
