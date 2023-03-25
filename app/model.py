from typing import Optional, Literal
from pydantic import BaseModel
from datetime import date
from uuid import uuid4

class Expense(BaseModel):
    id_: Optional[str] = uuid4().hex
    day: Optional[date] = date.today()
    amount: float
    category: Literal["Food", "Education", "Home", "Others"]
    description: Optional[str] = ""

class ExpenseOptional(Expense):
    __annotations__ = {k: Optional[v] for k, v in Expense.__annotations__.items()}