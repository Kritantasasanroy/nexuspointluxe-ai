# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from style_logic import suggest_outfits
from ml_recommender import get_similar_items
from product_data import product_catalog
from user_history import save_user_feedback, get_user_history, user_has_history
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StyleRequest(BaseModel):
    occasion: str
    temperature: float
    color_vibe: str
    budget: str
    user_id: Optional[str] = "demo_user"

class FeedbackRequest(BaseModel):
    user_id: str
    liked_item_name: Optional[str] = None
    disliked_item_name: Optional[str] = None

class CommentRequest(BaseModel):
    user_id: str
    feedback: str

@app.post("/style")
def get_style_suggestions(request: StyleRequest):
    if user_has_history(request.user_id):
        user_history = get_user_history(request.user_id)
        outfits = get_similar_items(user_history, product_catalog)
        for o in outfits:
            o["why"] = "Recommended based on your feedback."
    else:
        outfits = suggest_outfits(request)
    return {"outfits": outfits}

@app.post("/feedback")
def save_feedback(request: FeedbackRequest):
    if request.liked_item_name:
        for item in product_catalog:
            if item["name"] == request.liked_item_name:
                save_user_feedback(request.user_id, liked_item=item)
                return {"status": "like saved"}
    if request.disliked_item_name:
        for item in product_catalog:
            if item["name"] == request.disliked_item_name:
                save_user_feedback(request.user_id, disliked_item=item)
                return {"status": "dislike saved"}
    return {"status": "not found"}

@app.post("/comment")
def save_comment(request: CommentRequest):
    save_user_feedback(request.user_id, feedback_text=request.feedback)
    return {"status": "comment saved"}
