from config import Config
from agents import ChatGPTAgent, GrokAgent, GeminiAgent, MachineAgent
from memory.rag_engine import RAGEngine
from data.feed import DataFeed

class Orchestrator:
    def __init__(self):
        self.agents = self._initialize_agents()
        self.rag_engine = RAGEngine()
        self.data_feed = DataFeed()
        self.consensus_threshold = Config.CONSENSUS_THRESHOLD
        self.max_rounds = Config.MAX_DEBATE_ROUNDS

    def _initialize_agents(self):
        agent_map = {
            'chatgpt': ChatGPTAgent,
            'grok': GrokAgent,
            'gemini': GeminiAgent,
            'machine': MachineAgent
        }
        
        agents = []
        for key, conf in Config.AGENTS.items():
            agent_cls = agent_map.get(key)
            if agent_cls:
                agents.append(agent_cls(
                    name=conf['name'],
                    model=conf['model'],
                    role=conf['role'],
                    weight=conf['weight'],
                    temperature=conf['temperature']
                ))
        return agents

    def run_debate(self, ticker):
        try:
            # 1. Gather Market Data
            try:
                market_data = self.data_feed.get_market_data(ticker)
                news = self.data_feed.get_news(ticker)
                market_data['news'] = news
            except Exception as e:
                print(f"Warning: Error fetching market data: {e}")
                return {"error": "Failed to fetch market data", "details": str(e)}

            # 2. Retrieve Context (RAG)
            try:
                historical_context = self.rag_engine.get_context(ticker)
            except Exception as e:
                print(f"Warning: Error retrieving historical context: {e}")
                historical_context = "No historical context available."

            # 3. Initial Analysis Round
            initial_opinions = []
            for agent in self.agents:
                try:
                    opinion = agent.analyze(market_data)
                    initial_opinions.append({
                        "agent": agent.name,
                        "weight": agent.weight,
                        "opinion": opinion
                    })
                except Exception as e:
                    print(f"Warning: {agent.name} failed initial analysis: {e}")
                    # Provide default HOLD opinion for failed agent
                    initial_opinions.append({
                        "agent": agent.name,
                        "weight": agent.weight,
                        "opinion": {
                            "signal": "HOLD",
                            "confidence": 0.0,
                            "reasoning": f"Agent error: {str(e)}"
                        }
                    })

            if not initial_opinions:
                return {"error": "All agents failed to provide initial analysis"}

            # 4. Debate Loop
            round_history = []
            current_opinions = initial_opinions

            for round_num in range(self.max_rounds):
                round_results = []
                # Include historical context in the debate context
                context = f"{historical_context}\n\n{self._summarize_context(current_opinions)}"

                # Check for consensus
                decision, confidence = self._calculate_consensus(current_opinions)
                if confidence >= self.consensus_threshold:
                    break

                # If no consensus, debate continues
                for agent in self.agents:
                    try:
                        others_history = [h for h in round_history if h['agent'] != agent.name]
                        response = agent.debate(context, others_history)

                        round_results.append({
                            "agent": agent.name,
                            "weight": agent.weight,
                            "opinion": {
                                "signal": response['revised_signal'],
                                "confidence": response['revised_confidence'],
                                "reasoning": response['response']
                            }
                        })
                    except Exception as e:
                        print(f"Warning: {agent.name} failed debate round {round_num + 1}: {e}")
                        # Keep previous opinion if debate fails
                        prev_opinion = next((op for op in current_opinions if op['agent'] == agent.name), None)
                        if prev_opinion:
                            round_results.append(prev_opinion)

                if not round_results:
                    print("Warning: All agents failed debate round, using initial opinions")
                    break

                current_opinions = round_results
                round_history.extend(round_results)

            # 5. Final Decision
            final_decision, final_confidence = self._calculate_consensus(current_opinions)

            # 6. Store in Memory via RAG Engine
            discussion_log = {
                "ticker": ticker,
                "rounds": round_num + 1,
                "decision": final_decision,
                "confidence": final_confidence,
                "history": round_history,
                "market_data": market_data
            }

            try:
                self.rag_engine.store_experience(ticker, discussion_log)
            except Exception as e:
                print(f"Warning: Failed to store experience in memory: {e}")

            return discussion_log

        except Exception as e:
            print(f"Critical error in run_debate: {e}")
            return {"error": "Critical system error", "details": str(e)}

    def _summarize_context(self, opinions):
        summary = "Current Opinions:\n"
        for op in opinions:
            summary += f"{op['agent']}: {op['opinion']['signal']} (Conf: {op['opinion']['confidence']})\n"
        return summary

    def _calculate_consensus(self, opinions):
        scores = {"BUY": 0.0, "SELL": 0.0, "HOLD": 0.0}
        total_weight = 0.0
        
        for op in opinions:
            weight = op['weight']
            signal = op['opinion']['signal']
            confidence = op['opinion']['confidence']
            
            scores[signal] += weight * confidence
            total_weight += weight
            
        if total_weight == 0:
            return "HOLD", 0.0
            
        final_scores = {k: v / total_weight for k, v in scores.items()}
        best_decision = max(final_scores, key=final_scores.get)
        best_confidence = final_scores[best_decision]
        
        return best_decision, best_confidence
