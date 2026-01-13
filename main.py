import os
from datetime import datetime, timedelta
import sys
from xai_sdk import Client
from xai_sdk.chat import user, system
from xai_sdk.tools import web_search, x_search, code_execution

api_key = os.getenv('XAI_API_KEY')
if not api_key:
    print("XAI_API_KEY not found, exiting...")
    import sys
    sys.exit(1)

now = datetime.now()
target_date = now if now.hour < 13 else now + timedelta(days=1)
DATE = target_date.strftime("%B %-d, %Y")
STOCK_COUNT = 5

print(f"Stock sentiment analysis for {DATE}")
print()

client = Client(api_key=f"{api_key}")
chat = client.chat.create(
    model="grok-4-1-fast",  # reasoning model
    # All server-side tools active
    tools=[
        web_search(),
        x_search(),
        code_execution(),
    ],
    include=["verbose_streaming"],
)

PROMPT = f"""

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

Be thorough, use tools in parallel for efficiency, and format exactly as a numbered list.

"""

chat.append(user(PROMPT))

is_thinking = True
for response, chunk in chat.stream():
    # View the server-side tool calls as they are being made in real-time
    for tool_call in chunk.tool_calls:
        print(f"\nCalling tool: {tool_call.function.name} with arguments: {tool_call.function.arguments}")
    if response.usage.reasoning_tokens and is_thinking:
        print(f"\rThinking... ({response.usage.reasoning_tokens} tokens)", end="", flush=True)
    if chunk.content and is_thinking:
        print("\n\nFinal Response:")
        is_thinking = False
    if chunk.content and not is_thinking:
        print(chunk.content, end="", flush=True)

print("\n\nCitations:")
print(response.citations)
print("\n\nUsage:")
print(response.usage)
print(response.server_side_tool_usage)
print("\n\nServer Side Tool Calls:")
print(response.tool_calls)
