from typing import Any, Callable, Dict, List, Optional
import webview
import inspect
import json
import asyncio
import os

from webview.guilib import GUIType

from haunt.binds import FunctionBind, FunctionBindType
from haunt.utils.async_sync import run_async_in_sync


class HauntClient:
    WEBVIEW_STARTED = False
    FUNCTION_BINDS: Dict[str, FunctionBind] = {}

    def __init__(self) -> None:
        self._load_patch_script()

    def _load_patch_script(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "..", "internal", "mount.js")
        with open(script_path, "r") as file:
            self.PATCH_SCRIPT = file.read()

    def mount(
        self,
        path: str,
        title: str,
        debug: bool = False,
        gui: Optional[GUIType] = None,
    ):
        """
        Creates and shows the HauntClient window.
        """

        def handle_window_patch(window: webview.Window):
            window.evaluate_js(self.PATCH_SCRIPT)

        self.api = HauntApi(client=self)
        self.window = webview.create_window(title, path, js_api=self.api)
        self.window.events.before_show += handle_window_patch
        if not self.WEBVIEW_STARTED:
            webview.start(debug=debug, gui=gui)
            self.WEBVIEW_STARTED = True

    def bind(
        self,
        func: Callable,
    ):
        """
        Binds a function to the HauntClient,
        allowing javascript code to call it.
        """

        sig = inspect.signature(func)
        name = func.__name__
        params = [name for name, _ in sig.parameters]
        is_async = inspect.iscoroutinefunction(func)
        self.FUNCTION_BINDS[name] = FunctionBind(
            bind_type=FunctionBindType.FROM_PYTHON,
            is_async=is_async,
            func=func,
            params=params,
        )

        return func


class FunctionNotFoundException(Exception):
    pass


class FunctionAlreadyExistsException(Exception):
    pass


class HauntApi:
    def __init__(
        self,
        client: HauntClient,
    ) -> None:
        self._client = client

    def call_function(
        self,
        func_name: str,
        args: List[Any],
    ) -> Any:
        func_bind = self._client.FUNCTION_BINDS.get(func_name)

        if not func_bind:
            raise FunctionNotFoundException()
        if func_bind.bind_type == FunctionBindType.FROM_PYTHON:
            assert func_bind.func
            result = func_bind.func(*args)
            if func_bind.is_async:
                return run_async_in_sync(result)
            else:
                return result

        elif func_bind.bind_type == FunctionBindType.FROM_JS:
            unpackedData = {"funcName": func_name, "args": args}
            packedData = json.dumps(unpackedData)
            code = f"window.haunt._exec_bind(`{packedData}`)"

            if func_bind.is_async:
                future = asyncio.get_event_loop().create_future()

                def func_callback(result):
                    future.set_result(result)

                self._client.window.evaluate_js(code, callback=func_callback)
                return run_async_in_sync(future)
            else:
                return self._client.window.evaluate_js(code)

    def bind_function(
        self,
        func_name: str,
        is_async: bool = False,
    ):
        if func_name in self._client.FUNCTION_BINDS:
            raise FunctionAlreadyExistsException()

        self._client.FUNCTION_BINDS[func_name] = FunctionBind(
            bind_type=FunctionBindType.FROM_JS,
            is_async=is_async,
        )
