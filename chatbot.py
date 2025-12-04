from typing import Dict, Any, List
from semantic_kernel import KernelContext
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
import json

class CarnivoreDietSkill:
    """diker Core skills for carnivore diet advice"""
    
    @sk_function(
        description="Provides information about carnivore and ketogenic diets",
        name="explain_carnivore_diet"
    )
    def explain_carnivore_diet(self, context: KernelContext) -> str:
        return """
        The Carnivore Diet is a zero-carb, high-fat diet that consists entirely of animal products.
        
        🔥 Key Benefits:
        1. Rapid fat loss and weight management
        2. Reduced inflammation and autoimmune symptoms
        3. Improved mental clarity and focus
        4. Stable energy throughout the day
        5. Simplified eating with no carb counting
        
        🥩 What to Eat:
        • Red meat (beef, lamb, bison)
        • Organ meats (liver, heart, kidney)
        • Poultry (chicken, turkey, duck)
        • Fish and seafood
        • Eggs
        • Animal fats (butter, tallow, lard)
        
        ❌ What to Avoid:
        • All plant foods (vegetables, fruits, grains)
        • Sugars and sweeteners
        • Seed oils (canola, soybean, corn oil)
        • Processed foods
        • Alcohol
        """
    
    @sk_function(
        description="Provides daily meal suggestions based on carnivore principles",
        name="suggest_meals"
    )
    @sk_function_context_parameter(
        name="meal_type",
        description="Breakfast, lunch, or dinner",
        default_value="any"
    )
    def suggest_meals(self, context: KernelContext) -> str:
        meal_type = context.variables.get("meal_type", "any").lower()
        
        meals = {
            "breakfast": [
                "🥚 4-6 scrambled eggs cooked in butter or tallow",
                "🥓 4-6 slices of bacon or sausage",
                "🥩 Leftover steak from dinner",
                "🍳 Ribeye steak and eggs"
            ],
            "lunch": [
                "🍔 2-3 beef burger patties (no bun)",
                "🍗 Chicken thighs with skin cooked in duck fat",
                "🥩 8-12oz of ground beef with melted cheese",
                "🐟 Canned sardines or salmon"
            ],
            "dinner": [
                "🥩 12-16oz ribeye or New York strip steak",
                "🐑 Lamb chops with rosemary butter",
                "🐖 Pork belly or pork shoulder",
                "🍣 Salmon fillet with lemon butter sauce"
            ]
        }
        
        if meal_type in meals:
            suggestions = meals[meal_type]
        else:
            suggestions = meals["breakfast"] + meals["lunch"] + meals["dinner"]
        
        return f"Suggested {meal_type if meal_type != 'any' else ''} meals:\n" + "\n".join([f"• {meal}" for meal in suggestions])
    
    @sk_function(
        description="Explains the importance of Vitamin D3 and K2, especially in winter",
        name="explain_vitamin_d3_k2"
    )
    def explain_vitamin_d3_k2(self, context: KernelContext) -> str:
        return """
        🌞 Vitamin D3 + K2: The Winter Essentials
        
        Why they're crucial in winter:
        1. **Vitamin D3**: 
           • Sunlight exposure drops significantly in winter
           • Most people become deficient without supplementation
           • Essential for immune function, bone health, and mood regulation
           • Carnivore sources: Fatty fish (salmon, mackerel), liver, egg yolks
           
        2. **Vitamin K2**:
           • Works synergistically with D3
           • Directs calcium to bones (not arteries)
           • Prevents arterial calcification
           • Carnivore sources: Goose liver, hard cheeses, butter from grass-fed cows
           
        💊 Recommended Winter Protocol:
        • D3: 5000-10000 IU daily with fatty meal
        • K2 (MK-7): 100-200mcg daily
        • Always take together for optimal absorption
        • Get blood levels checked every 3-6 months
        """
    
    @sk_function(
        description="Lists foods to avoid on carnivore/keto diet",
        name="list_foods_to_avoid"
    )
    def list_foods_to_avoid(self, context: KernelContext) -> str:
        foods = [
            "🚫 Seed oils: Canola, soybean, corn, sunflower, safflower oil",
            "🚫 Sugars: All forms including honey, maple syrup, agave",
            "🚫 Grains: Wheat, rice, oats, corn, quinoa",
            "🚫 Legumes: Beans, lentils, peanuts, soy",
            "🚫 Processed foods: Anything with ingredient labels",
            "🚫 Vegetables high in oxalates: Spinach, kale, almonds, beets",
            "🚫 Fruits: All fruits (except occasional berries in keto)",
            "🚫 Alcohol: Beer, wine, spirits (except occasional dry wine in keto)",
            "🚫 Artificial sweeteners: Aspartame, sucralose, saccharin"
        ]
        
        return "🍽️ Foods to Avoid on Carnivore/Keto:\n" + "\n".join(foods)
    
    @sk_function(
        description="Explains why red meat is nutritionally superior",
        name="explain_red_meat_benefits"
    )
    def explain_red_meat_benefits(self, context: KernelContext) -> str:
        return """
        🥩 Why Red Meat is King:
        
        Nutrient Density Comparison (per 100g):
        • Complete Protein: 20-30g vs 2-3g in plants
        • Heme Iron: Highly bioavailable vs non-heme in plants
        • Zinc: 5-7mg vs 1-2mg in plant sources
        • B12: Found ONLY in animal products
        • Creatine: Essential for brain and muscle function
        • Carnosine: Anti-aging and muscle endurance
        • CLA: Natural fat-burning compound
        • Cholesterol: Essential for hormone production
        
        🌱 Anti-Nutrients in Plants:
        • Oxalates (kidney stones)
        • Lectins (gut irritation)
        • Phytic acid (mineral blocker)
        • Goitrogens (thyroid disruption)
        • FODMAPs (digestive issues)
        
        Red meat contains none of these!
        """

class NutrientDatabase:
    """Database of nutrient information for carnivore foods"""
    
    def __init__(self):
        self.foods = {
            "ribeye_steak": {
                "protein_g": 29,
                "fat_g": 24,
                "carbs_g": 0,
                "calories": 330,
                "vitamin_b12_mcg": 2.9,
                "zinc_mg": 6.2,
                "iron_mg": 2.4
            },
            "eggs": {
                "protein_g": 13,
                "fat_g": 11,
                "carbs_g": 1,
                "calories": 155,
                "vitamin_d_iu": 87,
                "choline_mg": 147,
                "selenium_mcg": 23
            },
            "liver": {
                "protein_g": 26,
                "fat_g": 4,
                "carbs_g": 3,
                "calories": 153,
                "vitamin_a_iu": 16898,
                "vitamin_b12_mcg": 70.6,
                "copper_mg": 12
            }
        }
    
    def get_nutrient_info(self, food_name: str) -> Dict[str, Any]:
        return self.foods.get(food_name.lower().replace(" ", "_"), {})
