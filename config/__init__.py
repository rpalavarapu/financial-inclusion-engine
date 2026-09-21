try:
    from .settings import *  # type: ignore
except ImportError:
    try:
        from .Settings import *  # type: ignore
    except ImportError:
        pass
