import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # System Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    XAI_API_KEY = os.getenv('XAI_API_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    # Redis (Short-term Memory)
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    
    # Vector DB (Long-term Memory)
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', 'memory/vector_store.index')
    
    # Agent Configuration
    AGENTS = {
        'chatgpt': {
            'name': 'ChatGPT Agent',
            'model': 'gpt-4-turbo',  # Updated to real GPT-4 Turbo model
            'role': 'Fundamental Analysis',
            'weight': 1.0,
            'temperature': 0.7
        },
        'grok': {
            'name': 'Grok Agent',
            'model': 'grok-beta',  # Updated to real Grok model (verify with xAI docs)
            'role': 'Social Sentiment',
            'weight': 1.0,
            'temperature': 0.7
        },
        'gemini': {
            'name': 'Gemini Agent',
            'model': 'gemini-pro',  # Updated to real Gemini Pro model
            'role': 'Technical Analysis',
            'weight': 1.2, # Higher weight for technicals as per user req
            'temperature': 0.7
        },
        'machine': {
            'name': 'Machine Agent',
            'model': 'llama-3.1-finetuned',
            'model_path': os.getenv('MACHINE_MODEL_PATH', 'models/machine_finetuned.gguf'), # Path to fine-tuned model
            'role': 'Risk & Execution',
            'weight': 1.1,
            'temperature': 0.5 # Lower temp for execution logic
        }
    }
    
    # Consensus Parameters
    CONSENSUS_THRESHOLD = 0.70
    MAX_DEBATE_ROUNDS = 5
