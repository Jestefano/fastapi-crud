from typing import Optional
from pydantic import BaseModel, constr, Field
from datetime import date
from app.enums import TypeEnum

# class Category(BaseModel):
#     id_: Optional[str] = Field(default = None, primary_key = True)
#     name: TypeEnum = Field(title = "Name of the category", example = "Food")

#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Food"
#             }
#         }

class Expense(BaseModel):
    id_: Optional[str] = Field(default = None)
    day: date = Field(default = date.today(),
                     title = "The day of the transaction")
    amount: constr(regex=r'-?^\d+(?:\.\d{1,2})?$') = Field(title = "The amount spent (as a string)",
                                                           description = ">0 when income, <0 when expense.",
                                                           example = "-20.5")
    category: str = Field(title = "Category of the transaction",
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
