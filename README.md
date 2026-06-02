# llm-resilience-guard 🛡️

A lightweight, developer-friendly Python wrapper designed to make OpenAI API integration resilient and cost-aware. It natively injects **exponential backoff retry mechanisms** and **granular cost tracking** into production pipelines with a single line of code.

## ✨ Key Features
*   **Automatic Error Recovery:** Seamlessly handles OpenAI API rate limits, network timeouts, and transient server errors using smart exponential backoff.
*   **Granular Cost Auditing:** Calculates real-time financial metrics for each API call based on token usage and model-specific pricing tiers.
*   **Zero-Overhead Integration:** Pure Python decorator design. No complex configurations required—just wrap your existing functions.
*   **Structured Logging:** Ready for production monitoring stacks (ELK, Datadog, Grafana).

## 📦 Installation (Development Stage)
Clone the repository and install the development dependencies:
```bash
git clone https://github.com
cd llm-resilience-guard
pip install -r requirements.txt
