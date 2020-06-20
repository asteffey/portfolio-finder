from progressbar import progressbar as _progressbar


def progressbar(iterator, enabled=True):
    """Displays a progressbar for the iterator."""
    if enabled:
        return _progressbar(iterator)
    return iterator
