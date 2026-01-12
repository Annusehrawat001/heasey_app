
from datetime import timedelta,datetime
from jose import jwt,JWTError

from schema.manufacturer_schema import ManufacturerA,LoginAManufacturer,responemanufacturer
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from database import get_db 
secu=OAuth2PasswordBearer(tokenUrl="/login")
from fastapi.responses import StreamingResponse
import io
from model.manufacfurer import Manufacturer,ProfileManufacturer

#  for image 
Max_image=4*1024*1024
Allow_content_type=["image/png","image/jpeg","image/jpg","image/gif"]
from fastapi import HTTPException,Depends,File,UploadFile,Form
from sqlalchemy.orm import Session



from passlib.context import CryptContext
####################################################################################################
Hashed_password=CryptContext(schemes= ["argon2", "bcrypt"],
    deprecated="auto"
)
       

def Hash_password(simple_password:str):
    return Hashed_password.hash(simple_password)

def verify_password(simple_password:str,new_password:str):
    return Hashed_password.verify (simple_password,new_password)
####################################################################################################
# Create_manufacturer---------------------1
####################################################################################################
def manufacturer_user_controller(register_in: ManufacturerA, db: Session):
      # 1️⃣ Check Manufacturer 
    user = db.query(Manufacturer).filter(Manufacturer.email == register_in.email).first()
    
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")
       # 1️⃣ Check Manufacturer Lenght
    if len(register_in.password) < 8:
        raise HTTPException( status_code=400, detail="Password must be at least 8 characters long" )
      # 1️⃣ Create Password Hash
    hashed_pass = Hashed_password.hash(register_in.password)
    #   # 1️⃣ add Details
    new_user = Manufacturer(
        Manufacturer_Name=register_in.Manufacturer_Name,
        email=register_in.email,
        password=hashed_pass,
        address=register_in.address,
        phone=register_in.phone,
        pin_code=register_in.pin_code,
        city=register_in.city,
        state=register_in.state,
        gender=register_in.gender
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

###################################################
# manufacturer get all--------------2
# #################################################
def get_all_manufacturer_controller(db: Session):
      # 1️⃣ Check Manufacturer 
    users = db.query(Manufacturer).all()

    if not users:
        raise HTTPException(status_code=400, detail="No users found")

    return users
####################################################
# get by id Manufacturer------------------3
# ################################################


def get_manufacturer_by_id_controller(id: int, db: Session):
      # 1️⃣ Check Manufacturer
    user = db.query(Manufacturer).filter(Manufacturer.id == id).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    return user
#####################################################
# Manufacturer------------4
# ###############################################


def update_manufacturer_controller(id: int, data, db: Session):
    # Check if user exists
    user = db.query(Manufacturer).filter(Manufacturer.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not valid user id for update")

    # Convert only provided fields
    update_data = data.dict(exclude_unset=True)

    # Apply updates
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user
#######################################################
# Manufacturer---------5
# #############################################

def delete_manufacturer_controller(id: int, db: Session):
        # Check if Manufacturer  exists
    user = db.query(Manufacturer).filter(Manufacturer.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid user ID")

    db.delete(user)
    db.commit()

    return user
####################################################################################################
# creat login-------------------6
####################################################################################################
def author(email:str,password:str,db:Session):
    user=db.query(Manufacturer).filter(Manufacturer.email==email).first()
    if not user:
        return False
 
    very=Hashed_password.verify(password,user.password) 
    if not very:
        return False
    return user

def create_token(data:dict,expiry:timedelta=None):
    user_data=data.copy()
    if expiry:
        expiry_time=datetime.utcnow()+expiry
    else:
        expiry_time =datetime.utcnow()+timedelta(minutes=EXPIRY)
        
        
    user_data.update({"exp":expiry_time})
    token=jwt.encode(user_data,secrate_key,algorithm=ALGORITHAM)
    return token

def get_token(user_data:LoginAManufacturer,db:Session):
    user_get=author(user_data.email,user_data.password,db)
    if not user_get:
        raise HTTPException (status_code=404,detail="email or password not match")
    usertoken=create_token(data={"sub":str(user_get.id)},expiry=timedelta(minutes=EXPIRY))
    return usertoken

    
def token_chenk(token:str=Depends(secu),db:Session=Depends(get_db)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    cer=HTTPException(status_code=400,detail=" not valid details ")
    try:
        payload=jwt.decode(token,secrate_key,algorithms=ALGORITHAM)
        user_id=payload.get("sub")
        if user_id is None:
             return cer
    except JWTError:
        return cer
    user=db.query(Manufacturer).filter(Manufacturer.id==int(user_id)).first()
    if user is None:
        return cer
    return user
#############################################
# Manufacturer --------------createProfile-----------7
# #######################################################

async def post_user_image(files: UploadFile = File(...),bio:str=Form(...),manufacturer_id: int = Form(...),description: str = Form(...),db: Session = Depends(get_db)):
    existing_user = db.query(ProfileManufacturer).filter(ProfileManufacturer.manufacturer_id == manufacturer_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User ID already exists")
    content = await files.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    
    if files.content_type not in Allow_content_type:
        raise HTTPException(status_code=400, detail="Invalid files type")
    
    if len(content) > Max_image:
        raise HTTPException(status_code=400, detail="File size exceeds 4MB limit")

    new_user = ProfileManufacturer(
        manufacturer_id=manufacturer_id,
        bio=bio,
        description=description,
        image=content,
        image_content_type=files.content_type,
        file_name=files.filename,
      
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Image uploaded successfully","id": new_user.id,"filename": new_user.file_name,
        "size": len(content),"content_type": new_user.image_content_type
    }

    



####################################################
# -------------------- Get ProfileManufacturer Image --------------------8
# ################################################
def get_profile_image(manufacturer_id: int, db: Session):
        # Check if Profile exists
    user = db.query(ProfileManufacturer).filter(ProfileManufacturer.manufacturer_id==manufacturer_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        # Check if profile image exists
    if not user.image:
        raise HTTPException(status_code=404, detail="Image not found")

    return StreamingResponse(io.BytesIO(user.image), media_type=user.image_content_type)


###############################################
# Manufacturer -----------Delete-------------9
# #####################################################
def delete_profile(id:int,db:Session):
        # Check if userPriles exists
    delete_customer_prfile=db.query(ProfileManufacturer).filter(ProfileManufacturer.id==id).first()
    if not delete_customer_prfile:
        raise HTTPException(status_code=404,detail="not valid user prodile id")
    db.delete(delete_customer_prfile)
    db.commit()
    return {
        "message":"User profile delete"
    }





blacklisted_tokens = set()

def logout_manufacturer(token: str):
    blacklisted_tokens.add(token)
    print("///////////////////////////////////////////////////////",blacklisted_tokens)
    
    return {"message": "Logout successful",
            "token":blacklisted_tokens}
    
    