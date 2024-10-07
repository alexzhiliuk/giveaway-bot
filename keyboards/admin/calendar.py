import calendar
from datetime import datetime

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class DialogCalendar:
    months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]

    def __init__(self, year: int = datetime.now().year, month: int = datetime.now().month):
        self.year = year
        self.month = month

    @staticmethod
    def get_confirm_kb(year, month, day):
        inline_kb = InlineKeyboardMarkup()
        inline_kb.add(InlineKeyboardButton("Верно", callback_data=f"SET-DATE {year} {month} {day}"))
        inline_kb.add(InlineKeyboardButton("Изменить", callback_data="START-YEAR"))
        return inline_kb

    @staticmethod
    def start_calendar(
        self,
        year: int = datetime.now().year
    ) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=5)

        for value in range(year, year + 2):
            inline_kb.add(InlineKeyboardButton(
                str(value),
                callback_data=f"SET-YEAR {value}"
            ))

        return inline_kb

    @classmethod
    def get_month_kb(cls, year: int):
        inline_kb = InlineKeyboardMarkup(row_width=6)

        inline_kb.add(InlineKeyboardButton(str(year), callback_data=f"START-YEAR"))
        inline_kb.add(InlineKeyboardButton("==============", callback_data=" "))

        months_row = []
        for month in cls.months[0:6]:
            months_row.append(
                InlineKeyboardButton(
                    month,
                    callback_data=f"SET-MONTH {year} {cls.months.index(month) + 1}"
                )
            )
        inline_kb.add(*months_row)

        months_row = []
        for month in cls.months[6:12]:
            months_row.append(
                InlineKeyboardButton(
                    month,
                    callback_data=f"SET-MONTH {year} {cls.months.index(month) + 1}"
                )
            )
        inline_kb.add(*months_row)

        return inline_kb

    @classmethod
    def get_days_kb(cls, year: int, month: int):
        inline_kb = InlineKeyboardMarkup(row_width=7)

        inline_kb.add(InlineKeyboardButton(
            str(year),
            callback_data=f"START-YEAR"
        ))
        inline_kb.add(InlineKeyboardButton(
            cls.months[month - 1],
            callback_data=f"START-MONTH {year}"
        ))
        inline_kb.add(InlineKeyboardButton("==============", callback_data=" "))

        inline_kb.add(
            *[InlineKeyboardButton(day, callback_data=" ") for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]]
        )

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            days_row = []
            for day in week:
                if day == 0:
                    days_row.append(InlineKeyboardButton(" ", callback_data=" "))
                    continue
                days_row.append(
                    InlineKeyboardButton(
                        str(day), callback_data=f"SET-DAY {year} {month} {day}"
                    )
                )
            inline_kb.add(*days_row)

        return inline_kb

    # def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
    #     return_data = (False, None)
    #     if data['act'] == "IGNORE":
    #         await query.answer(cache_time=60)
    #     if data['act'] == "SET-YEAR":
    #         await query.message.edit_reply_markup(await self._get_month_kb(int(data['year'])))
    #     if data['act'] == "PREV-YEARS":
    #         new_year = int(data['year']) - 5
    #         await query.message.edit_reply_markup(await self.start_calendar(new_year))
    #     if data['act'] == "NEXT-YEARS":
    #         new_year = int(data['year']) + 5
    #         await query.message.edit_reply_markup(await self.start_calendar(new_year))
    #     if data['act'] == "START":
    #         await query.message.edit_reply_markup(await self.start_calendar(int(data['year'])))
    #     if data['act'] == "SET-MONTH":
    #         await query.message.edit_reply_markup(await self._get_days_kb(int(data['year']), int(data['month'])))
    #     if data['act'] == "SET-DAY":
    #         await query.message.delete_reply_markup()   # removing inline keyboard
    #         return_data = True, datetime(int(data['year']), int(data['month']), int(data['day']))
    #     return return_data
