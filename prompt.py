DEFAULT_DEBUG_PROMPT = """
    Tell me a simple joke. Use markdown formatting to format the joke to emphasize the punchline.
"""

PRIMARY_PROMPT = """
GOAL: 
Generate a Daily Stock Impact Report for {DATE}. 

PROCESS: 
Scan recent news and X posts for major events impacting stocks. Identify the top {STOCK_COUNT} stocks with significant sentiment shifts. 

For each stock, provide:
• Details: Ticker Symbol, Full Company Name, Current Price (fetch real-time via code_execution with polygon), Market Cap, Sector/Industry, 52-Week High/Low, P/E Ratio, Volume, Recent Dividend Info.
• Impact Theory: Describe the event/news, its economic implications, market psychology effects, historical parallels, and 2 analogies.
• News Impact Analysis: Bullish or Bearish outlook, with estimated price impact percentage and reasoning (use web_search for news, x_keyword_search or x_semantic_search for X sentiment, limit:20, mode:Latest).
• Potential Profit/Risks: Opportunities for long/short positions with % gains/losses, plus key risks.
• Confidence Rating: A (highest), B (high), or C (moderate), with justification.

Be thorough, use tools in parallel for efficiency. Return the result as a JSON object.
"""


def get_primary_prompt(date: str, stock_count: int) -> str:
    return PRIMARY_PROMPT.format(DATE=date, STOCK_COUNT=stock_count).strip()


def get_debug_prompt() -> str:
    return DEFAULT_DEBUG_PROMPT.strip()
