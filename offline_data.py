IMG_DEFAULT = "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800&q=80"

def get_demo_recipe(user_input):
    user_input = user_input.lower()
    
    # 1. DESSERT MATCH
    if any(x in user_input for x in ["sugar", "chocolate", "milk", "sweet", "cake"]):
        return {
            "title": "Midnight Molten Lava Mug Cake",
            "image": "https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=800&q=80",
            "logic": "A rich, gooey chocolate fix ready in 2 minutes.",
            "taste_profile": "Rich, Sweet, Gooey",
            "tasting_notes": "An explosion of warm dark chocolate with a velvety texture.",
            "time": "5 Mins",
            "ingredients_data": [
                {"item": "2 tbsp Flour", "substitute": "Almond Flour"},
                {"item": "2 tbsp Cocoa", "substitute": "Melted Chocolate"},
                {"item": "1 tbsp Sugar", "substitute": "Honey/Maple Syrup"}
            ],
            "instructions": [
                {"text": "Mix dry ingredients in a mug.", "image_url": "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=400"},
                {"text": "Stir in milk.", "image_url": "https://images.unsplash.com/photo-1607920592519-bab4d79134fb?w=400"}
            ],
            "nutrition": {"Protein": "4g", "Carbs": "35g", "Fat": "8g"},
            "beverages": [],
            "storage": "Eat immediately."
        }

    # 2. DEFAULT MATCH (Savory)
    return {
        "title": "Royal Dhaba Egg Curry",
        "image": "https://images.unsplash.com/photo-1525351484163-7529414395d8?w=800&q=80",
        "logic": "Transforms simple boiled eggs into a rich main course.",
        "taste_profile": "Spicy, Savory, Creamy",
        "tasting_notes": "A robust blend of roasted spices with a creamy tomato finish.",
        "time": "20 Mins",
        "ingredients_data": [
            {"item": "4 Boiled Eggs", "substitute": "Paneer or Potatoes"},
            {"item": "2 Tomatoes", "substitute": "Tomato Puree"},
            {"item": "1 Onion", "substitute": "Fried Onion Paste"}
        ],
        "instructions": [
            {"text": "Fry boiled eggs.", "image_url": "https://images.unsplash.com/photo-1591458761786-e883584852aa?w=600"},
            {"text": "Sauté onions.", "image_url": "https://images.unsplash.com/photo-1629196914375-f7e48f477b6d?w=600"}
        ],
        "nutrition": {"Protein": "24g", "Carbs": "12g", "Fat": "18g"},
        "beverages": [],
        "storage": "Refrigerate for 2 days."
    }