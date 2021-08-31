from typing import overload


def folder_check() -> None:
    ...

def _log_subdir_check() -> None:
    ...

class StdLog:
    def __init__(self):
        ...

    def std_log_setup(self) -> None:
        ...

    def std_log_write(self, function_to_log:object) -> None:
        ...

class ArcpyLogging:
    def __init__(self):
        ...

    @staticmethod
    def setup_arc_log_dir() -> None:
        ...

    @overload
    def write_getmessage(self, msg: str) -> None:
        ...

    @overload
    def write_getmessage(self, msg: object) -> None:
        ...

class Error:
    def __init__(self):
        ...

    def get_err_message(self, exception:Exception) -> str:
        ...

    def error_handle(self, e:Exception):
        ...

    def error_handle_no_exit_quiet(self, e: Exception) -> None:
        ...

    def error_setup(self) -> None:
        ...

    def error_write(self) -> None:
        ...
