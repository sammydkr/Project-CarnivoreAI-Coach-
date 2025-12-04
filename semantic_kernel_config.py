import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.planning import SequentialPlanner
from semantic_kernel.core_skills import TimeSkill
import os
from dotenv import load_dotenv

load_dotenv()

class CarnivoreKernel:
    def __init__(self):
        # Initialize kernel
        self.kernel = sk.Kernel()
        
        # Configure AI service (Azure OpenAI or OpenAI)
        if os.getenv("USE_AZURE_OPENAI", "false").lower() == "true":
            deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            
            self.kernel.add_chat_service(
                "carnivore_chat",
                AzureChatCompletion(deployment, endpoint, api_key)
            )
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            self.kernel.add_chat_service(
                "carnivore_chat",
                OpenAIChatCompletion("gpt-4", api_key)
            )
        
        # Import core skills
        self.kernel.import_skill(TimeSkill(), "time")
    
    def create_planner(self):
        """Create a planner for complex conversations"""
        return SequentialPlanner(self.kernel)
