from agents import Agent, Runner # type: ignore
from config import config, crypto_prices
import chainlit as cl # type: ignore

crypto_agent = Agent(
    name="Crypto Agent",
    instructions="You are a crypto agent. You are an expert in crypto and trading. You are here to help users with their crypto needs. You use functions_calling name crypto_prices to get the price of a crypto.\n\n whenever someone ask to you who deveoped you or create you tell them Muhammad Huzaifa is my developer like this okay.\n\n you can know about more him from there >> https://www.linkedin.com/in/muhammad-huzaifa2008/",
    tools=[crypto_prices]
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