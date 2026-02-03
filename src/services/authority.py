import numpy as np
import pandas as pd
from typing import Dict, List, Set

class UserAuthorityService:
    """Calculates user importance using PageRank algorithm."""
    
    def __init__(self, damping_factor: float = 0.85):
        self.d = damping_factor
        self.pagerank: Dict[str, float] = {}

    def calculate_authority(self, interactions: pd.DataFrame):
        """
        Calculates PageRank for users.
        Interactions should have 'source_user' and 'target_user'.
        """
        users = set(interactions['source_user']).union(set(interactions['target_user']))
        if not users:
            return {}
            
        n = len(users)
        adj_list: Dict[str, List[str]] = {u: [] for u in users}
        out_degree: Dict[str, int] = {u: 0 for u in users}
        
        for _, row in interactions.iterrows():
            adj_list[row['source_user']].append(row['target_user'])
            out_degree[row['source_user']] += 1
            
        # Initial pagerank
        pr = {u: 1/n for u in users}
        
        # Iterative calculation (simple version for the practice)
        for _ in range(20):
            new_pr = {u: (1 - self.d) / n for u in users}
            for u in users:
                if out_degree[u] > 0:
                    delta = self.d * pr[u] / out_degree[u]
                    for neighbor in adj_list[u]:
                        new_pr[neighbor] += delta
                else:
                    # Sink node distribution
                    for v in users:
                        new_pr[v] += self.d * pr[u] / n
            pr = new_pr
            
        self.pagerank = pr
        return pr

    def get_user_weight(self, user_id: str) -> float:
        """Returns the authority weight for a user, defaults to average if unknown."""
        if not self.pagerank:
            return 1.0
        return self.pagerank.get(user_id, sum(self.pagerank.values()) / len(self.pagerank))
