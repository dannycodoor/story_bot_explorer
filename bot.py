import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Configure logging
logging.basicConfig(level=logging.INFO)

# Telegram Bot Token
API_TOKEN = 'YOUR_BOT_API_TOKEN_HERE'

# Function to fetch node info from API
def fetch_node_info(node_address):
    url = f"https://api.testnet.storyscan.app/validators/{node_address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Helper function to format large numbers
def format_number(value):
    return f"{int(float(value)):,}" if '.' in str(value) else f"{int(value):,}"

# Handler for /start command
async def send_welcome(message: types.Message):
    await message.answer("👋 Hello! Send me a validator address and I will fetch the node information for you.")

# Handler to process validator address input
async def get_node_info(message: types.Message):
    node_address = message.text
    node_info = fetch_node_info(node_address)

    if node_info:
        commission_rate = float(node_info['commission']['commission_rates']['rate'])
        max_commission_rate = float(node_info['commission']['commission_rates']['max_rate'])
        total_tokens = format_number(node_info.get('tokens', 'N/A'))
        delegator_shares = format_number(node_info.get('delegator_shares', 'N/A'))
        participation_rate = node_info.get('participation', {}).get('rate', 'N/A')
        window_uptime = node_info['uptime']['windowUptime']['uptime'] * 100
        validator_status = node_info.get('status', 'N/A')
        voting_power = node_info.get('votingPowerPercent', 0) * 100
        cumulative_share = node_info.get('cumulativeShare', 0) * 100

        response_text = (
            f"🌐 <b>Node Information</b> for <code>{node_address}</code>:\n\n"
            f"📇 <b>Operator Address:</b> <code>{node_info.get('operator_address', 'N/A')}</code>\n"
            f"⏳ <b>Unbonding Time:</b> {node_info.get('unbonding_time', 'N/A')}\n"
            f"💰 <b>Commission Rate:</b> {commission_rate:.2f}\n"
            f"📉 <b>Max Commission Rate:</b> {max_commission_rate:.2f}\n"
            f"🪙 <b>Total Tokens:</b> {total_tokens}\n"
            f"📊 <b>Delegator Shares:</b> {delegator_shares}\n"
            f"👥 <b>Participation Rate:</b> {participation_rate}\n"
            f"⚙️ <b>Window Uptime:</b> {window_uptime:.2f}%\n"
            f"🟢 <b>Validator Status:</b> {validator_status}\n"
            f"⚡️ <b>Voting Power:</b> {voting_power:.2f}%\n"
            f"📈 <b>Cumulative Share:</b> {cumulative_share:.2f}%"
        )
        await message.answer(response_text, parse_mode='HTML')
    else:
        await message.answer("⚠️ Error fetching node information. Please check the address and try again.")

# Main function to set up bot and start polling
async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Register handlers
    dp.message.register(send_welcome, Command(commands=["start"]))
    dp.message.register(get_node_info, lambda message: message.text.startswith("storyvaloper"))

    # Start polling
    await dp.start_polling(bot)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
