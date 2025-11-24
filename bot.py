import os
import uuid
import httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL", "https://example.com")
API_BACKEND = os.getenv("API_BACKEND", "http://web:8000")  # internal docker network

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

CONSENT_TEXT = (
    "This is an authorized security test. Clicking the link below will log your IP address, "
    "browser headers, and approximate city-level geolocation for testing purposes.\n\n"
    "Do you consent to proceed?"
)

@dp.message(commands=["start", "help"])
async def cmd_start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="I CONSENT", callback_data="consent_yes")
    kb.button(text="Cancel", callback_data="consent_no")
    await message.reply(CONSENT_TEXT, reply_markup=kb.as_markup())

@dp.callback_query(F.data == "consent_no")
async def handle_no(call: types.CallbackQuery):
    await call.message.edit_text("Consent not given. Test cancelled.")
    await call.answer()

@dp.callback_query(F.data == "consent_yes")
async def handle_yes(call: types.CallbackQuery):
    # create session record via backend API (backend will create session and return session_id)
    payload = {
        "telegram_user_id": call.from_user.id,
        "telegram_username": call.from_user.username,
        "consent": True
    }
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.post(f"{API_BACKEND}/api/sessions", json=payload)
            r.raise_for_status()
            data = r.json()
            session_id = data["session_id"]
        except Exception as e:
            await call.message.edit_text("Failed to create test session. Contact admin.")
            await call.answer()
            return

    test_url = f"{BASE_URL}/test/{session_id}"
    resp_text = (

        "Consent recorded ✅\n\n"

        f"Please click this link to complete the test (this will log your IP & browser headers):\n\n"

        f"{test_url}\n\n"

        "You will see a confirmation page after visiting. If you want your data deleted, contact the test owner."

    )
    await call.message.edit_text(resp_text)
    await call.answer()

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
