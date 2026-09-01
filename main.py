from search_engine.search import search_web
from search_engine.llm import generate_answer


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

        snippet = content[:200].replace("\n", " ")

        print(f"[{number}] {title}")
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
    print("  exit    - Exit the search engine")
    print()
    print("Anything else is treated as a search query.")
    print()


def main():
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

        if not query:
            print("Please enter a search query.")
            print()
            continue

        print()
        print("Searching the web...")
        print()

        results = search_web(query)

        if not results:
            print("No search results were found.")
            print()
            continue

        print(f"Found {len(results)} results.")
        print("Generating answer...")
        print()

        answer = generate_answer(query, results)

        print("=" * 60)
        print("                          ANSWER")
        print("=" * 60)
        print()

        print(answer)

        display_sources(results)


if __name__ == "__main__":
    main()