from fastapi import APIRouter,HTTPException
router=APIRouter()
from sqlalchemy.orm import Session
from model.wishlist_model import Wishlist
from model.User_Model import Register_User
from model.Product_model  import Product

def  create_wishlist(data_in:Wishlist,db:Session):
    user=db.query(Register_User).filter(Register_User.id==data_in.register_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="register_user id not valid")
    user=db.query(Product).filter(Product.Product_id==data_in.product_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="not valid product_id")
    user=Wishlist(
        product_id=data_in.product_id,
        register_id=data_in.register_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_items(db:Session):
    user=db.query(Wishlist).all()
    if not user:
        raise HTTPException(status_code=404,detail="not valid ")
    return user

def delete_wishlist_item(id:int,db:Session):
    users_wishlist=db.query(Wishlist).filter(Wishlist.id==id).first()
    if not users_wishlist:
        raise HTTPException(status_code=404,detail="not valid wishlist id")
    db.delete(users_wishlist)
    db.commit()
    return {
        "message":"your data delete"
    }