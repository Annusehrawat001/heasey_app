from model.User_Model import Register_User
from fastapi import HTTPException
import random
from sqlalchemy.orm import Session
from schema.Otp_schema import OtpA,ForgetA,Reset_password
from model.Otp_model import OTP
from function import hash_password,verfiy_password

def OtpCreate():
    return(random.randint(1000,9999))


def Send_Otp(data:OtpA,db:Session):
    user_otp=db.query(Register_User).filter(Register_User.email==data.email).first()
    if not user_otp:
        raise HTTPException(status_code=404,detail="Not valid user email")
    otp_generate=random.randint(1000,9999)
    user_otp=OTP(
        email=data.email,
        otps=otp_generate
    )
    db.add(user_otp)
    db.commit()
    db.refresh(user_otp)
    return user_otp




def forgot_password(data:ForgetA,db:Session):
    lost_password=db.query(Register_User).filter(Register_User.email==data.email).first()
    if not lost_password:
        raise HTTPException(status_code=400,detail="NOt valid user eamil")
    if len(data.password) < 8:
        raise HTTPException(status_code=400,detail="not valid password lenght")
    otp_check=db.query(OTP).filter(OTP.otps==data.otps).first()
    if otp_check:
        db.delete(otp_check)
        db.commit()
        
    if not otp_check:
        raise HTTPException(status_code=404,detail="not valid otp ")
    lost_password.password=hash_password(data.password)
    
    db.add(lost_password)
    db.commit()
    db.refresh(lost_password)

    return lost_password


def reset_password(data:Reset_password,db:Session):
    user_reset = db.query(Register_User).filter(Register_User.email == data.email).first()
    if not user_reset:
        raise HTTPException(status_code=404, detail="User not found")
    if not verfiy_password(data.old_password,user_reset.password):
        raise HTTPException(status_code=400,detail="not valid user old password")
    if len(data.new_password) < 8:
        raise HTTPException(status_code=400,detail="not valid user new password lenght .")
    otp_check=db.query(OTP).filter(OTP.otps==data.otps).first()
    if otp_check:
        db.delete(otp_check)
        db.commit()
    if not otp_check:
        raise HTTPException(status_code=404,detail="not valid otp ")
    user_reset.password=hash_password(data.new_password)
    db.add(user_reset)
    db.commit()
    db.refresh(user_reset)
    return user_reset











# def forget_password(data:ForgetA,db:Session):
#     user_forget=db.query(Register_User).filter(Register_User.email==data.email).first()
#     if not user_forget:
#         raise HTTPException(status_code=404,detail="not valid user email")
#     if len(data.password)<8:
#         raise HTTPException(status_code=404,detail="not valid password len")
#     otp=db.query(OTP).filter(OTP.otps==data.otps).first()
#     if not otp:
#         raise HTTPException(status_code=404,detail="not valid  user otp")
#     user_forget.password==hash_password(data.password)
#     if otp:
#         db.delete(otp)
#         db.commit()
   
#     return otp
    

# def Reast_password(data:Reset_password,db:Session):
#     user=db.query(Register_User).filter(Register_User.email==data.email).first()
#     if not user:
#         raise HTTPException(status_code=404,detail="not valid user email")
