import logging

def getLogger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    # fileHandler = logging.FileHandler("debug.log")
    # fileHandler.setFormatter(logFormatter)
    # logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger

def functionLogging(fn):
    """ prepare logging obkect
    """
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s\t%(name)s\t: %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='debug.log')
    log = logging.getLogger(fn.__name__)
    log.debug("called with args %s" % (args,))


# Number of times to indent output
# A list is used to force access by reference
__report_indent = [0]

def report(fn):
    """Decorator to print information about a function
    call for use while debugging.
    Prints function name, arguments, and call number
    when the function is called. Prints this information
    again along with the return value when the function
    returns.
    """

    def wrap(*params,**kwargs):
        call = wrap.callcount = wrap.callcount + 1

        indent = ' ' * __report_indent[0]
        fc = "%s(%s)" % (fn.__name__, ', '.join(
            [a.__repr__() for a in params] +
            ["%s = %s" % (a, repr(b)) for a,b in kwargs.items()]
        ))

        print "%s%s called [#%s]" % (indent, fc, call)
        __report_indent[0] += 1
        ret = fn(*params,**kwargs)
        __report_indent[0] -= 1

        return ret
    wrap.callcount = 0
    return wrap