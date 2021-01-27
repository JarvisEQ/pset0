#!/usr/bin/env python3


def last_8(some_int):
    """Return the last 8 digits of an int

    :param int some_int: the number
    :rtype: int
    """
    
    # short and sweet
    return some_int % 100000000


def optimized_fibonacci(f):
    
    # dynamic programming ftw
    
    mem = []

    for i in range(f + 1):
        
        if i == 0:
            mem.append(0)
        elif i < 3:
            mem.append(1)
        else: 
            tmp = mem[i - 1] + mem[i - 2]
            mem.append(tmp)

    return mem[f]



class SummableSequence(object):
    def __init__(self, *initial):
        
        self.initial = []

        for item in initial:
            self.initial.append(item)

    def __call__(self, f):
        
        mem = []
        for i in range(f + 1):

            if i < len(self.initial):
                mem.append(self.initial[i])
            else:
                tmp = mem[i - 1] + mem[i - 2]
                mem.append(tmp)

        return mem[f]


if __name__ == "__main__":

    print("f(100000)[-8:]", last_8(optimized_fibonacci(100000)))

    new_seq = SummableSequence(5, 7, 11)
    print("new_seq(100000)[-8:]:", last_8(new_seq(100000)))
