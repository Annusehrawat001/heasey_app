from schema.category_schema import CategoryA
from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.category_model import Category




def category_create(category_in:CategoryA,db:Session):
  
    categorys=db.query(Category).filter(Category.category_name==category_in.category_name).first()
    if categorys:
        raise HTTPException(status_code=400,detail="not valid category already created")
    categorys=Category(
        category_name=category_in.category_name,
        description=category_in.description,
        brand=category_in.brand
    )
    db.add(categorys)
    db.commit()
    db.refresh(categorys)
    return categorys


def get_all(db:Session):
     
    user=db.query(Category).all()
    if not user:
        raise HTTPException(status_code=404,detail="not valid ")
    return

def delete_category(id:int,db:Session):
    user_delete=db.query(Category).filter(Category.category_id==id).first()
    if not user_delete:
        raise HTTPException(status_code=404,detail="category id not valid")

    db.delete(user_delete)
    db.commit()
   
    return user_delete


def category_id(id:int,db:Session):
    user_category=db.query(Category).filter(Category.category_id==id).first()
    if not user_category:
        raise HTTPException(status_code=404,detail="not valid category")
    return user_category

