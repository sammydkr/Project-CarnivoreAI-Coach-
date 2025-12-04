import os
import json
import schedule
import time
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import openai
from dotenv import load_dotenv
import requests

load_dotenv()

class InstagramCarnivoreBot:
    def __init__(self):
        self.client = Client()
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.hashtags = [
            "#CarnivoreDiet", "#Carnivore", "#Keto", "#LowCarb",
            "#AnimalBased", "#MeatHeals", "#Steak", "#LCHF",
            "#ZeroCarb", "#CarnivoreLifestyle", "#Health"
        ]
    
    def login(self):
        """Login to Instagram"""
        try:
            self.client.login(
                username=os.getenv("INSTAGRAM_USERNAME"),
                password=os.getenv("INSTAGRAM_PASSWORD")
            )
            print("✅ Logged in to Instagram successfully")
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def generate_daily_post(self):
        """Generate a daily carnivore-related post"""
        themes = [
            "motivational monday",
            "nutrition tuesday", 
            "recipe wednesday",
            "transformation thursday",
            "faq friday",
            "science saturday",
            "sunday meal prep"
        ]
        
        day = datetime.now().weekday()
        theme = themes[day]
        
        # Generate post content using OpenAI
        prompt = f"""
        Create an engaging Instagram post about the carnivore diet for {theme}.
        Include:
        1. A catchy title
        2. 2-3 key points about carnivore benefits
        3. A call to action
        4. Relevant emojis
        
        Theme: {theme}
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a carnivore diet expert creating social media content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        caption = response.choices[0].message.content
        caption += f"\n\n{''.join(self.hashtags[:7])}"
        
        return caption
    
    def generate_image_for_post(self, theme: str):
        """Generate image using DALL-E or use local library"""
        image_prompts = {
            "motivational monday": "Strong healthy person surrounded by carnivore foods, energetic, vibrant colors, inspirational",
            "nutrition tuesday": "Beautiful infographic showing nutrient density of meat vs plants, scientific, clear",
            "recipe wednesday": "Delicious looking steak with butter, perfect sear, food photography, mouth-watering",
            "transformation thursday": "Before and after transformation showing health improvement, side by side",
            "science saturday": "Scientific diagram showing benefits of carnivore diet on human body, educational"
        }
        
        prompt = image_prompts.get(theme, "Healthy person enjoying carnivore diet foods")
        
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            return response.data[0].url
        except:
            # Fallback to local images or templates
            return None
    
    def post_to_instagram(self, caption: str, image_url: str = None):
        """Post to Instagram"""
        try:
            if image_url:
                # Download image
                response = requests.get(image_url)
                image_path = "temp_post.jpg"
                with open(image_path, "wb") as f:
                    f.write(response.content)
                
                # Upload to Instagram
                self.client.photo_upload(
                    path=image_path,
                    caption=caption
                )
                print("✅ Posted to Instagram successfully")
                
                # Clean up
                os.remove(image_path)
            else:
                # Post without image (carousel or video would be similar)
                print("⚠️ No image to post")
            
            return True
            
        except Exception as e:
            print(f"❌ Post failed: {e}")
            return False
    
    def respond_to_comments(self):
        """Auto-respond to comments using AI"""
        # Get recent posts
        user_id = self.client.user_id
        media = self.client.user_medias(user_id, amount=5)
        
        for post in media:
            comments = self.client.media_comments(post.id, amount=20)
            
            for comment in comments:
                if not comment.replied:
                    # Generate AI response
                    ai_response = self.generate_comment_response(comment.text)
                    
                    # Reply to comment
                    self.client.media_comment(post.id, ai_response, replied_to_comment_id=comment.id)
                    print(f"✅ Replied to comment: {comment.text[:50]}...")
    
    def generate_comment_response(self, comment_text: str) -> str:
        """Generate AI response to comments"""
        prompt = f"""
        A follower commented on our carnivore diet post: "{comment_text}"
        
        Respond helpfully and positively. Keep it under 150 characters.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful carnivore diet coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        return response.choices[0].message.content

def main():
    bot = InstagramCarnivoreBot()
    
    if bot.login():
        # Schedule daily posts
        schedule.every().day.at("09:00").do(
            lambda: bot.post_daily_content()
        )
        
        # Schedule comment responses (every 2 hours)
        schedule.every(2).hours.do(bot.respond_to_comments)
        
        print("🤖 Instagram bot running...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    main()
