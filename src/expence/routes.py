from fastapi import APIRouter, status, HTTPException, Depends

from src.expence.schemas import ExpenceUpdate
from src.db.main import get_db
from sqlalchemy.orm import Session
from src.expence.schemas import ExpenceRead, ExpenceCreate
from src.expence.service import ExpenceService
expence_router = APIRouter()
expence_service = ExpenceService()

@expence_router.get('/', response_model=ExpenceRead)
async def get_all_expenses(db:Session = Depends(get_db)):
    all_expence = expence_service.get_expense(db)
    return all_expence

@expence_router.post('/', response_model=ExpenceRead)
async def create_expense(task: ExpenceCreate, db: Session = Depends(get_db)):
    create = expence_service.create_expense(db, task)
    return create

@expence_router.get('/{expence_uuid}', response_model=ExpenceRead)
async def get_one_expense(expence_uuid: str, db:Session = Depends(get_db)):
    get_expence = expence_service.get_expense(db, expence_uuid)
    if get_expence:
        return get_expence
    else:
        raise HTTPException(status_code=404)

@expence_router.patch('/{expence_uuid}', response_model=ExpenceRead)
async def update_expense(task: ExpenceUpdate, expence_uuid: str, db: Session = Depends(get_db)):
    update = expence_service.update_expense(expence_uuid, db, task)
    if update:
        return update
    raise HTTPException(status_code=404)

@expence_router.delete('/{expence_uuid}')
async def delete_expense(expence_uuid: str, db: Session = Depends(get_db)):
    delete = expence_service.delete_expense(expence_uuid, db)
    if delete:
        return delete
    raise  HTTPException(status_code=404)

