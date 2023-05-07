from messages import *

messages_to_text = {

    MESSAGES.START_GREETINGS:
        '👋 Привет! Я бот, скидывающий анекдоты! Ты можешь получать '
        'любимые анекдоты всех или свои любимые анекдоты, я запомню!, '
        'как ты хочешь, чтобы я присылал тебе анекдоты?',

    MESSAGES.GET_TOP_JOKE:
        'Топовый анекдот!',

    MESSAGES.GET_RANDOM_JOKE:
        'Случайный анекдот!',

    MESSAGES.GET_FAVORITE_JOKE:
        'Любимый анекдот!',

    MESSAGES.NO_FAVORITE_JOKES_FOR_USER:
        'Похоже, что у вы ещё не ставили анекдотам хорошие оценки, '
        'но сейчас вы можете получить топовый или случайный анекдот и '
        'пополнить свою коллекцию!',

    MESSAGES.NO_TOP_JOKES_FOR_USER:
        'Похоже я существую ещё слишком мало, и люди ещё не '
        'выбрали достаточно крутых анекдотов для тебя'
        ', но я уверен мы это быстро исправим!',

    MESSAGES.NO_RANDOM_JOKES_FOR_USER:
        'Похоже, что у нас со всем всё плохо, раз я тебе даже случайный '
        'анек не могу подкинуть, прости ради Христа, просто меня '
        'делали криворукие студенты недопрограммисты, которым надо'
        'просто сдать просто проект по базам данных, ты их не осуждай,'
        ' им и так не просто',

    MESSAGES.JOKE_RATING_QUESTION:
        'Как тебе этот анек?) Оцени его по шкале от одного до пяти,'
        ' твоя оценка повлияет на его репутацию!',

    MESSAGES.REPLY_ON_RATTING:
        'Хорошо, я запомню, чё, ещё по анеку)!',

    MESSAGES.ZERO_RATTING:
        '0',

    MESSAGES.ONE_RATTING:
        '1',

    MESSAGES.TWO_RATTING:
        '2',

    MESSAGES.THREE_RATTING:
        '3',

    MESSAGES.FOUR_RATTING:
        '4',

    MESSAGES.FIVE_RATTING:
        '5',

    MESSAGES.GET_JOE_IN_ONE_HOUR:
        'Хочу раз в час!',

    MESSAGES.GET_JOE_IN_FIVE_HOUR:
        'Хочу раз в пять часов!',

    MESSAGES.GET_JOE_IN_INFINITE_HOUR:
        'Не хочу получать :(',

    MESSAGES.REPLY_ON_PERIOD_QUERY:
        'Хорошо! А теперь можешь получить какой-нибуть анек!)',

    MESSAGES.ADD_IN_FAVORITE:
        'Добавить в любимые!',

    MESSAGES.DELETE_FROM_FAVORITE:
        'Удалить из любимых',

    MESSAGES.STAY_IN_FAVORITE:
        'Оставить в любимых',

    MESSAGES.FAVORITE_ADD_SUCCESSFULL:
        'Добавил',

    MESSAGES.FAVORITE_DELETE_SUCCESSFULL:
        'Удалил',

    MESSAGES.STAY_IN_FAVORITE_QUESTION:
        'Оставить в любимых?',
    MESSAGES.FAVORITE_STAYING_SUCCESSFULL:
        'Оставил'
}

evaluation_to_number = {
    MESSAGES.ZERO_RATTING: 0,
    MESSAGES.ONE_RATTING: 1,
    MESSAGES.TWO_RATTING: 2,
    MESSAGES.THREE_RATTING: 3,
    MESSAGES.FOUR_RATTING: 4,
    MESSAGES.FIVE_RATTING: 5
}

period_request_to_number = {
    MESSAGES.GET_JOE_IN_ONE_HOUR: 1,
    MESSAGES.GET_JOE_IN_FIVE_HOUR: 5,
    MESSAGES.GET_JOE_IN_INFINITE_HOUR: None
}

no_joke_messages = {
    MESSAGES.GET_RANDOM_JOKE: MESSAGES.NO_RANDOM_JOKES_FOR_USER,
    MESSAGES.GET_FAVORITE_JOKE: MESSAGES.NO_FAVORITE_JOKES_FOR_USER,
    MESSAGES.GET_TOP_JOKE: MESSAGES.NO_TOP_JOKES_FOR_USER,
}