from fastapi import FastAPI
app=FastAPI()
from database import Base,engine
from model.Otp_model import OTP
from model.User_Model import Register_User
from model.category_model import Category
from model.Product_model import Product
from model.manufacfurer import Manufacturer,ProfileManufacturer
from model.kyc import KYC
from model.MY_cart_model import MY_CART
from model.order_model import Order
from model.review_model import Review
from model.wishlist_model import Wishlist


Base.metadata.create_all(bind=engine)

from router.Register_router import router as Register_router
from router.Otp_router import router as Otp_router
from router.category_router import router as category_router
from router.Product_router import router as product_router
from router.manufacturer_router import router as manufcturer_router
from router.kyc import router as kyc_router
from router.My_cart_router import router as Mycart_router
from router.order_router import router as order_router
from router.review_router import router as review_router
from router.wishlist_router import router as wishlist_router


app.include_router(Register_router)
app.include_router(Otp_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(manufcturer_router)
app.include_router(kyc_router)
app.include_router(Mycart_router)
app.include_router(order_router)
app.include_router(review_router)
app.include_router(wishlist_router)


