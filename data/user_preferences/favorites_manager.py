import json
import os

class FavoritesManager:
    def __init__(self, favorites_file="data/user_preferences/favorites.json"):
        self.favorites_file = favorites_file
        self.max_favorites = 5
        os.makedirs(os.path.dirname(favorites_file), exist_ok=True)
        if not os.path.exists(favorites_file):
            with open(favorites_file, 'w') as f:
                json.dump([], f)
    
    def get_favorites(self):
        try:
            with open(self.favorites_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def add_favorite(self, city):
        favorites = self.get_favorites()
        city = city.strip().title()
        
        if city in favorites:
            return False, f"{city} already in favorites"
        if len(favorites) >= self.max_favorites:
            return False, f"Maximum {self.max_favorites} favorites allowed"
        
        favorites.append(city)
        with open(self.favorites_file, 'w') as f:
            json.dump(favorites, f)
        return True, f"{city} added"
    
    def remove_favorite(self, city):
        favorites = self.get_favorites()
        city = city.strip().title()
        
        if city not in favorites:
            return False, f"{city} not in favorites"
        
        favorites.remove(city)
        with open(self.favorites_file, 'w') as f:
            json.dump(favorites, f)
        return True, f"{city} removed"