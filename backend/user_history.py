# backend/user_history.py

user_histories = {}

def save_user_feedback(user_id, liked_item=None, disliked_item=None, feedback_text=None):
    if user_id not in user_histories:
        user_histories[user_id] = {"likes": [], "dislikes": [], "feedback": []}
    if liked_item:
        user_histories[user_id]["likes"].append(liked_item)
    if disliked_item:
        user_histories[user_id]["dislikes"].append(disliked_item)
    if feedback_text:
        user_histories[user_id]["feedback"].append(feedback_text)

def get_user_history(user_id):
    return user_histories.get(user_id, {"likes": [], "dislikes": [], "feedback": []})

def user_has_history(user_id):
    return user_id in user_histories and (user_histories[user_id]["likes"] or user_histories[user_id]["dislikes"])
