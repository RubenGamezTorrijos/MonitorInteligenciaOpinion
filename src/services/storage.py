import json
import os
import pandas as pd
import pickle
from datetime import datetime
from typing import List, Dict, Optional
from src.config.constants import DATA_DIR

class ReviewRepository:
    """Handles local persistence of review data (JSON-based Data Lake)."""
    
    def __init__(self):
        # Ensure data directory exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            
    def _get_filepath(self, domain: str) -> str:
        """Returns the standard filepath for a domain's history."""
        clean_domain = domain.lower().replace(" ", "").split('/')[0]
        return os.path.join(DATA_DIR, f"{clean_domain}_history.json")

    def save_reviews(self, domain: str, df_new: pd.DataFrame) -> int:
        """
        Saves new reviews to the domain's history file.
        Returns the number of new reviews added.
        """
        if df_new.empty:
            return 0
            
        filepath = self._get_filepath(domain)
        
        # Load existing
        current_data = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    current_data = json.load(f)
            except Exception as e:
                print(f"Error loading history for {domain}: {e}")
                current_data = []
        
        # Create a set of existing (user, date, text) tuples to avoid duplicates
        existing_signatures = {
            (r.get('user', ''), r.get('date', ''), r.get('text', '')[:50]) 
            for r in current_data
        }
        
        # Filter new reviews
        new_count = 0
        for _, row in df_new.iterrows():
            # Create signature
            sig = (row.get('user', ''), row.get('date', ''), row.get('text', '')[:50])
            
            if sig not in existing_signatures:
                # Convert row to dict and handle timestamps
                record = row.to_dict()
                if 'timestamp_scraping' not in record:
                    record['timestamp_scraping'] = datetime.now().isoformat()
                    
                current_data.append(record)
                existing_signatures.add(sig)
                new_count += 1
                
        # Save back if there are changes
        if new_count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
                
        return new_count

    def load_history(self, domain: str) -> pd.DataFrame:
        """Loads the full review history for a domain."""
        filepath = self._get_filepath(domain)
        if not os.path.exists(filepath):
            return pd.DataFrame()
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        except Exception:
            return pd.DataFrame()

    def get_global_corpus(self) -> List[str]:
        """Loads ALL text content from ALL domains for global training."""
        all_texts = []
        # Iterate over all json files in data dir
        for filename in os.listdir(DATA_DIR):
            if filename.endswith("_history.json"):
                try:
                    filepath = os.path.join(DATA_DIR, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        texts = [d.get('text', '') for d in data if d.get('text')]
                        all_texts.extend(texts)
                except:
                    pass
        return all_texts

class ModelRegistry:
    """Handles persistence of trained Machine Learning models (Pickle-based)."""
    
    def __init__(self):
        self.model_dir = os.path.join(DATA_DIR, "models")
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
            
    def save_model(self, name: str, model_obj):
        """Saves a model object to a .pkl file."""
        filepath = os.path.join(self.model_dir, f"{name}.pkl")
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(model_obj, f)
            return True
        except Exception as e:
            print(f"Error saving model {name}: {e}")
            return False

    def load_model(self, name: str):
        """Loads a model object from a .pkl file."""
        filepath = os.path.join(self.model_dir, f"{name}.pkl")
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading model {name}: {e}")
            return None
