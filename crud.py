from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import uuid
import json
import os

app = FastAPI()
Filename = "database.json"

class Item(BaseModel):
    name: str
    email: EmailStr
    text: str

class TextInput(BaseModel):
    text: str

def load_data():
    if os.path.exists(Filename):
        try:
            with open(Filename, "r") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
    return []

def save_data(data):
    with open(Filename, "w") as file:
        json.dump(data, file, indent=2)

@app.post("/users")
def create_user(item: Item):
    data = load_data()
    user_id = int(uuid.uuid4().int % 10000)
    record = {
        "user_id": user_id,
        "name": item.name,
        "email": item.email,
        "text": item.text
    }
    data.append(record)
    save_data(data)
    return {"message": "User added successfully", "user": record}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    data = load_data()
    for user in data:
        if user.get("user_id") == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/all_users")
def get_all_users():
    return load_data()

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: Item):
    data = load_data()
    for user in data:
        if user.get("user_id") == user_id:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            user["text"] = updated_user.text
            save_data(data)
            return {"message": "User updated successfully", "user": user}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    data = load_data()
    for user in data:
        if user.get("user_id") == user_id:
            data.remove(user)
            save_data(data)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
        

@app.post("/analyze/{user_id}")
def analyze_text(user_id: int):
    data = load_data() 
    for user in data:
        if user.get("user_id") == user_id:
            text = user.get("text", "")
            break
    else:
        raise HTTPException(status_code=404, detail="User not found")
    if len(text) > 200:
        raise HTTPException(status_code=400, detail="Text exceeds 200 characters")
        

    result = {
        "word_count": len(text.split()),
        "char_count": len(text),
        "special_char_count": sum(1 for c in text if not c.isalnum() and not c.isspace()),
        "uppercase_count": sum(1 for c in text if c.isupper()),
        "lowercase_count": sum(1 for c in text if c.islower())
    }
    return result


