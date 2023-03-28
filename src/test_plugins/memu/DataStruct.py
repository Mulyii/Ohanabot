from typing import Dict, Any, Union
from pydantic import BaseModel


class Plugin_Menu_item(BaseModel):
    name: str
    description: str
    usage: str
    extra: Union[Dict[Any, Any], None] = None
