import messages
import database_manager

database_joke_functions = {
    messages.MESSAGES.GET_RANDOM_JOKE: database_manager.make_get_joke_for_user_function(messages.MESSAGES.GET_RANDOM_JOKE),
    messages.MESSAGES.GET_TOP_JOKE: database_manager.make_get_joke_for_user_function(messages.MESSAGES.GET_TOP_JOKE),
    messages.MESSAGES.GET_FAVORITE_JOKE: database_manager.make_get_joke_for_user_function(messages.MESSAGES.GET_FAVORITE_JOKE)
}
