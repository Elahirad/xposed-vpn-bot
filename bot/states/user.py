from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    main_page = State()

    class IncreaseBalance(StatesGroup):
        get_amount = State()
        get_receipt = State()
