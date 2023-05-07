import parse_joke_manager
import psycopg2
import bot_messages

conn = psycopg2.connect(
  database="postgres",
  user="postgres",
  host="localhost",
  password="qweasdzxc12321"
)

conn.autocommit = True
cur = conn.cursor()

joke_type_to_query = {
    bot_messages.MESSAGES.GET_TOP_JOKE: "select joke_sentence, joke_id from get_best_joke_for_user(",
    bot_messages.MESSAGES.GET_RANDOM_JOKE: "select joke_sentence, joke_id from get_random_joke_for_user(",
    bot_messages.MESSAGES.GET_FAVORITE_JOKE: "select joke_sentence, joke_id from get_favorite_joke_for_user("
}


def add_new_to_actual_jokes(new_joke_number):
    query = "select * from add_new_to_actual_jokes(" + str(new_joke_number) + ");"
    cur.execute(query)
    reply = cur.fetchall()[0]
    is_sucsesfull_inserting = reply[0]
    return is_sucsesfull_inserting is True


def add_new_to_joke_sentences(new_joke_number):
    jokes = [tuple([parse_joke_manager.get_new_joke()]) for _ in range(new_joke_number)]
    query = "insert into joke_sentences(joke_sentence) values (%s)"
    cur.executemany(query, jokes)


def make_get_joke_for_user_function(joke_type):
    def get_joke_for_user_function(user_id):
        query = joke_type_to_query[joke_type] + str(user_id) + ");"
        cur.execute(query)
        query_result = cur.fetchall()
        if not query_result:
            return None, None
        joke_sentence, joke_id = query_result[0]
        return joke_sentence, joke_id
    return get_joke_for_user_function


def add_evaluation_for_joke(joke_id, joke_ratting):
    query = "call add_evaluation_for_joke(" + str(joke_id) + "," + str(joke_ratting) + ");"
    cur.execute(query)
    return


def add_user_period_request(user_id, period):
    query = "call add_user_period_request(" + str(user_id) + "," + str(period) + ");"
    cur.execute(query)
    return


def add_new_user(user_id):
    query = "insert into users(user_telegram_id) values (" + str(user_id) + ") on conflict do nothing;"
    cur.execute(query)
    return


def add_favorite_joke(user_id, joke_id):
    query = "call add_favorite_joke(" + str(user_id) + "," + str(joke_id) + ");"
    cur.execute(query)
    return


def delete_from_favorite_joke(user_id, joke_id):
    query = "call delete_from_favorite_joke(" + str(user_id) + "," + str(joke_id) + ");"
    cur.execute(query)
    return


joke_sentences_needed_row_count = 20
actual_jokes_needed_row_count = 10


def fill_tables_if_not_enough_data():
    joke_sentences_count_query = "select count(*) from joke_sentences"
    actual_jokes_count_query = "select count(*) from actual_jokes"
    cur.execute(joke_sentences_count_query)
    joke_sentences_row_count = cur.fetchone()[0]
    cur.execute(actual_jokes_count_query)
    actual_jokes_row_count = cur.fetchone()[0]
    if joke_sentences_row_count < joke_sentences_needed_row_count:
        add_new_to_joke_sentences(joke_sentences_needed_row_count - joke_sentences_row_count)
    if actual_jokes_row_count < actual_jokes_needed_row_count:
        add_new_to_actual_jokes(actual_jokes_needed_row_count - actual_jokes_row_count)
    return
