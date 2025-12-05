import asyncio
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


# ==================== KONFIGURATSIYA ====================
@dataclass
class BotConfig:
    """Bot sozlamalari"""
    TOKEN: str = "8257163432:AAGJUgG_vJ_kwGUy1iJccNON4Yy0wTnv4r8"  # Bu yerga tokenni kiriting
    ADMIN_ID: int = 7782143104  # Bu yerga admin ID sini kiriting (o'z Telegram ID)
    ECOTRACK_URL: str = "https://ecotrack-ny80.onrender.com"

config = BotConfig()


# ==================== FSM HOLATLAR ====================
class AddPersonStates(StatesGroup):
    """Odam qo'shish uchun holatlar"""
    waiting_for_name = State()   # Ism kutilmoqda
    waiting_for_phone = State()  # Telefon raqam kutilmoqda


# ==================== KLAVIATURALAR ====================
def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Asosiy menyu klaviaturasini qaytaradi
    
    Returns:
        ReplyKeyboardMarkup: Asosiy menyu tugmalari
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Platforma link")],
            [KeyboardButton(text="➕ Odam qo'shishni yozish")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Menyudan tanlang..."
    )
    return keyboard


# ==================== GLOBAL MA'LUMOTLAR ====================
# Foydalanuvchi ma'lumotlarini vaqtincha saqlash
user_data_storage = {}


# ==================== LOGGING SOZLASH ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== YORDAMCHI FUNKSIYALAR ====================
async def notify_admin(bot: Bot, user: dict, person_data: dict, count: int):
    """
    Adminga yangi odam qo'shilganligi haqida xabar yuborish
    
    Args:
        bot: Bot instance
        user: Foydalanuvchi ma'lumotlari (from_user)
        person_data: Qo'shilgan odam ma'lumotlari
        count: Shu foydalanuvchi qo'shgan odamlar soni
    """
    try:
        # Foydalanuvchi haqida ma'lumot
        user_info = f"@{user.username}" if user.username else f"ID: {user.id}"
        user_full_name = user.full_name or "Noma'lum"
        
        # Vaqt
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        # Admin uchun xabar
        admin_message = (
            "🆕 <b>YANGI ODAM QO'SHILDI!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 <b>Qo'shgan foydalanuvchi:</b>\n"
            f"   • Ism: {user_full_name}\n"
            f"   • Username: {user_info}\n\n"
            f"📋 <b>Qo'shilgan odam:</b>\n"
            f"   • Ism: {person_data['name']}\n"
            f"   • Telefon: {person_data['phone']}\n\n"
            f"📊 <b>Statistika:</b>\n"
            f"   • Bu foydalanuvchi bugun qo'shgan: {count} ta\n\n"
            f"🕐 <b>Vaqt:</b> {current_time}"
        )
        
        await bot.send_message(
            chat_id=config.ADMIN_ID,
            text=admin_message,
            parse_mode="HTML"
        )
        
        logger.info(f"Adminga xabar yuborildi: {user_full_name} odam qo'shdi")
        
    except Exception as e:
        logger.error(f"Adminga xabar yuborishda xatolik: {e}")


# ==================== HANDLERLAR ====================
# Router yaratish
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start komandasi handleri
    Botni ishga tushirganda chiqadigan xabar
    
    Args:
        message: Foydalanuvchi xabari
    """
    try:
        welcome_text = (
            "Assalomu alaykum! EcoTrack botga xush kelibsiz 👋\n"
            "Bugun platformaga nechta odam qo'shdingiz?"
        )
        
        await message.answer(
            text=welcome_text,
            reply_markup=get_main_menu()
        )
        
        logger.info(f"Foydalanuvchi {message.from_user.id} botni ishga tushirdi")
        
    except Exception as e:
        logger.error(f"Start komandasi xatosi: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")


@router.message(F.text == "🌐 Platforma link")
async def send_platform_link(message: Message):
    """
    Platforma linkini yuborish
    
    Args:
        message: Foydalanuvchi xabari
    """
    try:
        link_text = (
            f"🌐 EcoTrack rasmiy platformasi:\n"
            f"{config.ECOTRACK_URL}"
        )
        
        await message.answer(link_text)
        logger.info(f"Foydalanuvchi {message.from_user.id} ga link yuborildi")
        
    except Exception as e:
        logger.error(f"Link yuborishda xatolik: {e}")
        await message.answer("Link yuborishda xatolik yuz berdi.")


@router.message(F.text == "➕ Odam qo'shishni yozish")
async def start_adding_person(message: Message, state: FSMContext):
    """
    Odam qo'shishni boshlash
    FSM holatiga o'tkazish
    
    Args:
        message: Foydalanuvchi xabari
        state: FSM holati
    """
    try:
        await message.answer(
            "👤 Iltimos, Nechta odam qo'shdingiz? platformaga qo'shgan odamlar sonini kiriting. ",
            reply_markup=get_main_menu()
        )
        await state.set_state(AddPersonStates.waiting_for_name)
        logger.info(f"Foydalanuvchi {message.from_user.id} odam qo'shishni boshladi")
        
    except Exception as e:
        logger.error(f"Odam qo'shishni boshlashda xatolik: {e}")
        await message.answer("Xatolik yuz berdi. Qaytadan urinib ko'ring.")


@router.message(AddPersonStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """
    Ism qabul qilish va telefon so'rash
    
    Args:
        message: Foydalanuvchi xabari
        state: FSM holati
    """
    try:
        name = message.text.strip()
        
        # Ism tekshiruvi - kamida 2 ta belgi bo'lishi kerak
        if len(name) < 2:
            await message.answer("❌ Ism juda qisqa. Iltimos, to'liq ism kiriting:")
            return
        
        # Ma'lumotni FSM state ga saqlash
        await state.update_data(name=name)
        
        await message.answer(
            f"✅ Ism qabul qilindi: {name}\n\n"
            "📱 Endi telefon raqamini kiriting:\n"
            "(Masalan: +998901234567 yoki 901234567)"
        )
        await state.set_state(AddPersonStates.waiting_for_phone)
        logger.info(f"Foydalanuvchi {message.from_user.id} ism kiritdi: {name}")
        
    except Exception as e:
        logger.error(f"Ism qabul qilishda xatolik: {e}")
        await message.answer("Xatolik yuz berdi. Qaytadan ism kiriting:")


@router.message(AddPersonStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """
    Telefon raqamni qabul qilish va saqlash
    Adminga xabar yuborish
    
    Args:
        message: Foydalanuvchi xabari
        state: FSM holati
    """
    try:
        phone = message.text.strip()
        
        # Telefon raqam formati tekshiruvi
        # O'zbekiston raqamlari uchun: +998 bilan boshlanishi yoki 9 raqamdan iborat
        phone_pattern = r'^(\+998)?[0-9]{9,12}$'
        if not re.match(phone_pattern, phone.replace(" ", "")):
            await message.answer(
                "❌ Noto'g'ri telefon raqam formati.\n"
                "Iltimos, to'g'ri formatda kiriting:\n"
                "+998901234567 yoki 901234567"
            )
            return
        
        # FSM state dan ismni olish
        user_data = await state.get_data()
        name = user_data.get('name')
        
        # Foydalanuvchi ID
        user_id = message.from_user.id
        
        # Agar bu foydalanuvchi uchun birinchi ma'lumot bo'lsa
        if user_id not in user_data_storage:
            user_data_storage[user_id] = []
        
        # Qo'shilgan odam ma'lumotlari
        person_data = {
            'name': name,
            'phone': phone
        }
        
        # Ma'lumotni saqlash
        user_data_storage[user_id].append(person_data)
        
        # Bugun qo'shilgan odamlar soni
        today_count = len(user_data_storage[user_id])
        
        # Foydalanuvchiga xabar yuborish
        await message.answer(
            f"✅ Rahmat! Ma'lumot saqlandi:\n\n"
            f"👤 Ism: {name}\n"
            f"📱 Telefon: {phone}\n\n"
            f"📊 Bugun qo'shilgan odamlar soni: {today_count} ta",
            reply_markup=get_main_menu()
        )
        
        # ADMINGA XABAR YUBORISH
        bot = message.bot
        await notify_admin(
            bot=bot,
            user=message.from_user,
            person_data=person_data,
            count=today_count
        )
        
        # FSM holatini tozalash
        await state.clear()
        
        logger.info(
            f"Foydalanuvchi {user_id} yangi odam qo'shdi. "
            f"Jami: {today_count}"
        )
        
    except Exception as e:
        logger.error(f"Telefon qabul qilishda xatolik: {e}")
        await message.answer(
            "Xatolik yuz berdi. Iltimos, qaytadan telefon raqam kiriting:"
        )


# ==================== ASOSIY FUNKSIYA ====================
async def main():
    """
    Botni ishga tushirish funksiyasi
    """
    try:
        # Bot va Dispatcher yaratish
        bot = Bot(token=config.TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Routerni ro'yxatdan o'tkazish
        dp.include_router(router)
        
        logger.info("✅ Bot ishga tushmoqda...")
        logger.info(f"📌 Platform URL: {config.ECOTRACK_URL}")
        logger.info(f"👤 Admin ID: {config.ADMIN_ID}")
        
        # Botni ishga tushirish (polling rejimida)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
    except Exception as e:
        logger.error(f"❌ Botni ishga tushirishda xatolik: {e}")
    finally:
        await bot.session.close()


# ==================== ISHGA TUSHIRISH ====================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot to'xtatildi")