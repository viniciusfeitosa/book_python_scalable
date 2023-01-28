import cProfile


def divisor(value):
    try:
        return 1/value
    except ZeroDivisionError as err:
        print(f'something wrong: {str(err)}')


def main():
    for i in reversed(range(100_000_000)):
        divisor(i)


if __name__ == '__main__':
    cProfile.run('main()')
