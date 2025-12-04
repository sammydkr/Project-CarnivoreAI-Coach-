import openai
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO
import base64

load_dotenv()

class CarnivoreImageGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_health_image(self, theme: str) -> str:
        """Generate motivational carnivore/keto images"""
        
        prompts = {
            "motivation": "A vibrant, energetic person feeling healthy and strong, surrounded by delicious carnivore foods like steak and eggs, bright colors, motivational",
            "food": "Beautiful photography of carnivore diet foods: ribeye steak with butter, crispy bacon, eggs, salmon, artistic food photography, high quality",
            "before_after": "Dramatic transformation showing someone going from unhealthy to vibrant health, side by side comparison, inspiring",
            "nutrients": "Creative visualization of nutrients from meat entering the body, showing energy and health benefits, scientific but beautiful"
        }
        
        prompt = prompts.get(theme, prompts["motivation"])
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=f"{prompt}. Health, wellness, carnivore diet, ketogenic lifestyle.",
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            return image_url
            
        except Exception as e:
            print(f"Image generation failed: {e}")
            # Fallback to a placeholder or local image
            return "https://via.placeholder.com/1024x1024/FF6B35/FFFFFF?text=Carnivore+Health"
    
    def create_nutrient_infographic(self, food_data: dict) -> str:
        """Create an infographic showing nutrient density"""
        # This would use PIL or another library to generate images
        # For now, return a placeholder
        return self.generate_health_image("nutrients")
