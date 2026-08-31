from search_engine.search import search_web


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
    print("Searching for:", query)
    print()

    results = search_web(query)

    print("SEARCH RESULTS")
    print("-" * 50)

    for number, result in enumerate(results, start=1):
        print(f"[{number}] {result['title']}")
        print(result["url"])
        print()


if __name__ == "__main__":
    main()