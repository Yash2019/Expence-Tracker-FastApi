from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from src.expence.schemas import ExpenceCreate, ExpenceRead, ExpenceUpdate
from src.db.model import  Expense
from sqlalchemy import select
app = FastAPI()

class ExpenceService:

    async def all_expense(self, db:Session):
        statement = select(Expense)
        result = db.execute(statement)
        return result.scalar().all()

    async def create_expense(self, db:Session, task: ExpenceCreate):
        new_expence = Expense(
            amount= task.amount,
            category=task.category,
            description=task.description,
            expense_date=task.expence_date
        )
        db.add(new_expence)
        db.commit()
        db.refresh(new_expence)
        return new_expence

    async def get_expense(self, db:Session, expence_uuid: str):
        statement = select(Expense).where(Expense.uuid == expence_uuid)
        result = db.execute(statement)
        return result.first()

    async def update_expense(self, expence_uuid: str, db:Session, task: ExpenceUpdate):
        expence= await self.get_expense(db ,expence_uuid)

        if not expence:
            raise HTTPException(status_code=404)

        if task.amount is not None:
            expence.amount = task.amount

        if task.category is not None:
            expence.category = task.category

        if task.description is not None:
            expence.description = task.description

        if task.expence_date is not None:
            expence.expence_data = task.expence_date

        db.commit()
        db.refresh(expence)
        return expence

    async def delete_expense(self, expence_uuid: str, db: Session):
        del_expence = self.get_expense(db, expence_uuid)

        if del_expence is not None:
            db.delete(del_expence)

            db.commit()
            return {}
        return None

