import click
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
import markdown
import os
import smtplib
import sys
from xai_sdk import Client
from xai_sdk.chat import user, system
from xai_sdk.tools import web_search, x_search, code_execution
import prompt
import schema
import preparer

DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))


def get_target_date():
    now = datetime.now()
    target_date = now if now.hour < 13 else now + timedelta(days=1)
    return target_date.strftime("%B %-d, %Y")


def get_current_time():
    # Return current time in PST
    return datetime.now(timezone(timedelta(hours=-8))).strftime("%H:%M:%S")

    def safe_int_cast(value, default=None):
        """
        Safely converts a value to an integer.

        :param value: The value to convert.
        :param default: The value to return if conversion fails (e.g., None, 0, etc.).
        :return: The integer value or the default value.
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            # Handle cases where the value cannot be converted (e.g., 'abc', None, etc.)
            return default


def init_xai():
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("XAI_API_KEY not found, exiting...")
        sys.exit(1)

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
        response_format=schema.StockAnalysisList,
    )
    return client, chat


def safe_int_cast(value, default=None):
    """
    Safely converts a value to an integer.

    :param value: The value to convert.
    :param default: The value to return if conversion fails (e.g., None, 0, etc.).
    :return: The integer value or the default value.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        # Handle cases where the value cannot be converted (e.g., 'abc', None, etc.)
        return default


def xapp(debug, email):
    VERBOSE = debug.verbose
    DEBUG = debug.enabled

    client, chat = init_xai()

    DATE = get_target_date()
    TIME = get_current_time()
    STOCK_COUNT = 5

    result = f"Stock sentiment analysis for {DATE} at {TIME}\n\n"

    PROMPT = prompt.get_primary_prompt(DATE, STOCK_COUNT)

    if DEBUG:
        PROMPT = debug.prompt

    # Output date time for logging
    print(f"# starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    chat.append(system(PROMPT))

    response = ""

    is_thinking = True
    for response, chunk in chat.stream():
        # View the server-side tool calls as they are being made in real-time
        for tool_call in chunk.tool_calls:
            if VERBOSE:
                print(
                    f"\nCalling tool: {tool_call.function.name} with arguments: {tool_call.function.arguments}"
                )
        if response.usage.reasoning_tokens and is_thinking:
            if VERBOSE:
                print(
                    f"\rThinking... ({response.usage.reasoning_tokens} tokens)",
                    end="",
                    flush=True,
                )
        if chunk.content and is_thinking:
            if VERBOSE:
                print("\n\nFinal Response:")
            is_thinking = False
        if chunk.content and not is_thinking:
            result += "".join(chunk.content)
            if VERBOSE:
                print(chunk.content, end="", flush=True)

    if VERBOSE:
        print("\n\nCitations:")
        print(response.citations)
        print("\n\nUsage:")
        print(response.usage)
        print(response.server_side_tool_usage)
        print("\n\nServer Side Tool Calls:")
        print(response.tool_calls)

    stock_analysis = schema.StockAnalysisList.model_validate_json(response.content)
    print(stock_analysis)
    with open(
        f"{DIR_SCRIPT}/daily/stock_analysis_{datetime.now().strftime('%Y%m%d.%H%M%S')}.json",
        "w",
    ) as f:
        f.write(stock_analysis.model_dump_json(indent=4))

    result += "\n"

    # Handle result
    print(result)
    with open(f"{os.getcwd()}/result.txt", "w") as f:
        f.write(result)

    # Calculate total token usage
    tokens = 0
    response_usage = str(response.usage)
    for usage_type in response_usage.splitlines():
        tokens += safe_int_cast(usage_type.split(":")[1].strip(), 0)

    with open(f"{os.getcwd()}/tokens_{tokens}.txt", "w") as f:
        f.write(str(tokens))

    print(f"used {tokens} tokens\n")

    # Import smtplib to send emails via Gmail
    if email.sender_email and email.sender_password and email.mailing_list:
        msg = EmailMessage()
        msg.set_content(result)  # Plain text version
        msg.add_alternative(preparer.get_html(DATE, stock_analysis), subtype="html")

        msg["Subject"] = f"Daily Stock Impact Report - {DATE}"
        msg["From"] = email.sender_email
        msg["To"] = email.mailing_list
        msg["CC"] = email.sender_email

        with smtplib.SMTP(email.smtp_host, email.smtp_port) as server:
            server.starttls()
            server.login(email.sender_email, email.sender_password)
            server.send_message(msg)
    else:
        print(
            f"warning: SENDER_EMAIL, SENDER_PASSWORD, or MAILING_LIST not found, unable to send email: {email}"
        )

    # Output date time for logging
    print(f"# done at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def test(debug, email):
    print(f"d={debug}")
    print(f"email={email}")


@click.command()
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Enable verbose mode"
)
@click.option(
    "--debug-prompt",
    "-dp",
    type=str,
    default=prompt.get_debug_prompt(),
    help="Set a debug prompt",
)
@click.option(
    "--sender-email",
    "-se",
    type=str,
    default="",
    help="Set a sender email",
)
@click.option(
    "--sender-password",
    "-sp",
    type=str,
    default="",
    help="Set a sender password",
)
@click.option(
    "--mailing-list",
    "-ml",
    type=str,
    default="",
    help="Set a mailing list",
)
def main(debug, verbose, debug_prompt, sender_email, sender_password, mailing_list):
    email = schema.Email(
        sender_email=sender_email,
        sender_password=sender_password,
        mailing_list=mailing_list,
    )
    debug = schema.Debug(
        enabled=debug,
        prompt=debug_prompt,
        verbose=verbose,
    )
    xapp(debug, email)


if __name__ == "__main__":
    main()
