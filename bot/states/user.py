from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    main_page = State()

    message_reply = State()

    class IncreaseBalance(StatesGroup):
        get_amount = State()
        get_receipt = State()

    class BuyService(StatesGroup):
        choose_product = State()
        choose_name = State()
        confirm = State()

    manage_admins = State()
    add_admin = State()

    class ManageServers(StatesGroup):
        main = State()
        get_name = State()
        get_url = State()
        get_proxy_path = State()
        get_users_path = State()
        get_admin_uuid = State()
        edit_name = State()
        edit_url = State()
        edit_proxy_path = State()
        edit_user_path = State()
        edit_admin_uuid = State()

    class ManageProducts(StatesGroup):
        main = State()
        get_name = State()
        get_server = State()
        get_days = State()
        get_gb_limit = State()
        get_price = State()
        edit_name = State()
        edit_server = State()
        edit_days = State()
        edit_gb_limit = State()
        edit_price = State()

    class MyServices(StatesGroup):
        prolong_confirm = State()
        remove_confirm = State()
        remove_second_confirm = State()