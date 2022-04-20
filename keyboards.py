from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.emoji import emojize

choice_callback = CallbackData('question', 'type')

category_choice_keyboard = types.InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text=emojize(':thinking_face: Вопросы'),
                callback_data=choice_callback.new(type='questions')),
            types.InlineKeyboardButton(
                text=emojize(':pouting_face: Недовольства'),
                callback_data=choice_callback.new(type='angry'))
        ],
        [
            types.InlineKeyboardButton(
                text=emojize(':face_with_monocle: Наблюдения'),
                callback_data=choice_callback.new(type='observations')),
            types.InlineKeyboardButton(
                text=emojize(':unamused_face: Жалобы'),
                callback_data=choice_callback.new(type='complaints')
            )
        ]
    ]
)
