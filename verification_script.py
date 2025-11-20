import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from orchestrator import Orchestrator
from utils.telegram_bot import TelegramBot
import json

def run_verification():
    print("Starting System Verification...")
    
    # 1. Initialize Orchestrator
    try:
        orchestrator = Orchestrator()
        print("✅ Orchestrator Initialized")
    except Exception as e:
        print(f"❌ Orchestrator Initialization Failed: {e}")
        return

    # 2. Initialize Telegram Bot
    bot = TelegramBot()
    print("✅ Telegram Bot Initialized")

    # 3. Run Debate for a Test Ticker
    ticker = "BTC-USD"
    print(f"\nRunning Debate for {ticker}...")
    
    try:
        result = orchestrator.run_debate(ticker)
        print("✅ Debate Completed")
        
        # 4. Print Results
        print("\n--- Debate Results ---")
        print(f"Decision: {result['decision']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Rounds: {result['rounds']}")
        
        print("\n--- Debate History ---")
        for round_data in result['history']:
            print(f"[{round_data['agent']}] -> {round_data['opinion']['signal']} (Conf: {round_data['opinion']['confidence']})")
            print(f"   Reasoning: {round_data['opinion']['reasoning'][:100]}...")
            
        # 5. Send Alert
        if result['confidence'] > 0.7:
            bot.send_alert(f"Trade Signal: {result['decision']} {ticker} (Conf: {result['confidence']:.2f})")
        else:
            print("No high confidence signal generated.")
            
    except Exception as e:
        print(f"❌ Debate Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_verification()
