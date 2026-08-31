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


if __name__ == "__main__":
    main()