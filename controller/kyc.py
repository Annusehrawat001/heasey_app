from fastapi import APIRouter,HTTPException,File,UploadFile,Form,Depends
router=APIRouter()
from sqlalchemy.orm import Session
from model.kyc import KYC,KYC_ID_PROOF,Bank_detail
from schema.kyc import KYC_schema,Bank_kyc_schema
from model.User_Model import Register_User
from database import get_db


def create_kyc(kyc_in:KYC_schema,db:Session): 
    user=db.query(Register_User).filter(Register_User.id==kyc_in.register_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="not valid user register id :")
    
    user_kyc=db.query(KYC).filter(KYC.email==kyc_in.email).first()
    if user_kyc:
        raise HTTPException(status_code=404,detail="not valid ")
   
    user_kyc=KYC(
        name=kyc_in.name,
        email=kyc_in.email,
        pincode=kyc_in.pincode,
        phone=kyc_in.phone,
        register_id=kyc_in.register_id
    )
    db.add(user_kyc)
    db.commit()
    db.refresh(user_kyc)
    return user_kyc

def delete_kyc(kyc_id:int,db:Session):
      # 1️⃣ Check KYC
    user_kyc=db.query(KYC).filter(KYC.kyc_id==kyc_id).first()
    if not user_kyc:
        raise HTTPException(status_code=404,detail="not valid ")
      # 1️⃣ Delete KYC
    db.delete(user_kyc)
    db.commit()
    return {
        "message":"Your data is delete"
    }




Max_image = 4 * 1024 * 1024
Allow_content_type = ["image/png", "image/jpeg", "image/jpg", "image/gif"]

async def creat_kyc_id_proof(
    kyc_id: int,
    file: UploadFile,
    db: Session
)
    user_kyc = db.query(KYC).filter(KYC.kyc_id == kyc_id).first()
    if  not user_kyc:
        raise HTTPException(status_code=404, detail="Invalid kyc_id")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    if file.content_type not in Allow_content_type:
        raise HTTPException(status_code=400, detail="Invalid image type")

    if len(content) > Max_image:
        raise HTTPException(status_code=400, detail="Image size exceeds limit")

    proof = KYC_ID_PROOF(
        file_name=file.filename,
        Allow_content_type=file.content_type,
        image=content,
        kyc_id=kyc_id
    )
  
    db.add(proof)
    db.commit()
    db.refresh(proof)

    return {"message": "KYC ID proof uploaded successfully"}





def create_banK_details(bank_in:Bank_kyc_schema,db:Session):
    
    banK_user=db.query(Bank_detail).filter(Bank_detail.account_number==bank_in.account_number).first()
    if banK_user:
        raise HTTPException(status_code=404,detail="not valid user account number")
   
    banK_user=Bank_detail(
        account_number=bank_in.account_number,
        account_holder_name= bank_in.account_holder_name,
        bank_name=bank_in.bank_name,
        branch_name=bank_in.branch_name,
        kyc_id=bank_in.kyc_id
        
    )
    db.add(banK_user)
    db.commit()
    db.refresh(banK_user)
    return banK_user

