import asyncio
import functools
import logging

from asyncio import create_task, ensure_future
from logging import getLogger
from traceback import format_exception
from typing import Any, Callable, Coroutine, Optional, Union
from models import LibraryAll
from starlette.concurrency import run_in_threadpool


log = getLogger("main")

NoArgsNoReturnFuncT = Callable[[], None]
NoArgsNoReturnAsyncFuncT = Callable[[], Coroutine[Any, Any, None]]
NoArgsNoReturnDecorator = Callable[
    [Union[NoArgsNoReturnFuncT, NoArgsNoReturnAsyncFuncT]], NoArgsNoReturnAsyncFuncT
]

MEM_CACHE_DICT = {}


def repeat_every(
    func: Union[NoArgsNoReturnAsyncFuncT, NoArgsNoReturnFuncT],
    on_end: NoArgsNoReturnFuncT,
    *,
    seconds: float,
    wait_first: bool = False,
    logger: Optional[logging.Logger] = None,
    raise_exceptions: bool = False,
    max_repetitions: Optional[int] = None,
):
    """
    This function queues a function to be periodically re-executed starting from
    the call to this function.

    The function passed should accept no arguments and return nothing. If necessary, this can be accomplished
    by using `functools.partial` or otherwise wrapping the target function prior to decoration.

    Parameters
    ----------
    seconds: float
        The number of seconds to wait between repeated calls
    wait_first: bool (default False)
        If True, the function will wait for a single period before the first call
    logger: Optional[logging.Logger] (default None)
        The logger to use to log any exceptions raised by calls to the decorated function.
        If not provided, exceptions will not be logged by this function (though they may be handled by the event loop).
    raise_exceptions: bool (default False)
        If True, errors raised by the decorated function will be raised to the event loop's exception handler.
        Note that if an error is raised, the repeated execution will stop.
        Otherwise, exceptions are just logged and the execution continues to repeat.
        See https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.set_exception_handler for more info.
    max_repetitions: Optional[int] (default None)
        The maximum number of times to call the repeated function. If `None`, the function is repeated forever.
    """
    is_coroutine = asyncio.iscoroutinefunction(func)
    repetitions = 0

    async def loop() -> None:
        nonlocal repetitions
        if wait_first:
            await asyncio.sleep(seconds)
        while max_repetitions is None or repetitions < max_repetitions:
            try:
                if is_coroutine:
                    await func()  # type: ignore
                else:
                    await run_in_threadpool(func)
                repetitions += 1
            except Exception as exc:
                if logger is not None:
                    formatted_exception = "".join(
                        format_exception(type(exc), exc, exc.__traceback__)
                    )
                    logger.error(formatted_exception)
                if raise_exceptions:
                    raise exc
            await asyncio.sleep(seconds)
        on_end()

    ensure_future(loop())


def set_cache(cache_id: str, value: Any):
    # just meme cache so far
    MEM_CACHE_DICT[cache_id] = value


def get_cache(cache_id: str) -> Any:
    return MEM_CACHE_DICT[cache_id]


def cache_cascade(
    cache_id: str,
    cache_every_h: int,
    stop_cache_after_h: int,
    caching_task: Any,
    pass_result: bool=False,
    precache: bool=True
):
    """
    If the end-point is requested, an iterative caching function is invoked
    in a loop at specific intervals. The cache loop will stop if the endpoint
    is not hit again after the maximum amount of time to keep re-caching (or)
    the release time.
    """
    cascade_stopped = True

    def cache_cascade():
        nonlocal cascade_stopped
        cascade_stopped = False

        def on_end():
            nonlocal cascade_stopped
            cascade_stopped = True

        repeat_every(
            func=functools.partial(caching_task, cache_id),
            # set released to True after max iter is reached
            on_end=on_end,
            seconds=cache_every_h * 60 * 60,
            raise_exceptions=True,
            logger=log,
            max_repetitions=stop_cache_after_h // cache_every_h,
        )

    def predicate(func):
        is_coroutine = asyncio.iscoroutinefunction(func)
        get_cached = lambda library: get_cache(cache_id.format(library=library.value))

        @functools.wraps(func)
        async def wrapped(library: LibraryAll):
            nonlocal cascade_stopped
            # cascade starts again when the endpoint is re-hit after stopped
            if cascade_stopped:
                cache_cascade()

            if pass_result:
                # here the wrapped function assumes control
                return await func(library) if is_coroutine else func(library)

            return get_cached(library)

        if pass_result:
            # expose cache getter to user's function
            wrapped.get_cached = get_cached
        return wrapped

    if precache:
        # call caching function once beginning
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            log.error("Missing asyncio runtime loop to initiate precaching.")
        else:
            create_task(caching_task(cache_id))
    else:
        raise Exception("It's unsafe to turn off precache at the moment.")

    return predicate
