from model.review_model import Review
from model.Product_model import Product
from model.User_Model import Register_User
from model.order_model import Order

from schema.review_schema import ReviewA

from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session

def create_review(data:ReviewA,db:Session):
    user_data=db.query(Register_User).filter(Register_User.id==data.register_id).first()
    if not user_data:
        raise HTTPException(status_code=404,detail="not valid register id")
    user_data=db.query(Product).filter(Product.Product_id==data.product_id).first()
    if not user_data:
        raise HTTPException(status_code=404,detail="not valid product_id")
    user_data=db.query(Order).filter(Order.order_id==data.order_id).first()
    if not user_data:
        raise HTTPException(status_code=404,detail="not valid user order id ")
    user_data=Review(
        register_id=data.register_id,
        product_id=data.product_id,
        order_id=data.order_id,
        rating=data.rating,
        comment=data.comment
        
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data
    
