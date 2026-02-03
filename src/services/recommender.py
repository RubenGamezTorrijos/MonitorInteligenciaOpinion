import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class CollaborativeFilteringService:
    """Implements User-to-User and Item-to-Item filtering for sentiment prediction."""
    
    def __init__(self):
        self.user_item_matrix = None
        self.user_similarity = None
        self.item_similarity = None

    def fit(self, df: pd.DataFrame):
        """Builds user-item matrix from reviews (user_id, product_id, score)."""
        self.user_item_matrix = df.pivot_table(index='user_id', columns='product_id', values='sentimiento_score').fillna(0)
        
    def pearson_similarity(self, u1: pd.Series, u2: pd.Series) -> float:
        """Calculates Pearson correlation between two users/items."""
        mask = (u1 != 0) & (u2 != 0)
        if not mask.any():
            return 0
        
        u1_m = u1[mask]
        u2_m = u2[mask]
        
        if len(u1_m) < 2: return 0
        
        u1_mean = u1_m.mean()
        u2_mean = u2_m.mean()
        
        num = np.sum((u1_m - u1_mean) * (u2_m - u2_mean))
        den = np.sqrt(np.sum((u1_m - u1_mean)**2)) * np.sqrt(np.sum((u2_m - u2_mean)**2))
        
        if den == 0: return 0
        return num / den

    def predict_user_item(self, user_id: str, item_id: str, k: int = 5) -> float:
        """Predicts score using User-to-User CF based on k-nearest neighbors."""
        if user_id not in self.user_item_matrix.index or item_id not in self.user_item_matrix.columns:
            return 0.0
            
        target_user_ratings = self.user_item_matrix.loc[user_id]
        if target_user_ratings[item_id] != 0:
            return target_user_ratings[item_id]
            
        similarities = []
        for other_user in self.user_item_matrix.index:
            if other_user == user_id: continue
            sim = self.pearson_similarity(target_user_ratings, self.user_item_matrix.loc[other_user])
            if sim > 0:
                similarities.append((sim, self.user_item_matrix.loc[other_user, item_id]))
                
        # Sort and take top k
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_k = similarities[:k]
        
        if not top_k: return 0.0
        
        num = sum(sim * score for sim, score in top_k if score != 0)
        den = sum(abs(sim) for sim, score in top_k if score != 0)
        
        return num / den if den != 0 else 0.0

    def predict_item_item(self, user_id: str, item_id: str, k: int = 5) -> float:
        """Predicts score using Item-to-Item CF."""
        if user_id not in self.user_item_matrix.index or item_id not in self.user_item_matrix.columns:
            return 0.0
            
        user_ratings = self.user_item_matrix.loc[user_id]
        item_ratings = self.user_item_matrix[item_id]
        
        similarities = []
        for other_item in self.user_item_matrix.columns:
            if other_item == item_id: continue
            sim = self.pearson_similarity(item_ratings, self.user_item_matrix[other_item])
            if sim > 0:
                similarities.append((sim, user_ratings[other_item]))
                
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_k = similarities[:k]
        
        if not top_k: return 0.0
        
        num = sum(sim * score for sim, score in top_k if score != 0)
        den = sum(abs(sim) for sim, score in top_k if score != 0)
        
        return num / den if den != 0 else 0.0
