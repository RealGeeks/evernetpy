from itertools import tee
from types import GeneratorType

Tee = tee([], 1)[0].__class__

def memoize(f):
    cache={}
    def ret(*args):
        if args not in cache:
            cache[args]=f(*args)
        if isinstance(cache[args], (GeneratorType, Tee)):
            # the original can't be used any more,
            # so we need to change the cache as well
            cache[args], r = tee(cache[args])
            return r
        return cache[args]
    return ret
