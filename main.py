from search_engine.search import search_web
from search_engine.llm import generate_answer


def display_sources(results):
    print()
    print("=" * 50)
    print("                   SOURCES")
    print("=" * 50)
    print()

    for number, result in enumerate(results, start=1):
        print(f"[{number}] {result.get('title', 'Unknown')}")
        print(result.get('url', 'Unknown'))
        print()


def main():
    print("=" * 50)
    print("           CUSTOM SEARCH ENGINE")
    print("=" * 50)
    print()
    print("Type 'exit' to quit.")
    print()

    while True:
        query = input("Enter your search query: ").strip()

        if query.lower() == "exit":
            print()
            print("Goodbye!")
            break

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

        print(f"Found {len(results)} search results.")
        print()
        print("Generating answer...")
        print()

        answer = generate_answer(query, results)

        print("=" * 50)
        print("                    ANSWER")
        print("=" * 50)
        print()

        print(answer)

        display_sources(results)


if __name__ == "__main__":
    main()