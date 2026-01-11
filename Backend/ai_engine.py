import json
import random
import urllib.parse
import re
from groq import Groq

# --- 1. POLLINATIONS IMAGE ENGINE (Magic Link) ---
def get_image_url(prompt):
    clean_prompt = re.sub(r'[^a-zA-Z0-9, ]', '', prompt)
    seed = random.randint(1, 999999)
    final_prompt = f"{clean_prompt}, professional food photography, 4k, delicious, michelin star plating, cinematic lighting"
    encoded = urllib.parse.quote(final_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=600&model=flux&seed={seed}&nologo=true"

# --- 2. RECIPE ENGINE ---
def generate_ai_recipe(groq_key, hf_token, ingredients, diet, vibe, cuisine, language, occasion, mood, leftover_mode, input_type, fireless_mode, servings, *args, **kwargs):
    
    try:
        client = Groq(api_key=groq_key)
        
        # --- STRICT INSTRUCTOR MODE ---
        system_role = "Act as a Patient Cooking Instructor."
        
        # CRITICAL CONSTRAINTS
        constraints = """
        1. COURSE STRICTNESS: If the user selected 'Dessert', the recipe MUST be a sweet dish. If they have onions/garlic, you must either find a way to make it sweet (e.g. onion jam tart) or ignore the savory ingredients if they clash too much. If 'Dinner/Lunch', it must be savory.
        2. QUANTITIES: You MUST repeat specific quantities in steps (e.g., '1 tsp salt').
        3. FROM SCRATCH: Do not assume pre-cooked items. Teach every step.
        4. SPICES: List all spices in the ingredients list.
        5. MANDATORY: Generate 'storage_tips' and 4 beverages.
        """
        
        if fireless_mode:
            system_role = "Act as a Student in a Dorm."
            constraints += " NO STOVE, NO OVEN. Kettle/Bowl only."
        if input_type == "Cooked Leftover (Repurpose Dish)":
            constraints += f" REPURPOSE LEFTOVERS: {ingredients}."

        prompt = f"""
        {system_role} Create a detailed recipe for {servings} people.
        Context: {input_type}. Ingredients: {ingredients}.
        Diet: {diet}. Cuisine: {cuisine}. Occasion: {occasion}. Mood: {mood}.
        Course Selection: {vibe}
        CONSTRAINTS: {constraints}
        
        RETURN JSON ONLY:
        {{
            "status": "success",
            "title": "Recipe Title",
            "logic": "Why this works",
            "ingredients_data": [
                {{"item": "Qty Item Name", "substitute": "Alternative"}}
            ],
            "instructions": [
                {{"text": "Detailed step...", "visual": "visual cue"}}
            ],
            "storage_tips": "Storage instructions.",
            "nutrition": {{ "Protein": "XXg", "Carbs": "XXg", "Fat": "XXg", "Calories": "XXX" }},
            "beverages": [
                {{"name": "Drink 1", "type": "Type", "desc": "Desc", "quick_recipe": "Mix X and Y"}},
                {{"name": "Drink 2", "type": "Type", "desc": "Desc", "quick_recipe": "Mix X and Y"}},
                {{"name": "Drink 3", "type": "Type", "desc": "Desc", "quick_recipe": "Mix X and Y"}},
                {{"name": "Drink 4", "type": "Type", "desc": "Desc", "quick_recipe": "Mix X and Y"}}
            ],
            "tasting_notes": "Flavor profile",
            "taste_profile": "Savory/Sweet"
        }}
        """
        
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.3
        )
        recipe_data = json.loads(completion.choices[0].message.content)
        if isinstance(recipe_data, list): recipe_data = recipe_data[0]
        
        recipe_data["image"] = get_image_url(recipe_data.get('title', 'Food'))
        
        if 'instructions' in recipe_data:
            for i in range(len(recipe_data['instructions'])):
                recipe_data['instructions'][i]['image_url'] = None

        return recipe_data

    except Exception as e:
        return {
            "status": "error", "title": "System Error", 
            "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe",
            "logic": str(e), "ingredients_data": [], "instructions": []
        }

def get_sos_help(api_key, issue):
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Cooking Emergency: {issue}. Fix in 1 sentence."}], 
            model="llama-3.3-70b-versatile"
        )
        return completion.choices[0].message.content
    except: return "Connection Error."