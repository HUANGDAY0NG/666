import time
import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional
from openai import OpenAI, OpenAIError

# Configure structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LLM-Resilience-Guard")

# Estimated pricing mapping per 1k tokens (Example rates, can be updated)
PRICING_MODEL = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4-turbo": {"input": 0.010, "output": 0.030},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
}

def track_cost_and_retry(max_retries: int = 3, initial_delay: float = 2.0) -> Callable:
    """
    A decorator for OpenAI API calls that provides automatic exponential backoff retries,
    error logging, and granular token/cost tracking.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            delay = initial_delay
            model_used = kwargs.get("model", "unknown")

            while retries <= max_retries:
                try:
                    start_time = time.time()
                    # Execute the actual OpenAI API call
                    response = func(*args, **kwargs)
                    duration = time.time() - start_time

                    # Parse token usage and calculate costs
                    if hasattr(response, 'usage') and response.usage:
                        prompt_tokens = response.usage.prompt_tokens
                        completion_tokens = response.usage.completion_tokens
                        total_tokens = response.usage.total_tokens

                        # Calculate estimated cost
                        rates = PRICING_MODEL.get(model_used, {"input": 0.0, "output": 0.0})
                        estimated_cost = ((prompt_tokens / 1000) * rates["input"]) + ((completion_tokens / 1000) * rates["output"])

                        logger.info(
                            f"SUCCESS | Model: {model_used} | Latency: {duration:.2f}s | "
                            f"Tokens: {total_tokens} (Prompt: {prompt_tokens}, Completion: {completion_tokens}) | "
                            f"Est. Cost: ${estimated_cost:.5f}"
                        )
                    else:
                        logger.info(f"SUCCESS | Latency: {duration:.2f}s (Token usage info unavailable)")

                    return response

                except OpenAIError as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"FAILED | Max retries ({max_retries}) reached. Error: {e}")
                        raise e

                    logger.warning(
                        f"RETRYING | OpenAI API Error caught: {e}. "
                        f"Attempt {retries}/{max_retries}. Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff

        return wrapper
    return decorator

# Quick test setup to verify imports are clean
if __name__ == "__main__":
    print("--------------------------------------------------")
    print("🚀 llm-resilience-guard initialized successfully!")
    print("Please check README.md to see how to use this in production.")
    print("--------------------------------------------------")
