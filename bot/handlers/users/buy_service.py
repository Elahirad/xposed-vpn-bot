from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.keyboards.default import get_default_markup, get_products_markup, get_order_confirm_markup, get_back_markup
from bot.states import UserStates
from loader import dp, _
from models import Product
from models import User
from services.hiddify import HiddifyInterface
from services.products import find_product
from services.service import add_service
from services.users import decrease_balance


@dp.message_handler(i18n_text='Buy a Service 🛒', state=UserStates.main_page)
@dp.message_handler(commands=['buy_service'], state='*')
async def _buy_service(message: Message):
    text = _('Please select the product you want.')
    await message.answer(text, reply_markup=get_products_markup())
    await UserStates.BuyService.choose_product.set()


@dp.message_handler(state=UserStates.BuyService.choose_product)
async def _get_product(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('You have successfully returned to the main menu.'),
                             reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
        return
    product = find_product(message.text)
    await state.update_data(product=product.name)
    await message.answer(_('OK! Now please choose a name for your service.'), reply_markup=get_back_markup())
    await UserStates.BuyService.choose_name.set()


@dp.message_handler(state=UserStates.BuyService.choose_name)
async def _get_name(message: Message, user: User, state: FSMContext):
    if message.text == _('Back 🔙'):
        await message.answer(_('Please select the product you want.'),
                             reply_markup=get_products_markup())
        await UserStates.BuyService.choose_product.set()
        return
    state_data = await state.get_data()
    product = find_product(state_data['product'])
    await state.update_data(name=message.text)
    await message.answer(
        _('OK! {product_name} Selected.\nHere is details of the product:\nName: {name}\nDays: {days}\nLimit(GB): {limit}\nPrice: {price}\nPress Confirm ✅ Button to finalize the order.').format(
            product_name=product.name, name=message.text, days=product.days, limit=product.gb_limit,
            price=product.price),
        reply_markup=get_order_confirm_markup())
    await UserStates.BuyService.confirm.set()


@dp.message_handler(state=UserStates.BuyService.confirm)
async def _get_confirmation(message: Message, state: FSMContext, user: User):
    if message.text == _('Back 🔙'):
        await message.answer(_('OK! Now please choose a name for your service.'),
                             reply_markup=get_back_markup())
        await UserStates.BuyService.choose_name.set()
        return

    if message.text == _('Confirm ✅'):
        state_data = await state.get_data()
        name = state_data['name']
        product: Product = find_product(state_data['product'])

        if user.balance < product.price:
            await message.answer(
                _('Dear user. Your balance is insufficient for purchasing this service.\nPlease charge your account and try again'),
                reply_markup=get_default_markup(user))
            await UserStates.main_page.set()
            return

        hiddify = HiddifyInterface(product.server.url, product.server.proxy_path,
                                   product.server.users_path, product.server.admin_uuid)
        service = hiddify.create_service(name, product.days, product.gb_limit)
        add_service(service['uuid'], user.id, product.server.id, product.id)
        decrease_balance(user.id, product.price)
        await message.answer(_('Purchased successfully!\nYour subscription link is:\n{link}').format(
            link=hiddify.get_sub_link(service['uuid'])), reply_markup=get_default_markup(user))
        await UserStates.main_page.set()
