

from fastapi import HTTPException
from sqlalchemy.orm import Session
from model.manufacfurer import Manufacturer
from controller.manufacture import Hash_password,verify_password
import random
from model.otp_manufacturer import OtpManufacturer
from schema.otp_manufacturer import ManufacturerForget_password,ManufacturerReset_password,OtpAManufacturer


####################################################################################################

def OtpCreate():
    otp=random.randint(1000,9999)
    return otp

#########################################################################################
# -----------Manufacturer---------SendOtp----------1
# #############################################################
def sendotp_manufacturer(data:OtpAManufacturer,db:Session):
    otp=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if not otp:
        raise HTTPException(status_code=400,detail="not valid user email _manufacturer")
    generated_otp=random.randint(1000,9999)
    new_otp=OtpManufacturer(
        email=data.email,
        otps=generated_otp
    )
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return {"message": "OTP sent successfully", "otp": generated_otp}
##################################################################################
# -----------Manufacturer -----------Forget_password----------------2
# ####################################################################

def forgot_password_manufacturer(data:ManufacturerForget_password,db:Session):
    lostPasswordmanufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if not lostPasswordmanufacturer:
        raise HTTPException(status_code=400,detail="NOt valid user eamil")
    if len(data.new_password) < 8:
        raise HTTPException(status_code=400,detail="not valid password lenght")
    otp_check=db.query(OtpManufacturer).filter(OtpManufacturer.otps==data.otps).first()
    if otp_check:
        db.delete(otp_check)
        db.commit()
    if not otp_check:
        raise HTTPException(status_code=404,detail="not valid opt ")
    lostPasswordmanufacturer.password= Hash_password(data.new_password)
    db.add(lostPasswordmanufacturer)
    db.commit()
    db.refresh(lostPasswordmanufacturer)

    return lostPasswordmanufacturer
###########################################################################################
#------------- Manufacturer----------------Reset_password--------------3
# ############################################################



def reset_password_manufacturer(data:ManufacturerReset_password,db:Session):
    manufacturer_reset_password = db.query(Manufacturer).filter(Manufacturer.email == data.email).first()
    if not manufacturer_reset_password:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.old_password,manufacturer_reset_password.password):
        raise HTTPException(status_code=400,detail="not valid user old password")
    if len(data.new_password) < 8:
        raise HTTPException(status_code=400,detail="not valid user new password lenght .")
    otp_check=db.query(OtpManufacturer).filter(OtpManufacturer.otps==data.otps).first()
    if otp_check:
        db.delete(otp_check)
        db.commit()
    if not otp_check:
        raise HTTPException(status_code=404,detail="not valid opt ")
    manufacturer_reset_password.password=Hash_password(data.new_password)
    db.add(manufacturer_reset_password)
    db.commit()
    db.refresh(manufacturer_reset_password)
    return manufacturer_reset_password


