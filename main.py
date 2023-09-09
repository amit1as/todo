from Models import Todo
from uuid import uuid4

import firebase_admin
from firebase_admin import credentials,firestore

from fastapi import FastAPI
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

collection_name = "sigaram_test_collection"

app = FastAPI()
db = firestore.client()

todos = []

# Get all todos
@app.get("/")
def get_todos():
    todos_ref = db.collection(collection_name)
    todos = todos_ref.stream()

    todo_list = []
    for todo in todos:
        todo_data = todo.to_dict()
        todo_data["id"] = todo.id
        todo_list.append(todo_data)

    return {"todos": todo_list}

# Get todo by id (single)
@app.get("/todo/{id}")
def get_todo(id:int):
    for todo in todos:
        if id == todo.id:
            return {"todo": todo}
    return {"message": "Todo not found!"}


# Create todo
@app.post("/")
async def create_todo(todo:Todo):
    todos_ref = db.collection(collection_name)
    todo_id = str(uuid4())
    print(todo_id)
    new_todo = dict(todo)
    todos_ref.document(todo_id).set(new_todo)
    new_todo["id"] = todo_id
    return {"todos":  new_todo}


# Update to (requires id)
@app.put("/todo/{todo_id}")
async def update_todo(todo_id:str,todo:Todo):
    doc_ref = db.collection(collection_name).document(todo_id)
    ss = doc_ref.get()
    if ss.exists:
        doc_ref.document(todo_id).set(dict(todo))
        return {"message": "Updated Successfully!"}
    return {"message": "Invalid id!"}

# Delete todo (requires id)
@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id:str):
    doc_ref = db.collection(collection_name).document(todo_id)
    ss = doc_ref.get()
    if ss.exists:
        doc_ref.delete()
        return {"message": "Deleted successfully!"}
    return {"message": "Todo not found!"}