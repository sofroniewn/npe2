from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from ._commands import CommandContribution
from ._menus import MenuItem
from ._readers import ReaderContribution
from ._sample_data import SampleDataContribution
from ._submenu import SubmenuContribution
from ._themes import ThemeContribution
from ._widgets import WidgetContribution
from ._writers import WriterContribution


class ContributionPoints(BaseModel):
    commands: Optional[List[CommandContribution]]
    readers: Optional[List[ReaderContribution]]
    writers: Optional[List[WriterContribution]]
    widgets: Optional[List[WidgetContribution]]
    sample_data: Optional[List[SampleDataContribution]]
    themes: Optional[List[ThemeContribution]]

    # We use a dict for menus to allow for keys with `/`
    menus: Optional[Dict[str, List[MenuItem]]] = Field(None, hide_docs=True)
    submenus: Optional[List[SubmenuContribution]] = Field(None, hide_docs=True)

    # configuration: Optional[JsonSchemaObject]
    # keybindings: Optional[List[KeyBindingContribution]]

    class Config:
        docs_exclude = {"menus", "submenus"}
