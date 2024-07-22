from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline import get_card_markup
from loader import dp, _
from services.card import get_cards, add_card, disable_card, activate_card


@dp.message_handler(commands=['manage_cards'], state='*', is_admin=True)
async def _get_cards(message: Message):
    cards = get_cards()
    if not len(cards):
        await message.reply(_('No cards found.'))
        return
    for card in cards:
        await message.reply(_('ID: {id}\nNumber: {number}\nStatus: {status}')
                            .format(id=card.id, number=card.number,
                                    status=_('Active ✅') if card.is_active else
                                    _('Inactive ⛔')),
                            reply_markup=get_card_markup(card.id, card.is_active))


@dp.message_handler(commands=['add_card'], state='*', is_admin=True)
async def _add_card(message: Message):
    try:
        number = message.text.split(' ')[1]
        card = add_card(number)
        await message.reply(_('Card {card} added successfully.').format(card=card.number))
    except:
        await message.reply(_("Failed to add card.\nCommand usage:\n/add_card [card_number]"))


@dp.callback_query_handler(lambda c: c.data.startswith('disable_card_'), state='*')
async def process_callback_card(callback_query: CallbackQuery, state: FSMContext):
    try:
        card_id = int(callback_query.data.split('_')[2])
        disable_card(card_id)
        await callback_query.answer(_('Card disabled successfully.'))
        await callback_query.message.edit_text(callback_query.message.text.replace(_('Active ✅'), _('Inactive ⛔')),
                                               reply_markup=get_card_markup(card_id, False))
    except:
        await callback_query.answer(_('An error occurred.'))


@dp.callback_query_handler(lambda c: c.data.startswith('activate_card_'), state='*')
async def process_callback_card(callback_query: CallbackQuery, state: FSMContext):
    try:
        card_id = int(callback_query.data.split('_')[2])
        activate_card(card_id)
        await callback_query.answer(_('Card activated successfully.'))
        await callback_query.message.edit_text(callback_query.message.text.replace(_('Inactive ⛔'), _('Active ✅'), ),
                                               reply_markup=get_card_markup(card_id, True))
    except:
        await callback_query.answer(_('An error occurred.'))
