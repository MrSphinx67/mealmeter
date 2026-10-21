"""ASGI omotač za platforme koje ne šalju lifespan (Vercel, Korak 5V); vidi api/index.py."""

import asyncio


class LifespanOnDemand:
    """ASGI omotač: lifespan unutarnje Starlette aplikacije radi u zasebnom zadatku od prvog zahtjeva do kraja
    procesa. Putanja "/api/index..." (ako je platforma prepiše na funkciju) svodi se na ostatak."""

    def __init__(self, app, inner):
        self.app, self.inner = app, inner
        self._lock: asyncio.Lock | None = None
        self._task: asyncio.Task | None = None
        self._ready = False

    async def start(self) -> None:
        if self._ready:
            return
        self._lock = self._lock or asyncio.Lock()
        async with self._lock:
            if self._ready:
                return
            started, failed = asyncio.Event(), []

            async def run():
                try:
                    async with self.inner.router.lifespan_context(self.inner):
                        started.set()
                        await asyncio.Event().wait()  # do kraja procesa (ili cancel pri shutdownu)
                except Exception as e:  # noqa: BLE001
                    failed.append(e)
                    started.set()

            self._task = asyncio.create_task(run())
            await started.wait()
            if failed:
                raise failed[0]
            self._ready = True

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            while True:
                msg = await receive()
                if msg["type"] == "lifespan.startup":
                    await self.start()
                    await send({"type": "lifespan.startup.complete"})
                elif msg["type"] == "lifespan.shutdown":
                    if self._task:
                        self._task.cancel()
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        await self.start()
        path = scope.get("path", "")
        if path == "/api/index" or path.startswith("/api/index/"):
            rest = path[len("/api/index"):] or "/"
            scope = {**scope, "path": rest, "raw_path": rest.encode()}
        await self.app(scope, receive, send)


def inner_app(app):
    """Unutarnja Starlette aplikacija ispod RequestLog/HostGuard/RateLimit."""
    while hasattr(app, "app"):
        app = app.app
    return app
