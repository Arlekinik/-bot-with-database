import sqlite3
from aiogram import Router, F, types
from aiogram.dispatcher import router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup ,State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.formatting import Text

from button.button_note import button

router = Router()


class Addrem (StatesGroup):
    add_note = State()
    delete_note = State()


con = sqlite3.connect('note.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS notes("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_id INTEGER NOT NULL,"
            "content TEXT NOT NULL)")


@router.message(Command("start"))
async def cmd_start(message: Message):
    content = Text("Привет," , message.from_user.first_name,
                   "Это бот для заметок. Вот команды:\n",
                    "/start — Приветствие и помощь\n",
                    "/add <текст> — Добавить новую заметку\n",
                    "/list — Показать список всех заметок пользователя\n",
                    "/delete <номер> — Удалить заметку по её номеру из списка\n",
                    "/clear — Удалить все заметки пользователя\n")
    await message.answer(**content.as_kwargs(),reply_markup=button())

@router.message(Command("list"))
async def cmd_list(message: Message):
    content = cur.execute("SELECT content FROM notes WHERE user_id=?", (message.from_user.id,)).fetchall()
    if content:
        printer = ""
        for i in range(len(content)):
            printer += f"{i+1}. {content[i][0]}\n"
        await message.answer(printer)
    else:
        await message.answer("А выводить нечего 0_о")

@router.message(StateFilter(None), Command("add"))
async def cmd_add(message: Message, command: CommandObject, state: FSMContext):
    user_id = message.from_user.id
    if command.args is None:
        await message.answer("Теперь введите заметку")
        await state.set_state(Addrem.add_note)

    else:
        cur.execute("INSERT INTO notes (user_id, content) VALUES (?, ?)", (user_id, command.args))
        await message.answer("Заматка добавлена")
        con.commit()

@router.message(StateFilter(None), Command("delete"))
async def cmd_delete(message: Message, command: CommandObject, state: FSMContext):
    user_id = message.from_user.id
    if command.args is None:
        await message.answer("Какую заметку хотите удалить ?")
        await state.set_state(Addrem.delete_note)

    else:
        arg = int(command.args) - 1
        res = cur.execute("SELECT id FROM notes WHERE user_id=? ORDER BY id asc LIMIT 1 OFFSET ?",(user_id,arg)).fetchall()
        if not res:
            await message.answer("А удалять нечего 0_о")
            return
        else:
            cur.execute("DELETE FROM notes WHERE id = ?", (res[0][0],))
            con.commit()
            await message.answer("Заметка удалена")

@router.message(Addrem.delete_note, F.text)
async def cmd_delet_state(message: Message, state: FSMContext):
    try:
        note_id = int(message.text)
        user_id = message.from_user.id
        res = cur.execute("SELECT id FROM notes WHERE user_id=? ORDER BY id asc LIMIT 1 OFFSET ?",
                          (user_id, note_id)).fetchall()
        if not res:
            await message.answer("А удалять нечего 0_о")
            await state.clear()
            return
        else:
                res = res[0][0]
                cur.execute("DELETE FROM notes WHERE id = ?", (res,))
                con.commit()
                await message.answer("Заметка добавлена")
                await state.clear()
    except ValueError:
        await message.answer("Введите число")

@router.message(Addrem.add_note, F.text)
async def cmd_add_state(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("INSERT INTO notes (user_id, content) VALUES (?, ?)", (user_id, message.text,))
    con.commit()
    await message.answer("Заметка добавлена")
    await state.clear()




@router.message(Command("clear"))
async def cmd_clear(message: Message):
    user_id = message.from_user.id
    res = cur.execute("SELECT id FROM notes WHERE USER_ID=?",(user_id,)).fetchall()
    if not res:
        await message.answer("А удалять нечего 0_о")
        return
    else:
        cur.execute("DELETE FROM notes WHERE user_id = ?",(user_id,))
        con.commit()
        await message.answer("Заметки удалены")