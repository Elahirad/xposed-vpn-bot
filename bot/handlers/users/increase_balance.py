from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.keyboards.default import get_default_markup
from bot.states import UserStates
from loader import dp, _, bot
from models import User, Receipt
from services.card import get_card_number
from services.users import get_admins


@dp.message_handler(i18n_text='Increase Balance💵', state=UserStates.main_page)
@dp.message_handler(commands=['increase_balance'], state='*')
async def _export_users(message: Message):
    text = _('Please enter the amount you want to increase')
    await message.answer(text)
    await UserStates.IncreaseBalance.get_amount.set()


@dp.message_handler(state=UserStates.IncreaseBalance.get_amount)
async def _get_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except:
        await message.answer(_('Please enter the amount you want to increase'))
        return

    text = _(
        'OK! Now send {amount} Tomans to below card number and send the receipt\nTouch the card number once to copy it!\n<code>{card_number}</code> ').format(
        amount=amount, card_number=get_card_number())
    await message.answer(text, parse_mode=types.ParseMode.HTML)
    await state.update_data(amount=amount)
    await UserStates.IncreaseBalance.get_receipt.set()


@dp.message_handler(state=UserStates.IncreaseBalance.get_receipt, content_types=types.ContentTypes.PHOTO)
async def _get_receipt(message: Message, state: FSMContext, user: User):
    photo = message.photo

    state_data = await state.get_data()

    Receipt.create(user=user, amount=state_data['amount'], receipt_photo=photo[-1].file_id)

    text = _('You receipt is received. Wait for approval process.')
    await message.answer(text, reply_markup=get_default_markup(user))

    text = _('Dear Admin !\nNew receipt is arrived. Check your panel please.')
    for admin in get_admins():
        await bot.send_message(chat_id=admin.id, text=text)

    await UserStates.main_page.set()


@dp.message_handler(lambda message: message.content_type != types.ContentTypes.PHOTO,
                    state=UserStates.IncreaseBalance.get_receipt)
async def _get_receipt(message: Message, state: FSMContext):
    await message.answer(_('Please send the receipt image'))
