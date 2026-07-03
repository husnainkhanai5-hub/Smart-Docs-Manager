from fastapi import APIRouter, Form, File, UploadFile
from pydantic import BaseModel
from database import db
from bson import ObjectId
import os
import shutil

router = APIRouter(prefix="/documents", tags=["Documents"])


class Document(BaseModel):
    title: str
    description: str


@router.post("/upload")
def upload_document(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    try:
        if os.path.exists("uploads") == False:
            os.makedirs("uploads")

        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        hus = {
            "title": title,
            "description": description,
            "file_path": file_path
        }
        db.documents.insert_one(hus)
        return {"_id": str(hus["_id"]), "message": "Document uploaded successfully", "status": 200}
    except Exception as e:
        return {"message": f"Document upload failed: {str(e)}", "data": None, "status": 500}


@router.get("/")
def get_all_documents():
    try:
        documents = db.documents.find()
        list_of_documents = []
        for document in documents:
            document["_id"] = str(document["_id"])
            list_of_documents.append(document)
        return {"message": "Documents fetched successfully",
            "data": list_of_documents,
            "status": 200}
    except Exception as e:
        return {
            "message": f"Documents fetch failed: {str(e)}",
            "data": None,
            "status": 500
        }


@router.get("/{id}")
def get_document(id: str):
    try:
        document = db.documents.find_one({"_id": ObjectId(id)})
        document["_id"] = str(document["_id"])
        return {"message": "Document fetched successfully",
            "data": document,
            "status": 200}
    except Exception as e:
        return {
            "message": f"Document fetch failed: {str(e)}",
            "data": None,
            "status": 500
        }


@router.delete("/{id}")
def delete_document(id: str):
    try:
        document = db.documents.delete_one({"_id": ObjectId(id)})
        if document.deleted_count == 0:
            return {"message": "Document not found",
                "data": None,
                "status": 404}
        return {"message": "Document deleted successfully",
            "data": None,
            "status": 200}
    except Exception as e:
        return {
            "message": f"Document delete failed: {str(e)}",
            "data": None,
            "status": 500
        }
@router.put("/{id}")
def update_document(id: str, title: str = Form(...), description: str = Form(...)):
    try:
        document = db.documents.update_one({"_id": ObjectId(id)}, {"$set": {"title": title, "description": description}})
        if document.modified_count == 0:
            return {"message": "Document not found",
                "data": None,
                "status": 404}
        return {"message": "Document updated successfully",
            "data": None,
            "status": 200}
    except Exception as e:
        return {
            "message": f"Document update failed: {str(e)}",
            "data": None,
            "status": 500
        }
