from collections.abc import Callable

def cprint(default: str ="\033[0;33m") -> Callable[[str], None]:
    """COLORPRINT/CPRINT: custom colorprint func, using currying"""
    def custom_print(string_: str) -> None:
        """COLORPRINT/CPRINT/CUSTOM_PRINT: returned, curried function
        for custom printing"""
        print(f"{default}{string_}\033[0m")
    return custom_print
