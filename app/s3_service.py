from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
from app.s3_utils import list_company_reports, get_report_file
from app.database import get_db
from app.models import User
from app.auth_utils import decode_access_token

router = APIRouter()

def get_current_user_company_code(request: Request) -> str:
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    token_data = decode_access_token(token)
    
    if not token_data or not token_data.username:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    db = next(get_db())
    user = db.query(User).filter(User.username == token_data.username).first()
    if not user or not user.company:
        raise HTTPException(status_code=404, detail="User or company not found")

    return user.company.company_code

@router.get("/", summary="List all reports for the current user's company")
def get_reports(request: Request):
    try:
        company_code = get_current_user_company_code(request)
        reports = list_company_reports(company_code)
        return {"reports": reports}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{report_file}", summary="Get a specific report file")
def get_report(report_file: str, request: Request):
    try:
        company_code = get_current_user_company_code(request)
        s3_key = f"mock_s3_archive/reports/{company_code}/{report_file}"
        report_data = get_report_file(s3_key)
        return {"data": report_data}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))