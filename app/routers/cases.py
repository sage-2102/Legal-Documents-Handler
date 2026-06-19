from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.case import Case
from app.models.complaint import Complaint
from app.models.user import User

from app.schemas.cases import (
    CaseCreate,
    CaseOut
)

from app.auth.dependencies import (
    get_current_user,
    lawyer_only
)

router = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)


# ==========================
# CREATE CASE
# ==========================
@router.post(
    "/",
    response_model=CaseOut,
    status_code=status.HTTP_201_CREATED
)
def create_case(
    data: CaseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(lawyer_only)
):
    lawyer = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    complaint = db.query(Complaint).filter(
        Complaint.id == data.complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    new_case = Case(
        complaint_id=data.complaint_id,
        client_id=complaint.client_id,
        lawyer_id=lawyer.id,
        hearing_date=data.hearing_date,
        status="Open"
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case


# ==========================
# GET ALL CASES
# ==========================
@router.get("/")
def get_cases(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    if user.role == "lawyer":
        cases = db.query(Case).filter(
            Case.lawyer_id == user.id
        ).all()

    elif user.role == "client":
        cases = db.query(Case).filter(
            Case.client_id == user.id
        ).all()

    else:
        cases = db.query(Case).all()

    return cases


# ==========================
# GET SINGLE CASE
# ==========================
@router.get(
    "/{case_id}",
    response_model=CaseOut
)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case


# ==========================
# UPDATE CASE STATUS
# ==========================
@router.put("/{case_id}/status")
def update_case_status(
    case_id: int,
    status_text: str,
    db: Session = Depends(get_db),
    current_user=Depends(lawyer_only)
):
    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    case.status = status_text

    db.commit()
    db.refresh(case)

    return {
        "message": "Case status updated",
        "case": case
    }


# ==========================
# UPDATE HEARING DATE
# ==========================
@router.put("/{case_id}/hearing")
def update_hearing_date(
    case_id: int,
    hearing_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(lawyer_only)
):
    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    case.hearing_date = hearing_date

    db.commit()
    db.refresh(case)

    return {
        "message": "Hearing date updated",
        "case": case
    }


# ==========================
# UPDATE NOTES
# ==========================
@router.put("/{case_id}/notes")
def update_case_notes(
    case_id: int,
    notes: str,
    db: Session = Depends(get_db),
    current_user=Depends(lawyer_only)
):
    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    case.notes = notes

    db.commit()
    db.refresh(case)

    return {
        "message": "Case notes updated",
        "case": case
    }


# ==========================
# DELETE CASE
# ==========================
@router.delete("/{case_id}")
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(lawyer_only)
):
    case = db.query(Case).filter(
        Case.id == case_id
    ).first()

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    db.delete(case)
    db.commit()

    return {
        "message": "Case deleted successfully"
    }