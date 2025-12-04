# 🥩 CarnivoreAI Coach 🤖

An intelligent chatbot system for carnivore and ketogenic diet advice, using multiple AI technologies and programming languages.

## ✨ Features

### 🤖 AI Chatbot
- Natural conversations about carnivore/keto diets
- Personalized meal suggestions
- Nutrient information and benefits
- Foods to avoid guidance
- Winter vitamin D3/K2 advice

### 🎨 Image Generation
- DALL-E generated motivational images
- Nutrient infographics
- Food photography
- Transformation visuals

### 📱 Multi-Platform
- Web interface
- Instagram automation
- REST API for integration
- Multi-language backend (Python + C#)

### 🏗️ Tech Stack
- **AI Services**: Azure OpenAI, OpenAI API
- **Orchestration**: Semantic Kernel (Python & C#)
- **Backend**: Python (FastAPI), C# (.NET)
- **Frontend**: HTML/CSS/JavaScript
- **DevOps**: Docker, GitHub Actions
- **Social**: Instagram API automation

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- .NET 8.0 SDK
- Docker & Docker Compose
- OpenAI/Azure OpenAI API keys
- Instagram account (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/carnivore-ai-coach.git
cd carnivore-ai-coach

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Method 1: Docker (Recommended)
docker-compose up --build

# Method 2: Manual setup

# Python backend
cd backend-python
pip install -r requirements.txt
python app.py

# C# backend (separate terminal)
cd backend-csharp
dotnet restore
dotnet run

# Instagram bot (optional)
cd instagram-bot
pip install -r requirements.txt
python instagram_handler.py
