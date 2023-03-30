from typing import Optional
from pydantic import BaseModel, Field, constr
from datetime import date

class Expense(BaseModel):
    id_: str = Field(None, include = False)
    day: Optional[date] = Field(default = date.today(),
                                title = "The day of the transaction")
    amount: constr(regex=r'-?^\d+(?:\.\d{1,2})?$') = Field(title = "The amount spent (as a string)",
                                                           description = ">0 when income, <0 when expense.",
                                                           example = "-20.5")
    category: Field(title = "Category of the transaction",
                    example = "Food",
                    description = "For a full list see /get_categories")
    description: Optional[str] = Field(default = "",
                                       title = "Details of the transaction",
                                       example = "FastAPI Course")
    
    class Config:
        schema_extra = {
            "example": {
                "day": "2023-03-25",
                "amount": "20",
                "category": "Food",
                "description": ""
            }
        }

class ExpenseOptional(Expense):
    __annotations__ = {k: Optional[v] for k, v in Expense.__annotations__.items()}
    