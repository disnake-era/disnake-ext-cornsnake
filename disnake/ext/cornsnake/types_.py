import typing as t

if t.TYPE_CHECKING:
    from typing_extensions import Concatenate, ParamSpec
else:
    def ParamSpec(*_: ..., **__: ...) -> ...:  # noqa: N802
        ...

    Concatenate = t.Generic

from disnake import AppCmdInter

P = ParamSpec("P", default=[AppCmdInter])

SlashCommandCallbackType = t.Callable[Concatenate[P], t.Any]
