from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from src.expence.schemas import ExpenceCreate, ExpenceRead, ExpenceUpdate
from src.db.model import  Expense
from sqlalchemy import select
from src.auth.models import User
from uuid import UUID
app = FastAPI()

class ExpenceService:
    def get_all_expenses(self, db: Session, user: User):
        stmt = select(Expense).where(
            Expense.user_id == user.uuid
        )
        return db.execute(stmt).scalars().all()


    def get_expense(self, db: Session, expense_uuid: UUID, user: User):
        stmt = select(Expense).where(
            Expense.uuid == expense_uuid,
            Expense.user_id == user.uuid
        )
        return db.execute(stmt).scalars().first()

    def create_expense(self, db: Session, task: ExpenceCreate, user: User):
        new_expence = Expense(
            amount=task.amount,
            category=task.category,
            description=task.description,
            expense_date=task.expense_date,
            user_id=user.uuid
        )
        db.add(new_expence)
        db.commit()
        db.refresh(new_expence)
        return new_expence

    def update_expense(self, db: Session, expense_uuid: UUID, task: ExpenceUpdate, user: User):
        expense = self.get_expense(db, expense_uuid, user)
        if not expense:
            return None

        if task.amount is not None:
            expense.amount = task.amount
        if task.category is not None:
            expense.category = task.category
        if task.description is not None:
            expense.description = task.description
        if task.expense_date is not None:
            expense.expense_date = task.expense_date

        db.commit()
        db.refresh(expense)
        return expense

    def delete_expense(self, db: Session, expense_uuid: UUID, user: User):
        expense = self.get_expense(db , expense_uuid, user)
        if not expense:
            return False

        db.delete(expense)
        db.commit()
        return True