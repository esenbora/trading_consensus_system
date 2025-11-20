import json
import os
from agents.base import BaseAgent
from config import Config
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

class ChatGPTAgent(BaseAgent):
    def __init__(self, name, model, role, weight, temperature):
        super().__init__(name, model, role, weight, temperature)
        api_key = Config.OPENAI_API_KEY
        if api_key:
            self.llm = ChatOpenAI(model=model, temperature=temperature, api_key=api_key)
        else:
            self.llm = None
            print(f"⚠️ {name}: OPENAI_API_KEY not found. Agent disabled.")

    def analyze(self, market_data):
        if not self.llm:
            return {"signal": "HOLD", "confidence": 0.0, "reasoning": "Agent disabled (Missing API Key)"}
            
        prompt = f"""
        Role: {self.role}
        Analyze the following market data: {json.dumps(market_data)}
        Provide a trading decision in JSON format with keys: signal (BUY/SELL/HOLD), confidence (0.0-1.0), reasoning.
        """
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            # Naive parsing, in production use OutputParsers
            content = response.content.strip()
            # Attempt to extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except Exception as e:
            return {"signal": "HOLD", "confidence": 0.0, "reasoning": f"Error: {str(e)}"}

    def debate(self, context, round_history):
        if not self.llm:
            return {"revised_signal": "HOLD", "revised_confidence": 0.0, "response": "Agent disabled."}
            
        prompt = f"""
        Role: {self.role}
        Context: {context}
        History: {json.dumps(round_history)}
        Critique the opinions and revise your stance if necessary.
        Return JSON: revised_signal, revised_confidence, response.
        """
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except Exception as e:
            return {"revised_signal": "HOLD", "revised_confidence": 0.0, "response": f"Error: {str(e)}"}

class GrokAgent(BaseAgent):
    def __init__(self, name, model, role, weight, temperature):
        super().__init__(name, model, role, weight, temperature)
        api_key = Config.XAI_API_KEY
        if api_key:
            # Assuming xAI compatible with OpenAI client
            self.llm = ChatOpenAI(
                model=model, 
                temperature=temperature, 
                api_key=api_key,
                base_url="https://api.x.ai/v1" 
            )
        else:
            self.llm = None
            print(f"⚠️ {name}: XAI_API_KEY not found. Agent disabled.")

    def analyze(self, market_data):
        if not self.llm:
            return {"signal": "HOLD", "confidence": 0.0, "reasoning": "Agent disabled (Missing API Key)"}
        
        # Similar logic to ChatGPT but prompt tailored for Social Sentiment
        prompt = f"""
        Role: {self.role}
        Focus on social sentiment and hype in this data: {json.dumps(market_data)}
        Provide JSON: signal, confidence, reasoning.
        """
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except Exception as e:
            return {"signal": "HOLD", "confidence": 0.0, "reasoning": f"Error: {str(e)}"}

    def debate(self, context, round_history):
        if not self.llm:
            return {"revised_signal": "HOLD", "revised_confidence": 0.0, "response": "Agent disabled."}
            
        prompt = f"""
        Role: {self.role}
        Context: {context}
        History: {json.dumps(round_history)}
        Debate based on social momentum.
        Return JSON: revised_signal, revised_confidence, response.
        """
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except Exception as e:
            return {"revised_signal": "HOLD", "revised_confidence": 0.0, "response": f"Error: {str(e)}"}

class GeminiAgent(BaseAgent):
    def __init__(self, name, model, role, weight, temperature):
        super().__init__(name, model, role, weight, temperature)
        api_key = Config.GOOGLE_API_KEY
        if api_key:
            self.llm = ChatGoogleGenerativeAI(model=model, temperature=temperature, google_api_key=api_key)
        else:
            self.llm = None
            print(f"⚠️ {name}: GOOGLE_API_KEY not found. Agent disabled.")

    def analyze(self, market_data):
        if not self.llm:
            return {"signal": "HOLD", "confidence": 0.0, "reasoning": "Agent disabled (Missing API Key)"}
            
        prompt = f"""
        Role: {self.role}
        Focus on technical indicators in this data: {json.dumps(market_data)}
        Provide JSON: signal, confidence, reasoning.
        """
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except Exception as e:
            return {"signal": "HOLD", "confidence": 0.0, "reasoning": f"Error: {str(e)}"}

    def debate(self, context, round_history):
        if not self.llm:
            return {"revised_signal": "HOLD", "revised_confidence": 0.0, "response": "Agent disabled."}
            
        prompt = f"""
        Role: {self.role}
        Context: {context}
        History: {json.dumps(round_history)}
        Debate based on technicals.
        Return JSON: revised_signal, revised_confidence, response.
        """
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            return json.loads(content)
        except Exception as e:
            return {"revised_signal": "HOLD", "revised_confidence": 0.0, "response": f"Error: {str(e)}"}

class MachineAgent(BaseAgent):
    def __init__(self, name, model, role, weight, temperature):
        super().__init__(name, model, role, weight, temperature)
        self.model_path = Config.AGENTS['machine'].get('model_path')
        self.model_loaded = False
        
        if os.path.exists(self.model_path):
            print(f"✅ {name}: Found fine-tuned model at {self.model_path}. Loading...")
            # Placeholder for actual model loading (e.g., llama_cpp or transformers)
            # self.llm = Llama(model_path=self.model_path, ...)
            self.model_loaded = True
        else:
            print(f"⚠️ {name}: Fine-tuned model not found at {self.model_path}.")
            print("   Please follow 'fine_tuning_guide.md' to train and place the model.")

    def analyze(self, market_data):
        if not self.model_loaded:
            return {
                "signal": "HOLD", 
                "confidence": 0.0, 
                "reasoning": "Model not loaded. Please fine-tune Llama 3.1 and save to 'models/machine_finetuned.gguf'."
            }
        
        # Real inference logic would go here
        return {
            "signal": "BUY", # Mock for now until model is present
            "confidence": 0.9,
            "reasoning": "Model inference result (Simulated)"
        }

    def debate(self, context, round_history):
        if not self.model_loaded:
            return {"revised_signal": "HOLD", "revised_confidence": 0.0, "response": "Model not loaded."}
            
        return {
            "revised_signal": "BUY",
            "revised_confidence": 0.95,
            "response": "Model debate inference result (Simulated)"
        }
