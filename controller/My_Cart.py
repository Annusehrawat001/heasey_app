
from sqlalchemy.orm import Session
from fastapi import APIRouter , Depends,HTTPException
from schema.My_cart_schema import MY_CART_MY
from model.Product_model import Product
from model.User_Model import Register_User
from model.MY_cart_model import MY_CART


# def my_cart_add_priduct(my_cart_in:MY_CART_MY,
#                         db:Session):
#     user_my_carts=db.query(Product).filter(Product.Product_id==my_cart_in.product_id).first()
#     if not user_my_carts:
#         raise HTTPException(status_code=404,detail="not valid user_id")
#     user_my_cart=db.query(Register_User).filter(Register_User.id==my_cart_in.register_id).first()
#     if not user_my_cart:
#         raise HTTPException(status_code=404,detail="not valid product")
#     if my_cart_in.stock_quantity > user_my_carts.Stock_quantity:
#         raise HTTPException(status_code=404,detail="not valid product")
#     user_my_cart=MY_CART(
#         stock_quantity=my_cart_in.stock_quantity,
#         price=my_cart_in.price,
#         product_id=my_cart_in.product_id,
#         register_id=my_cart_in.register_id
        
#     )
#     db.add(user_my_cart)
#     db.commit()
#     db.refresh(user_my_cart)
#     return user_my_cart

from fastapi import HTTPException
from sqlalchemy.orm import Session

def my_cart_add_product(cart_in: MY_CART_MY, db: Session):

    # 1️⃣ Check product
    product = db.query(Product).filter( Product.Product_id == cart_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2️⃣ Check user
    user = db.query(Register_User).filter( Register_User.id == cart_in.register_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3️⃣ Stock check
    if cart_in.stock_quantity > product.Stock_quantity:
        raise HTTPException( status_code=400,detail="Not enough stock available")

    # 4️⃣ Check if product already in cart
    cart_item = db.query(MY_CART).filter( MY_CART.product_id == cart_in.product_id, MY_CART.register_id == cart_in.register_id).first()
    if cart_item:
        # update quantity
        cart_item.stock_quantity += cart_in.stock_quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item

    # 5️⃣ Create new cart item
    new_cart = MY_CART(
        product_id=product.Product_id,
        register_id=user.id,
        stock_quantity=cart_in.stock_quantity,
        price=product.selling_price   # ✅ price from product table
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return new_cart



def get_all(db:Session):
    get_my_cart_all=db.query(MY_CART).all()
    if not get_my_cart_all:
        raise HTTPException(status_code=404,detail="not any my cart")
    return get_my_cart_all

def get_my_cart_by_id(id:int,db:Session):
    MyCartById=db.query(MY_CART).filter(MY_CART.my_cart_id==id).first()
    if not MyCartById:
        raise HTTPException(status_code=404,detail="not valid mycart_id")
    return MyCartById


def delete_mycart(id:int,db:Session):
    MyCartDelete=db.query(MY_CART).filter(MY_CART.my_cart_id==id).first()
    if not MyCartDelete:
        raise HTTPException(status_code=404,detail="not valid user mycare id")
    db.delete(MyCartDelete)
    db.commit()
    return{
        "message":"Your data delete"
    }