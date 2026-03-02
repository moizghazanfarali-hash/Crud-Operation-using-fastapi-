from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,EmailStr
import json
import os
import uuid

app = FastAPI()
FileName = "database.json"


class User(BaseModel):
    name: str
    email: EmailStr


def load_data():
    if os.path.exists(FileName):
        try:
            with open(FileName, "r") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
    return []


def save_data(data):
    with open(FileName, "w") as file:
        json.dump(data, file, indent=4)


@app.post("/users")
def create_user(user: User):
    data = load_data()

    user_id = str(uuid.uuid4())

    record = {
        "user_id": user_id,
        "name": user.name,
        "email":user.email
        

    }

    data.append(record)
    save_data(data)

    return {"message": "User created successfully", "user": record}
    
@app.get("/all_users)
def all_data():
    return load_data()

@app.get("/users/{user_id}")
def get_user(user_id: str):
    data = load_data()

    for user in data:
        if user.get("user_id") == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}")
def update_user(user_id: str, updated_user: User):
    data = load_data()

    for user in data:
        if user.get("user_id") == user_id:
            user["name"] = updated_user.name
            user["email"] = user_email.email

            save_data(data)
            return {"message": "User updated successfully", "user": user}

    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    data = load_data()

    for index, user in enumerate(data):
        if user.get("user_id") == user_id:
            deleted_user = data.pop(index)
            save_data(data)
            return {"message": "User deleted successfully", "user": deleted_user}

    raise HTTPException(status_code=404, detail="User not found")

class Analyst(BaseModel):
    your_personal_information: str
 
@app.post("/analysts/{user_id}")
def create_analyst(user_id: str, analyst: Analyst):

    data = load_data()

    # 🔍 Check if user exists
    user_found = False
    for user in data:
        if user.get("user_id") == user_id:
            user_found = True
            break

    if not user_found:
        raise HTTPException(status_code=404, detail="User not found")

    text = analyst.your_personal_information

    if not text:
        raise HTTPException(status_code=400, detail="Input cannot be empty.")

    if len(text) > 200:
        raise HTTPException(status_code=400, detail="Input exceeds 200 characters limit.")

    lower_count = sum(1 for c in text if c.islower())
    upper_count = sum(1 for c in text if c.isupper())
    total_chars = len(text)
    special_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
    word_count = len(text.split())

    analyst_id = str(uuid.uuid4())

    record = {
        "analyst_id": analyst_id,
        "user_id": user_id,
        "your_personal_information": text,
        "lowercase_count": lower_count,
        "uppercase_count": upper_count,
        "special_characters": special_count,
        "total_characters": total_chars,
        "word_count": word_count
    }

    data.append(record)
    save_data(data)


    return record
