from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import datetime

class Todo(BaseModel):
    title : str
    description: Optional[str] | None = None
    date_created : str = str(datetime.datetime.now())