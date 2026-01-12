from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends
from schema.order_schema import OrderA
from model.User_Model import Register_User
from model.MY_cart_model import MY_CART
from model.Product_model import Product
from model.order_model import Order
from sqlalchemy.exc import SQLAlchemyError



from sqlalchemy.exc import SQLAlchemyError

def order_create(order_in: OrderA, db: Session):

    try:
      
        user = db.query(Register_User).filter(Register_User.id == order_in.register_id ).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found register id")
     
        cart_items = db.query(MY_CART).filter( MY_CART.register_id == order_in.register_id).all()
        if not cart_items:
            raise HTTPException( status_code=400,detail="Cart is empty")
        total_price = 0
     
        for item in cart_items:
            product = db.query(Product).filter(   Product.Product_id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404,detail="Product not found")
            if item.stock_quantity > product.Stock_quantity:
                raise HTTPException(  status_code=400,  detail=f"Not enough stock for {product.Product_name}")
            total_price += item.stock_quantity * product.selling_price
      
        new_order = Order(
            register_id=user.id,
            total_price=total_price,
            payment_method=order_in.payment_method,
            stock_quantity=item.stock_quantity,
            product_id=product.Product_id
            )
        db.add(new_order)
        db.flush()   
        product.Stock_quantity -= item.stock_quantity
     
        db.query(MY_CART).filter(MY_CART.register_id == user.id).delete()
        db.commit()
        db.refresh(new_order)

        return new_order

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500,detail="Order creation failed" )




def get_all_order(db:Session):
      
    user=db.query(Order).all()
    if  not user:
        raise HTTPException(status_code=404,detail="not user have any order ")
    return user


def delete_order(order_id: int, db: Session):
  
    orders = db.query(Order).filter(Order.order_id == order_id).first()

    if not orders:
        raise HTTPException(status_code=404, detail="Invalid order id")

    product=db.query(Product).filter(Product.Product_id==orders.product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="not valid product id")
 
    product.Stock_quantity += orders.stock_quantity

    db.delete(orders)
    db.commit()

    return {
        "message": "Order cancelled successfully, stock restored"
    }



def get_id(id:int,db:Session):
\
    user_order=db.query(Order).filter(Order.order_id==id).first()
    if not user_order:
        raise HTTPException(status_code=404,detail="not valid user order")
    return user_order

  
      
      
      
      
      