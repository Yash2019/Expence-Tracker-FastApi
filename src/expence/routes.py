from fastapi import APIRouter, status, HTTPException, Depends
from uuid import UUID
from src.expence.schemas import ExpenceUpdate
from src.db.main import get_db
from sqlalchemy.orm import Session
from src.expence.schemas import ExpenceRead, ExpenceCreate
from src.expence.service import ExpenceService
from src.auth.dependencies import get_current_user
from src.auth.models import User

expence_router = APIRouter()
expence_service = ExpenceService()

@expence_router.get('/', response_model=list[ExpenceRead])
def get_all_expenses(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return expence_service.get_all_expenses(db, current_user)

@expence_router.post('/', response_model=ExpenceRead)
def create_expense(task: ExpenceCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    return expence_service.create_expense(db, task, current_user)

@expence_router.get('/{expense_uuid}', response_model=ExpenceRead)
def get_one_expense(expense_uuid: UUID,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    expense = expence_service.get_expense(db, expense_uuid, current_user)
    if not expense:
        raise HTTPException(status_code=404)
    return expense

@expence_router.patch('/{expence_uuid}', response_model=ExpenceRead)
def update_expense(expence_uuid: UUID, task: ExpenceUpdate, db: Session = Depends(get_db),
                   current_user:User = Depends(get_current_user)):
    expence = expence_service.update_expense(db, expence_uuid, task, current_user)
    if not expence:
        raise HTTPException(status_code=404)
    return expence

@expence_router.delete("/{expense_uuid}")
def delete_expense(
    expense_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not expence_service.delete_expense(db, expense_uuid, current_user):
        raise HTTPException(status_code=404)
    return {"detail": "deleted"}
