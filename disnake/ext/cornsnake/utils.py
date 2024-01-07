# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, cast

if TYPE_CHECKING:
    from typing import Any, TypeVar

    from typing_extensions import ParamSpec

    P = ParamSpec("P")
    T = TypeVar("T")


def copy_sig(_: Callable[P, Any]) -> Callable[[Callable[..., T]], Callable[P, T]]:
    def inner(func: Callable[..., T]) -> Callable[P, T]:
        return cast(Callable[P, T], func)
    return inner
