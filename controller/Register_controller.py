from schema.Register_schema import RegisterA,Update_Date,Data
from fastapi import HTTPException,Depends,File,UploadFile,Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from model.User_Model import Register_User
from function import change_password





def Register_Create(User_in:RegisterA,db:Session):
    user=db.query(Register_User).filter(Register_User.email==User_in.email).first()
    if user:
        raise HTTPException(status_code=404,detail="not valid user email")
    if len(User_in.password) < 8:
        raise HTTPException(status_code=404,detail="not valid len of a password")
    user_password=change_password.hash(User_in.password)
    user=Register_User(
        name=User_in.name,
        email=User_in.email,
        password=user_password,
        phone=User_in.phone,
        pincode=User_in.pincode,
        gender=User_in.gender,
        state=User_in.state,
        Address=User_in.Address,
        
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_Register_by_id(User_id:int,db:Session):
    user=db.query(Register_User).filter(Register_User.id==User_id).first()
    if not user:
        raise HTTPException (status_code=404,detail="not valid user ")
    return user



def Update_register_user(user_id: int, user_data: Update_Date, db: Session):
    user_update = db.query(Register_User).filter(Register_User.id == user_id).first()
    if not user_update:
        raise HTTPException(status_code=404, detail="not valid user id")

    users_data = user_data.dict(exclude_unset=True)
    for key, value in users_data.items():
        setattr(user_update, key, value)

    db.commit()
    db.refresh(user_update)
    return user_update


def delete_register_user(user_id:int,db:Session):
    user_delete=db.query(Register_User).filter(Register_User.id==user_id).first()
    if not user_delete:
        raise HTTPException(status_code=404,detail="not valid user id")
    db.delete(user_delete) 
    db.commit()
    return user_delete


def auth(db:Session,email:str,password:str):
    users=db.query(Register_User).filter(Register_User.email==email).first()
    if not users:
        return False
    
    very=change_password.verify(password,users.password)
    if not very:
        return False
    return users
from typing import Optional
from datetime import timedelta,datetime
from jose import jwt,JWTError
EXPIRY=24*60
SECRET_KEY="hello"
ALGORITHM="HS256"
from database import get_db
def  Create_token(data:dict,expriy:Optional[timedelta]=None):
    user_data= data.copy()
    if expriy:
        expriy=datetime.utcnow()+expriy
    else:
        expriy=datetime.utcnow()+ timedelta(seconds=EXPIRY)
    user_data.update({"exp":expriy})
    token=jwt.encode(user_data,SECRET_KEY,algorithm=ALGORITHM)
    return token

def get_token(user_data:Data,db:Session=Depends(get_db)):
    user=auth(db,user_data.email,user_data.password)
    if not user:
        raise HTTPException(status_code=404,detail="not valid user email,passowrd")
    users=Create_token(data={"sub":str(user.id)},expriy=timedelta(seconds=EXPIRY))
    return users
    
def valid_token(token:str=Depends(secu),db:Session=Depends(get_db)):
    cer=HTTPException(status_code=400,detail=" not valid details ")
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        user_id=payload.get("sub")
        if user_id is None:
             return cer
    except JWTError:
        return cer
    user_check=db.query(Register_User).filter(Register_User.id==int(user_id)).first()
    if  user_check is None:
        raise HTTPException(status_code=404,detail="not valid user id ")
    return user_check


blacklisted_tokens = set()

def logout(token: str):
    blacklisted_tokens.add(token)
    print("///////////////////////////////////////////////////////",blacklisted_tokens)
    
    return {"message": "Logout successful",
            "token":blacklisted_tokens}
    
    
from model.User_Model import Register_Profile
Max_image=4*1024*1024
Allow_content_type=["image/png","image/jpeg","image/jpg","image/gif"]

async def Create_profile_Register(file:UploadFile=File(...),bio:str=Form(...),discription:str=Form(...),
                            register_id:int=Form(...)
                            ,db:Session=Depends(get_db)):
    register_profile=db.query(Register_Profile).filter(Register_Profile.register_id==register_id).first()
    if    register_profile:
        raise HTTPException(status_code=404,detail="not valid user id  ")
    content= await file.read()
    if not content:
        raise HTTPException(status_code=404,detail="not valid user content ")
    if file.content_type not in Allow_content_type:
        raise HTTPException(status_code=404,detail="not valid user content type")
    if len(content) > Max_image:
        raise HTTPException(status_code=404,detail="not valid user image len")
    profif=Register_Profile(
        bio=bio,
        discription=discription,
        register_id=register_id,
        Allow_content_type=file.content_type,
        image=content,
        file_name=file.filename
    )
    
    db.add(profif)
    db.commit()
    db.refresh(profif)
    return{
        "message": "Image uploaded successfully","filename": profif.file_name,
        "size": len(content),"content_type": profif.Allow_content_type
    }
    
from fastapi.responses import StreamingResponse
import io
def get_prfile_image(profile_id:int,db:Session):
    user=db.query(Register_Profile).filter(Register_Profile.profile_id==profile_id).first()
    if not user :
        raise HTTPException(status_code=404,detail="not valid user profile_id")
    if not user.image:
        raise HTTPException(status_code=404,detail="not valid user")
    return  StreamingResponse(io.BytesIO(user.image),media_type=user.Allow_content_type)


def delete_profile(id:int,db:Session):
    userdelete=db.query(Register_Profile).filter(Register_Profile.profile_id==id).first()
    if  userdelete:
        raise HTTPException(status_code=404,detail="not valid user image ")
    db.delete(userdelete)
    db.commit()
    return{
        "message":"your data delete"
    }