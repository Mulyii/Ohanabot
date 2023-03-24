from typing import Dict, Any, Union
from pydantic import BaseModel


class Plugin_Memu_item(BaseModel):
    name: str
    description: str
    usage: str
    extra: Union[Dict[Any, Any], None] = None
