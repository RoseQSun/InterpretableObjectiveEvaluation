from multiprocessing.pool import ThreadPool as Pool
import signal
from functools import partial

import tqdm
from music21 import *


# ------- Loading --------


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException()


def _timeout(seconds=10):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator


def _load_score(filepath):
    return converter.parse(filepath)


def load_score_timeout(filepath, pbar=None, timeout=3):
    """ Load a single score with timeout setting """
    @_timeout(timeout)
    def _load_score_timeout(filepath):
        return converter.parse(filepath)
    if pbar: pbar.update(1)
    try:
        return _load_score_timeout(filepath)
    except TimeoutException:
        return None


def load_score(filepath, pbar=None):
    if pbar: pbar.update(1)
    return _load_score(filepath)


PROCESSES = 8

def load_scores_multithread(filepaths):
    """ Load multiple scores with multithreading """
    pbar = tqdm.tqdm(total=len(list(filepaths)))
    with Pool(PROCESSES) as pool:
        result_list = pool.map(partial(load_score, pbar=pbar), filepaths)
    return result_list


def load_scores_timeout(filepaths, timeout=3):
    """ Load multiple score with timeout """
    pbar = tqdm.tqdm(total=len(list(filepaths)))
    result_list = []
    for fp in filepaths:
        result_list.append(load_score_timeout(fp, pbar=pbar, timeout=timeout))
    return result_list
