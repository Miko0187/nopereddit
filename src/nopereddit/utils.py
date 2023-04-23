import os
import pickle
import tempfile
from typing import Dict

tempdir = tempfile.gettempdir()
cache_file = f"{tempdir}/nopereddit.cache"


def _save_cache(cache: Dict[str, list]) -> None:
    """Saves the cache to a file.

    This method should only be used internally. Not by the user.

    Args
    ----
    `cache` type of `Dict[str, list]`
        The cache to save"""
    with open(cache_file, "wb") as file:
        pickle.dump(cache, file)


def _load_cache() -> Dict[str, list]:
    """Loads the cache from a file.

    This method should only be used internally. Not by the user.

    Returns
    -------
    `Dict[str, list]` type of `dict`
        The cache"""
    if not os.path.exists(cache_file):
        _save_cache({})
        return _load_cache()

    with open(cache_file, "rb") as file:
        return pickle.load(file)
