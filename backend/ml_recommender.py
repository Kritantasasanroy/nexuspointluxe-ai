# backend/ml_recommender.py

from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_similar_items(user_history, product_catalog, top_n=3):
    feature_keys = ["occasion", "color_vibe", "budget", "type", "weight"]
    def filter_keys(item):
        return {k: item[k] for k in feature_keys}
    v = DictVectorizer(sparse=False)

    # Prepare features
    likes = [filter_keys(item) for item in user_history["likes"]]
    dislikes = [filter_keys(item) for item in user_history["dislikes"]]
    products = [filter_keys(item) for item in product_catalog]
    X_products = v.fit_transform(products)
    scores = np.zeros(len(product_catalog))

    # Score by similarity to likes
    if likes:
        X_likes = v.transform(likes)
        sim_likes = cosine_similarity(X_products, X_likes).mean(axis=1)
        scores += sim_likes
    # Penalize similarity to dislikes
    if dislikes:
        X_dislikes = v.transform(dislikes)
        sim_dislikes = cosine_similarity(X_products, X_dislikes).mean(axis=1)
        scores -= sim_dislikes

    # Sort by score
    top_indices = scores.argsort()[::-1][:top_n]
    return [product_catalog[i] for i in top_indices]
