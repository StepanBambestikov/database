import telebot
from telebot import types
import bot_messages
import database_manager
import joke_functions


class joke_waiting_for_evaluation_manager:
    joke_waiting_for_evaluation = {}

    def __init__(self):
        self.joke_waiting_for_evaluation = {}

    def add_joke(self, joke_id, user_id):
        self.joke_waiting_for_evaluation[user_id] = joke_id

    def get_waiting_joke(self, user_id):
        try:
            joke_id = self.joke_waiting_for_evaluation[user_id]
            del self.joke_waiting_for_evaluation[user_id]
            return joke_id
        except KeyError:
            return None


def make_ratting_markup():
    zero_joke_ratting_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.ZERO_RATTING])
    one_joke_ratting_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.ONE_RATTING])
    two_joke_ratting_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.TWO_RATTING])
    three_joke_ratting_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.THREE_RATTING])
    four_joke_ratting_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.FOUR_RATTING])
    five_joke_ratting_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.FIVE_RATTING])
    add_in_favorite_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.ADD_IN_FAVORITE])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(zero_joke_ratting_button, one_joke_ratting_button, two_joke_ratting_button,
               three_joke_ratting_button, four_joke_ratting_button, five_joke_ratting_button,
               add_in_favorite_button)
    return markup


def make_general_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    favorite_joke_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.GET_FAVORITE_JOKE])
    top_joke_button = types.KeyboardButton(bot_messages.messages_to_text[bot_messages.MESSAGES.GET_TOP_JOKE])
    random_joke_button = types.KeyboardButton(bot_messages.messages_to_text[bot_messages.MESSAGES.GET_RANDOM_JOKE])
    markup.add(favorite_joke_button, top_joke_button, random_joke_button)
    return markup


def make_favorite_joke_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stay_in_favorite_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.STAY_IN_FAVORITE])
    delete_from_favorite_button = types.KeyboardButton(bot_messages.messages_to_text[bot_messages.MESSAGES.DELETE_FROM_FAVORITE])
    markup.add(stay_in_favorite_button, delete_from_favorite_button)
    return markup


def make_period_question_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    one_hour_button = types.KeyboardButton(
        bot_messages.messages_to_text[bot_messages.MESSAGES.GET_JOE_IN_ONE_HOUR])
    five_hour_button = types.KeyboardButton(bot_messages.messages_to_text[bot_messages.MESSAGES.GET_JOE_IN_FIVE_HOUR])
    infinite_hour_button = types.KeyboardButton(bot_messages.messages_to_text[bot_messages.MESSAGES.GET_JOE_IN_INFINITE_HOUR])
    markup.add(one_hour_button, five_hour_button, infinite_hour_button)
    return markup


def start_bot():
    bot = telebot.TeleBot('My_telegram_bot_token')
    gemeral_markup = make_general_markup()
    ratting_markup = make_ratting_markup()
    period_markup = make_period_question_markup()
    favorite_joke_markup = make_favorite_joke_markup()

    waiting_joke_manager = joke_waiting_for_evaluation_manager()

    def send_joke(user_id, joke):
        bot.send_message(user_id, joke, parse_mode='Markdown')

    def joke_request_manager(message, joke_request_type):
        database_joke_function = joke_functions.database_joke_functions[joke_request_type]
        joke_sentence, joke_id = database_joke_function(message.from_user.id)
        if not joke_sentence and joke_request_type == bot_messages.MESSAGES.GET_FAVORITE_JOKE:
            bot.send_message(message.from_user.id,
                             bot_messages.messages_to_text[bot_messages.MESSAGES.NO_FAVORITE_JOKES_FOR_USER],
                             parse_mode='Markdown', reply_markup=gemeral_markup)
            return False
        while not joke_sentence:
            is_successful_inserting = database_manager.add_new_to_actual_jokes(1)
            if not is_successful_inserting:
                database_manager.add_new_to_joke_sentences(10)
                database_manager.add_new_to_actual_jokes(1)
            joke_sentence, joke_id = database_joke_function(message.from_user.id)

        send_joke(message.from_user.id, joke_sentence)
        waiting_joke_manager.add_joke(joke_id, message.from_user.id)
        return True

    def ratting_request_manager(message, ratting_type):
        bot.send_message(message.from_user.id,
                         bot_messages.messages_to_text[bot_messages.MESSAGES.REPLY_ON_RATTING],
                         parse_mode='Markdown', reply_markup=gemeral_markup)
        joke_id = waiting_joke_manager.get_waiting_joke(message.from_user.id)
        if joke_id:
            database_manager.add_evaluation_for_joke(joke_id, bot_messages.evaluation_to_number[ratting_type])

    def period_request_manager(message, period_type):
        bot.send_message(message.from_user.id,
                         bot_messages.messages_to_text[bot_messages.MESSAGES.REPLY_ON_PERIOD_QUERY],
                         parse_mode='Markdown', reply_markup=gemeral_markup)
        if period_type != bot_messages.MESSAGES.GET_JOE_IN_INFINITE_HOUR:
            database_manager.add_user_period_request(message.from_user.id,
                                                     bot_messages.period_request_to_number[period_type])

    @bot.message_handler(commands=['start'])
    def start(message):
        database_manager.fill_tables_if_not_enough_data()
        database_manager.add_new_user(message.from_user.id)
        bot.send_message(message.from_user.id, bot_messages.messages_to_text[bot_messages.MESSAGES.START_GREETINGS],
                         reply_markup=period_markup)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):

        if message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.GET_FAVORITE_JOKE]:
            favorite_joke_is_getted = joke_request_manager(message, bot_messages.MESSAGES.GET_FAVORITE_JOKE)
            if favorite_joke_is_getted:
                bot.send_message(message.from_user.id,
                             bot_messages.messages_to_text[bot_messages.MESSAGES.STAY_IN_FAVORITE_QUESTION],
                             parse_mode='Markdown', reply_markup=favorite_joke_markup)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.GET_RANDOM_JOKE]:
            joke_request_manager(message, bot_messages.MESSAGES.GET_RANDOM_JOKE)
            bot.send_message(message.from_user.id,
                             bot_messages.messages_to_text[bot_messages.MESSAGES.JOKE_RATING_QUESTION],
                             parse_mode='Markdown', reply_markup=ratting_markup)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.GET_TOP_JOKE]:
            joke_request_manager(message, bot_messages.MESSAGES.GET_TOP_JOKE)
            bot.send_message(message.from_user.id,
                             bot_messages.messages_to_text[bot_messages.MESSAGES.JOKE_RATING_QUESTION],
                             parse_mode='Markdown', reply_markup=ratting_markup)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.ZERO_RATTING]:
            ratting_request_manager(message, bot_messages.MESSAGES.ZERO_RATTING)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.ONE_RATTING]:
            ratting_request_manager(message, bot_messages.MESSAGES.ONE_RATTING)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.TWO_RATTING]:
            ratting_request_manager(message, bot_messages.MESSAGES.TWO_RATTING)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.THREE_RATTING]:
            ratting_request_manager(message, bot_messages.MESSAGES.THREE_RATTING)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.FOUR_RATTING]:
            ratting_request_manager(message, bot_messages.MESSAGES.FOUR_RATTING)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.FIVE_RATTING]:
            ratting_request_manager(message, bot_messages.MESSAGES.FIVE_RATTING)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.ADD_IN_FAVORITE]:
            joke_id = waiting_joke_manager.get_waiting_joke(message.from_user.id)
            if joke_id:
                database_manager.add_favorite_joke(message.from_user.id,joke_id)
                bot.send_message(message.from_user.id,
                                 bot_messages.messages_to_text[bot_messages.MESSAGES.FAVORITE_ADD_SUCCESSFULL],
                                 reply_markup=gemeral_markup)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.DELETE_FROM_FAVORITE]:
            joke_id = waiting_joke_manager.get_waiting_joke(message.from_user.id)
            if joke_id:
                database_manager.delete_from_favorite_joke(message.from_user.id, joke_id)
                bot.send_message(message.from_user.id,
                                 bot_messages.messages_to_text[bot_messages.MESSAGES.FAVORITE_DELETE_SUCCESSFULL],
                                 reply_markup=gemeral_markup)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.STAY_IN_FAVORITE]:
            bot.send_message(message.from_user.id,
                             bot_messages.messages_to_text[bot_messages.MESSAGES.FAVORITE_STAYING_SUCCESSFULL],
                             reply_markup=gemeral_markup)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.GET_JOE_IN_ONE_HOUR]:
            period_request_manager(message, bot_messages.MESSAGES.GET_JOE_IN_ONE_HOUR)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.GET_JOE_IN_FIVE_HOUR]:
            period_request_manager(message, bot_messages.MESSAGES.GET_JOE_IN_FIVE_HOUR)
        elif message.text == bot_messages.messages_to_text[bot_messages.MESSAGES.GET_JOE_IN_INFINITE_HOUR]:
            period_request_manager(message, bot_messages.MESSAGES.GET_JOE_IN_INFINITE_HOUR)

    bot.polling(none_stop=True, interval=0)
