import timeit

LOOP_VALUE = 1_000_000


def run_for() -> int:
    resp = 0
    for i in range(LOOP_VALUE):
        resp += i
    return resp


def run_while() -> int:
    resp = 0
    i = 0
    while i < LOOP_VALUE:
        resp += i
        i += 1
    return resp


if __name__ == '__main__':
    print('for execution  : ', timeit.timeit(run_for, number=5))
    print('while execution: ', timeit.timeit(run_while, number=5))
