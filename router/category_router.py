from fastapi import APIRouter,Depends
from sqlalchemy.orm  import  Session
router=APIRouter()
from database import get_db
from schema.category_schema import CategoryA
from controller.category_controller import category_create,get_all,delete_category,category_id

@router.post("/category")
def create_category(data:CategoryA,db:Session=Depends(get_db)):
    return category_create(data,db)

@router.get("/get")
def get_all_category(db:Session=Depends(get_db)):
    return  get_all(db)

@router.delete("/delete")
def get_category(id:int,db:Session=Depends(get_db)):
    return delete_category(id,db)

@router.get("/get_id")
def get_category(id:int,db:Session=Depends(get_db)):
    return category_id(id,db)
