import warnings
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    List,
    NewType,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from typing_extensions import Literal, Protocol

if TYPE_CHECKING:
    import magicgui.widgets
    import numpy as np
    import qtpy.QtWidgets


# General types

# PathLike = Union[str, pathlib.Path]  # we really have to pick one
PathLike = str
PathOrPaths = Union[PathLike, Sequence[PathLike]]
PythonName = NewType("PythonName", str)

# Layer-related types


def _ensure_str_or_seq_str(path):
    if isinstance(path, Path) or (
        isinstance(path, (list, tuple)) and any([isinstance(p, Path) for p in path])
    ):
        warnings.warn(
            "Npe2 receive a `Path` or a list of `Path`s, instead of `str`,"
            " this will  become an error in the future and is likely a"
            " napari bug. Please fill and issue.",
            UserWarning,
            stacklevel=3,
        )


class ArrayLike(Protocol):
    shape: Tuple[int, ...]
    ndim: int
    dtype: "np.dtype"

    def __array__(self) -> "np.ndarray":
        ...  # pragma: no cover


LayerName = Literal[
    "image", "labels", "points", "shapes", "surface", "tracks", "vectors"
]
Metadata = Dict
DataType = Union[ArrayLike, Sequence[ArrayLike]]
FullLayerData = Tuple[DataType, Metadata, LayerName]
LayerData = Union[Tuple[DataType], Tuple[DataType, Metadata], FullLayerData]

# ########################## CONTRIBUTIONS #################################

# WidgetContribution.command must point to a WidgetCreator
Widget = Union["magicgui.widgets.Widget", "qtpy.QtWidgets.QWidget"]
WidgetCreator = Callable[..., Widget]

# ReaderContribution.command must point to a ReaderGetter
ReaderFunction = Callable[[PathOrPaths], List[LayerData]]
ReaderGetter = Callable[[PathOrPaths], Optional[ReaderFunction]]


# SampleDataGenerator.command must point to a SampleDataCreator
SampleDataCreator = Callable[..., List[LayerData]]

# WriterContribution.command must point to a WriterFunction
# Writers that take at most one layer must provide a SingleWriterFunction command.
# Otherwise, they must provide a MultiWriterFunction.
# where the number of layers they take is defined as
# n = sum(ltc.max() for ltc in WriterContribution.layer_type_constraints())
SingleWriterFunction = Callable[[str, DataType, Metadata], List[str]]
MultiWriterFunction = Callable[[str, List[FullLayerData]], List[str]]
WriterFunction = Union[SingleWriterFunction, MultiWriterFunction]

# ##########################################################################
