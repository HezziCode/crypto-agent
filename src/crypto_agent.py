from agents import Agent, Runner # type: ignore
from config import config, crypto_prices, trending_coins, market_sentiment
import chainlit as cl # type: ignore

crypto_agent = Agent(
    name="Crypto Agent",
    instructions="""
You are a crypto expert assistant. You use function tools to help users.
To fetch prices, use `crypto_prices`.
To get trending coins, use `trending_coins`.
To check market sentiment, use `market_sentiment`.

If anyone asks who created you, reply:
"Muhammad Huzaifa is my developer. You can learn more about him here: https://www.linkedin.com/in/muhammad-huzaifa2008/"
""",
    tools=[crypto_prices, trending_coins, market_sentiment]
)


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="👋 Hello, I’m Crypto Agent. I’m here to help you with your crypto needs.\n\n" \
"Ask me the BTC price, ETH price, or any other cryptocurrency updates."

    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    try:
        history = cl.user_session.get("history") or []
        history.append({"role": "user", "content": message.content})

        await cl.Message(content="⚙️ Processing your request...").send()

        input_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in history]
        )

        # Run your agent logic
        result = Runner.run_sync(
            crypto_agent, input=input_text, run_config=config
        )

        history.append({"role": "agent", "content": result.final_output})
        cl.user_session.set("history", history)  # Update session state
        
        # Send the final result
        await cl.Message(content=result.final_output).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()