from search_engine.search import search_web
from search_engine.llm import generate_answer
from search_engine.ranking import rank_results
from search_engine.query import analyze_query, make_contextual_query
from search_engine.conversation import Conversation

def display_sources(results):

    print()
    print("=" * 60)
    print("                         SOURCES")
    print("=" * 60)
    print()

    for number, result in enumerate(results, start=1):
        title = result.get("title", "Unknown")
        url = result.get("url", "Unknown")
        content = result.get("content", "")
        score = result.get("score", 0)

        snippet = content[:200].replace("\n", " ")

        print(f"[{number}] {title}")
        print(f"     Relevance score: {score:.2f}")
        print(f"     {url}")
        print(f"     {snippet}...")
        print()


def display_help():
    print()
    print("=" * 60)
    print("                          HELP")
    print("=" * 60)
    print()
    print("Commands:")
    print("  help    - Show this help menu")
    print("  clear   - Clear conversation history")
    print("  exit    - Exit the search engine")
    print()
    print("Anything else is treated as a search query.")
    print()


def main():

    conversation = Conversation()
    print("=" * 60)
    print("                  CUSTOM SEARCH ENGINE")
    print("=" * 60)
    print()
    print("Search the web and get AI-generated answers.")
    print("Type 'help' for commands or 'exit' to quit.")
    print()

    while True:
        query = input("Search > ").strip()

        if query.lower() == "exit":
            print()
            print("Goodbye!")
            break

        if query.lower() == "help":
            display_help()
            continue

        if query.lower() == "clear":
            conversation.clear()
            print()
            print("Conversation history cleared.")
            print()
            continue

        if not query:
            print("Please enter a search query.")
            print()
            continue

        print()
        print("Searching the web...")
        print()

        contextual_query = make_contextual_query(
        query,
        conversation.get_history()
        )

        search_queries = analyze_query(contextual_query)

        all_results = []

        for search_query in search_queries:
            print(f"Searching for: {search_query}")

            results = search_web(search_query)

            all_results.extend(results)

        if not all_results:
            print("No search results were found.")
            print()
            continue

        ranked_results = rank_results(all_results)

        print(f"Found {len(results)} search results.")
        print(f"Using the top {len(ranked_results)} results.")
        print("Generating answer...")
        print()

        answer = generate_answer(
            query, 
            ranked_results,
            conversation.get_history()
        )

        conversation.add_message("user", query)
        conversation.add_message("assistant", answer)

        print("=" * 60)
        print("                          ANSWER")
        print("=" * 60)
        print()

        print(answer)

        display_sources(ranked_results)


if __name__ == "__main__":
    main()