from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import io, base64

from .config.mongo import collection
from .config.database import get_db
from .models.users import Users


app = FastAPI()


@app.post("/")
async def create(
    full_name: str,
    email: EmailStr,
    password: str,
    phone: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    is_user_exists = db.query(Users).filter_by(email=email).first()
    if is_user_exists:
        raise HTTPException(status_code=400, detail="Email already taken")
    user_object = Users(
        full_name=full_name,
        email=email,
        password=hashed_password,
        phone=phone,
    )
    print(user_object)
    db.add(user_object)
    db.commit()
    file_content = await file.read()
    await collection.insert_one(
        {"filename": file.filename, "content": file_content, "user_id": user_object.id}
    )
    return {"success": True, "id": user_object.id}


@app.get("/")
async def users(id: int, db: Session = Depends(get_db)):
    user_object = db.query(Users).filter_by(id=id).first()
    if user_object:
        user_profile = await collection.find_one({"user_id": user_object.id})
        if user_profile:
            file_content = user_profile.get("content")
            filename = user_profile.get("filename")
            if file_content and filename:
                user_details = {
                    "id": user_object.id,
                    "name": user_object.full_name,
                    "email": user_object.email,
                    "phone": user_object.phone,
                }
                # Return file as json response by encoding file using base64
                file_stream = io.BytesIO(file_content)
                encoded_file_content = base64.b64encode(file_stream.getvalue()).decode()
                response_data = {
                    "file_content": encoded_file_content,
                    "data": user_details,
                }
                response = JSONResponse(content=response_data)
                return response
        return {user_object}
    return {"status": "no user found"}
