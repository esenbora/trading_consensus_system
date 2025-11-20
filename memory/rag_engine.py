from memory.redis_client import RedisClient
from memory.vector_store import VectorStore
import json

class RAGEngine:
    def __init__(self):
        self.redis = RedisClient()
        self.vector_store = VectorStore()

    def get_context(self, ticker):
        """
        Retrieves relevant context for the debate.
        Combines short-term memory (Redis) and long-term memory (Vector Store).
        """
        context = []
        
        # 1. Short-term: Recent discussion for this ticker
        recent = self.redis.get_discussion(ticker)
        if recent:
            context.append(f"Recent Discussion (Last 1h): {recent['decision']} with confidence {recent['confidence']}")

        # 2. Long-term: Similar past situations (Mock embedding for now)
        # In real app, we'd embed the current market state
        mock_query_vector = [0.1] * 768 
        similar_memories = self.vector_store.search_memory(mock_query_vector)
        
        if similar_memories:
            context.append("Similar Past Situations:")
            for mem in similar_memories:
                context.append(f"- {mem['context']} (Similarity: {mem['distance']:.2f})")
                
        return "\n".join(context)

    def store_experience(self, ticker, discussion_log):
        """
        Stores the experience in both short-term and long-term memory.
        """
        # Short-term
        self.redis.store_discussion(ticker, discussion_log)
        
        # Long-term
        # Create a text summary to embed
        summary = f"Ticker: {ticker}, Decision: {discussion_log['decision']}, Confidence: {discussion_log['confidence']}"
        # Mock embedding
        mock_vector = [0.1] * 768 
        self.vector_store.add_memory(mock_vector, summary)
