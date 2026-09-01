from search_engine.search import search_web
from search_engine.llm import generate_answer


def main():
    print("=" * 50)
    print("           CUSTOM SEARCH ENGINE")
    print("=" * 50)
    print()

    query = input("Enter your search query: ")

    if not query.strip():
        print("Please enter a search query.")
        return

    print()
    print("Searching the web...")
    print()

    results = search_web(query)

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

    print()
    print("=" * 50)
    print("                   SOURCES")
    print("=" * 50)
    print()

    for number, result in enumerate(results, start=1):
        print(f"[{number}] {result['title']}")
        print(result["url"])
        print()


if __name__ == "__main__":
    main()