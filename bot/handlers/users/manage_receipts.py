from aiogram import types
from aiogram.dispatcher.filters import Regexp
from aiogram.types import Message
from peewee import DoesNotExist

from bot.keyboards.inline import get_receipt_inline_markup
from bot.states import UserStates
from loader import dp, _, bot
from services.receipt import get_unresolved_receipts, get_receipt_by_id
from services.users import increase_balance


@dp.message_handler(i18n_text='Manage receipts 🧾', state=UserStates.main_page)
@dp.message_handler(commands=['manage_receipts'], state='*')
async def _export_users(message: Message):
    receipts = get_unresolved_receipts()

    if not len(receipts):
        await message.answer(text=_("There is no receipts!"))

    for receipt in receipts:
        markup = get_receipt_inline_markup(receipt.id)
        await message.answer_photo(photo=receipt.receipt_photo,
                                   caption=_('User: @{user}\nAmount: {amount} Tomans').format(
                                       user=receipt.user.username,
                                       amount=receipt.amount),
                                   reply_markup=markup)


@dp.callback_query_handler(Regexp(r'^receipt_approve_(\d+)$'), state='*')
async def approve_receipt(callback_query: types.CallbackQuery, regexp: Regexp):
    receipt_id = int(regexp.group(1))
    try:
        receipt = get_receipt_by_id(receipt_id)

        increase_balance(receipt.user.id, receipt.amount)

        receipt.approved = True

        receipt.save()

        await bot.send_message(chat_id=receipt.user.id, text=_('Your receipt has been approved!'))
        await callback_query.answer(_("Receipt approved."))
        await callback_query.message.edit_reply_markup(reply_markup=None)  # Remove the inline buttons
    except DoesNotExist:
        await callback_query.answer(_("Receipt not found."))
    except Exception as e:
        await callback_query.answer(_("An error occurred."))


@dp.callback_query_handler(Regexp(r'^receipt_reject_(\d+)$'), state='*')
async def reject_receipt(callback_query: types.CallbackQuery, regexp: Regexp):
    receipt_id = int(regexp.group(1))
    try:
        receipt = get_receipt_by_id(receipt_id)

        receipt.rejected = True

        receipt.save()
        await bot.send_message(chat_id=receipt.user.id, text=_('Your receipt has been rejected!'))
        await callback_query.answer(_("Receipt rejected."))
        await callback_query.message.edit_reply_markup(reply_markup=None)  # Remove the inline buttons
    except DoesNotExist:
        await callback_query.answer(_("Receipt not found."))
    except Exception as e:
        await callback_query.answer(_("An error occurred."))
