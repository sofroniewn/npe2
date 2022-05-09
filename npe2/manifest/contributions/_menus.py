from collections import namedtuple
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from ..utils import Executable

Menu = namedtuple("Menu", "key description order")

# a list of valid napari menu locations that plugins can contribute too.
# keys provided in the plugin manifest must match these strings
NAPARI_MENUS = {
    Menu("/napari/layer_context", "Process Layer", 0),
    Menu("/napari/layer_context/projections", "Make Projection", 0),
    Menu("/napari/layer_context/convert_type", "Convert datatype", 0),
    Menu("/napari/tools/acquisition", "Acquisition", 0),
    Menu("/napari/tools/transform", "Transform", 1),
    Menu("/napari/tools/filter", "Filter", 2),
    Menu("/napari/tools/segmentation", "Segmentation", 3),
    Menu("/napari/tools/measurement", "Measurement", 4),
    Menu("/napari/tools/classification", "Classification", 5),
    Menu("/napari/tools/visualization", "Visualization", 6),
    Menu("/napari/tools/utilities", "Utilities", 7),
}


# user provides this
class _MenuItem(BaseModel):
    when: Optional[str] = Field(
        description="Condition which must be true to show this item"
    )
    group: Optional[str] = Field(description="Group into which this item belongs")


class Submenu(_MenuItem):
    submenu: str = Field(
        ...,
        description="Identifier of the submenu to display in this item."
        "The submenu must be declared in the 'submenus' -section",
    )
    # if submenu doesn't exist, you get:
    # Menu item references a submenu ...` which is not defined in the 'submenus' section


class MenuCommand(_MenuItem, Executable):
    command: str = Field(
        ...,
        description="Identifier of the command to execute. "
        "The command must be declared in the 'commands' section",
    )
    # if command doesn't exist, you get:
    # "Menu item references a command `...` which is not defined in the
    # 'commands' section."
    alt: Optional[str] = Field(
        description="Identifier of an alternative command to execute. "
        "It will be shown and invoked when pressing Alt while opening a menu."
        "The command must be declared in the 'commands' section"
    )
    # if command doesn't exist, you get:
    # "Menu item references an alt-command  `...` which is not defined in
    # the 'commands' section."


MenuItem = Union[MenuCommand, Submenu]


MenuContribution = Dict[str, List[MenuItem]]
