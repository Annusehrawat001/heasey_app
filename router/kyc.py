
from fastapi import APIRouter,Depends,File,UploadFile,Form
from sqlalchemy.orm  import  Session
router=APIRouter()
from database import get_db
from schema.kyc import KYC_schema,Bank_kyc_schema
from controller.Kyc import create_kyc,delete_kyc,creat_kyc_id_proof,create_banK_details

####################################################################################################
####################################################################################################
@router.post("/postkyc")
def post_kyc(kyc_in:KYC_schema,db:Session=Depends(get_db)):
    return create_kyc(kyc_in,db)
####################################################################################################
####################################################################################################
@router.delete("/delete_kyc")
def kyc_delete(id:int,db:Session=Depends(get_db)):
    return  delete_kyc(id,db)

####################################################################################################
####################################################################################################
@router.post("/postkycproof")
async def proof_id(
    kyc_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await creat_kyc_id_proof(kyc_id, file, db)


####################################################################################################
####################################################################################################
@router.post("/creat_bank_details")
def create_bank(bank_in:Bank_kyc_schema,db:Session=Depends(get_db)):
    return  create_banK_details(bank_in,db)
####################################################################################################
####################################################################################################