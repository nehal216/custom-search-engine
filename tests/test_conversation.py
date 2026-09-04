from search_engine.conversation import Conversation


def test_conversation_starts_empty():

    conversation = Conversation()

    assert conversation.get_history() == []


def test_add_message():

    conversation = Conversation()

    conversation.add_message(
        "user",
        "What is Python?"
    )

    history = conversation.get_history()

    assert len(history) == 1
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "What is Python?"


def test_multiple_messages():

    conversation = Conversation()

    conversation.add_message(
        "user",
        "What is Python?"
    )

    conversation.add_message(
        "assistant",
        "Python is a programming language."
    )

    history = conversation.get_history()

    assert len(history) == 2


def test_clear_conversation():

    conversation = Conversation()

    conversation.add_message(
        "user",
        "What is Python?"
    )

    conversation.clear()

    assert conversation.get_history() == []