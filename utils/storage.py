from firebase_setup import db
def get_user(uid):
    node = db.child(f"users/{uid}").get()
    return node.val() if node.exists() else None
def set_user(uid, data):
    db.child(f"users/{uid}").set(data)
def update_user(uid, data):
    db.child(f"users/{uid}").update(data)
def push_event(event):
    db.child("events").push(event)
def get_all_users():
    node = db.child("users").get()
    return node.val() or {}
