import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""
    pass


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.time()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        seconds = time.time() - self._start_time
        self._start_time = None
        minute = round(seconds / 60)
        return minute


obj = Timer()


def str_obj():
    return obj.start()


def stp_obj():
    return obj.stop()
