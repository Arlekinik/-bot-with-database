    from aiogram.types import ReplyKeyboardMarkup
    from aiogram.utils.keyboard import ReplyKeyboardBuilder

    def button() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardBuilder()
        kb.button(text="/start")
        kb.button(text="/list")
        kb.button(text="/add")
        kb.button(text="/delete")
        kb.button(text="/clear")
        kb.adjust(2,1,2)

        return kb.as_markup(input_field_placeholder="Выберите команду или введите текст")