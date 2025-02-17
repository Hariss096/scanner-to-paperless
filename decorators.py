from aiohttp import ClientSession, ClientTimeout


def client_session(func):
    async def wrapper(*args, **kwargs):
        async with ClientSession(timeout=ClientTimeout(total=20)) as session:
            return await func(session, *args, **kwargs)

    return wrapper
