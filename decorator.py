def attempt(
        n=5
):
    def decorator(
            func
    ):
        def wraps(
                *args,
                **kwargs
        ):
            print('-------')
            print(n)
            func(*args, **kwargs)
            print('-------')
            return

        return wraps

    return decorator


@attempt(n=5)
def my_print(name):
    print(f'Hello, {name}!')


@attempt(n=5)
def my_print2(name):
    print(f'Hello, {name}2!')

my_print(name='Ivan')
my_print2(name='Sasha')
