import asyncio


def run_async_in_sync(func, *args, **kwargs):
    """
    Run an async function synchronously.
    """
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # For nested event loops (e.g., when using frameworks like Jupyter)
        # Use asyncio.run_coroutine_threadsafe or a custom executor
        coro = func(*args, **kwargs)
        future = asyncio.ensure_future(coro)
        return future.result()  # This might block; use carefully in a running loop
    else:
        return loop.run_until_complete(func(*args, **kwargs))
