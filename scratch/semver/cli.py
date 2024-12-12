import fire
import inspect


def dispatch(args: list[str]):
    print(f"{__file__}:{inspect.currentframe().f_code.co_name}")


if "__main__" == __name__:
    fire.Fire(dispatch)
