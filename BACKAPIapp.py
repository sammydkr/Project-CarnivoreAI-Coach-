from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from chatbot import CarnivoreDietSkill, NutrientDatabase
from image_generator import CarnivoreImageGenerator
from semantic_kernel_config import CarnivoreKernel
import json

app = FastAPI(title="CarnivoreAI Coach", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
kernel_manager = CarnivoreKernel()
diet_skill = CarnivoreDietSkill()
nutrient_db = NutrientDatabase()
image_gen = CarnivoreImageGenerator()

# Data models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"
    context: Optional[dict] = {}

class ImageRequest(BaseModel):
    theme: str
    caption: Optional[str] = ""

class MealPlanRequest(BaseModel):
    days: int = 7
    calories_per_day: Optional[int] = 2000
    preferences: Optional[list] = []

@app.get("/")
async def root():
    return {
        "name": "CarnivoreAI Coach",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "AI chat about carnivore diet",
            "/generate-image": "Generate health/food images",
            "/meal-plan": "Get carnivore meal plans",
            "/nutrients/{food}": "Get nutrient info for food"
        }
    }

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Main chatbot endpoint"""
    try:
        user_message = request.message.lower()
        
        # Route to appropriate skill based on message content
        if any(word in user_message for word in ["meal", "eat", "food", "recipe"]):
            response = diet_skill.suggest_meals({})
        elif any(word in user_message for word in ["avoid", "bad", "harmful"]):
            response = diet_skill.list_foods_to_avoid({})
        elif any(word in user_message for word in ["vitamin d", "vitamin k", "winter"]):
            response = diet_skill.explain_vitamin_d3_k2({})
        elif any(word in user_message for word in ["benefit", "why", "good"]):
            response = diet_skill.explain_red_meat_benefits({})
        elif any(word in user_message for word in ["explain", "what is", "tell me"]):
            response = diet_skill.explain_carnivore_diet({})
        else:
            # Use Semantic Kernel for complex queries
            context = kernel_manager.kernel.create_new_context()
            context["input"] = request.message
            
            # Import our skill
            skill = kernel_manager.kernel.import_skill(diet_skill, "carnivore")
            
            # Run the appropriate function
            result = await kernel_manager.kernel.run_async(
                skill["explain_carnivore_diet"],
                input_context=context
            )
            response = str(result)
        
        return {
            "response": response,
            "suggested_actions": [
                "Get meal suggestions",
                "Learn about nutrients",
                "See foods to avoid",
                "Generate motivational image"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-image")
async def generate_image(request: ImageRequest):
    """Generate motivational carnivore images"""
    try:
        image_url = image_gen.generate_health_image(request.theme)
        
        # Instagram-ready caption
        captions = {
            "motivation": "🔥 Feeling unstoppable on carnivore! Your body was designed to thrive on animal foods. #CarnivoreDiet #HealthTransformation",
            "food": "🥩 This is what optimal nutrition looks like! Real food doesn't need labels. #Steak #RealFood #CarnivoreLifestyle",
            "before_after": "🎯 Consistency beats perfection. Trust the process, eat the meat! #Transformation #CarnivoreJourney",
            "nutrients": "⚡️ Nutrient density on a plate! Everything your body needs in its most bioavailable form. #NutrientDense #AnimalBased"
        }
        
        caption = request.caption or captions.get(request.theme, "Carnivore lifestyle for optimal health! #Carnivore #Health")
        
        return {
            "image_url": image_url,
            "caption": caption,
            "hashtags": "#CarnivoreDiet #Keto #LowCarb #AnimalBased #Health #Wellness #Nutrition #RealFood",
            "theme": request.theme
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nutrients/{food_name}")
async def get_nutrients(food_name: str):
    """Get nutrient information for specific foods"""
    nutrients = nutrient_db.get_nutrient_info(food_name)
    
    if not nutrients:
        raise HTTPException(status_code=404, detail="Food not found in database")
    
    return {
        "food": food_name,
        "nutrients": nutrients,
        "health_benefits": get_food_benefits(food_name)
    }

def get_food_benefits(food_name: str) -> list:
    """Get health benefits for specific foods"""
    benefits = {
        "ribeye": [
            "Complete protein for muscle building",
            "Heme iron for energy production",
            "Zinc for immune function",
            "Creatine for brain and muscle health"
        ],
        "eggs": [
            "Perfect protein source",
            "Choline for brain health",
            "Vitamin D for immune function",
            "Lutein for eye health"
        ],
        "liver": [
            "Nature's multivitamin",
            "High in Vitamin A for vision",
            "Massive B12 for energy",
            "Copper for joint health"
        ]
    }
    
    return benefits.get(food_name.lower(), ["Rich in essential nutrients"])

@app.get("/api/winter-vitamin-guide")
async def winter_vitamin_guide():
    """Special guide for winter nutrition"""
    return {
        "title": "Winter Vitamin Protocol for Carnivores",
        "guide": diet_skill.explain_vitamin_d3_k2({}),
        "supplement_recommendations": [
            "Vitamin D3: 5000-10000 IU daily",
            "Vitamin K2 (MK-7): 100-200mcg daily",
            "Magnesium: 400mg before bed",
            "Cod Liver Oil: 1 tsp daily"
        ],
        "food_sources": [
            "Fatty fish (salmon, mackerel, sardines)",
            "Grass-fed butter and ghee",
            "Egg yolks from pasture-raised chickens",
            "Beef liver (once per week)"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
