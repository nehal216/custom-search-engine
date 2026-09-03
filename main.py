from search_engine.search import search_web
from search_engine.llm import generate_answer
from search_engine.ranking import rank_results
from search_engine.query import analyze_query, make_contextual_query
from search_engine.conversation import Conversation
from search_engine.validation import validate_citations, remove_invalid_citations

from colorama import Fore, Style, init

init(autoreset=True)

def display_sources(results):
    print()
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + "                         SOURCES")
    print(Fore.MAGENTA + "=" * 60)
    print()

    for number, result in enumerate(results, start=1):

        title = result.get("title", "Unknown")
        url = result.get("url", "Unknown")
        content = result.get("content", "")
        score = result.get("score", 0)

        snippet = content[:200].replace("\n", " ")

        print(
            Fore.CYAN +
            f"[{number}] {title}"
        )

        print(
            Fore.YELLOW +
            f"     Relevance score: {score:.2f}"
        )

        print(
            Fore.BLUE +
            f"     {url}"
        )

        print(
            Fore.WHITE +
            f"     {snippet}..."
        )

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
    print()
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "              CUSTOM SEARCH ENGINE")
    print(Fore.CYAN + "=" * 60)
    print()

    print(Fore.WHITE + "Search the web and get AI-generated answers.")
    print(
        Fore.YELLOW +
        "Type 'help' for commands or 'exit' to quit."
    )

    print()

    while True:
        query = input(Fore.CYAN + "Search > " + Style.RESET_ALL).strip()

        if query.lower() == "exit":
            print()
            print(Fore.CYAN + "Goodbye!")
            break

        if query.lower() == "help":
            display_help()
            continue

        if query.lower() == "clear":
            conversation.clear()
            print()
            print(Fore.GREEN + "Conversation history cleared.")
            print()
            continue

        if not query:
            print(Fore.RED + "Please enter a search query.")
            print()
            continue

        print()
        print(Fore.YELLOW + "Searching the web...")
        print()

        contextual_query = make_contextual_query(
        query,
        conversation.get_history()
        )

        if contextual_query != query:
            print(f"Rewritten query: {contextual_query}")

        search_queries = analyze_query(contextual_query)

        all_results = []

        for search_query in search_queries:
            print(Fore.BLUE +f"Searching for: {search_query}")
            results = search_web(search_query)
            all_results.extend(results)

        if not all_results:
            print(Fore.RED + "\nNo search results were found.")
            print(Fore.YELLOW + "Try rephrasing your question.\n")
            continue

        ranked_results = rank_results(
            all_results,
            contextual_query
        )

        print(Fore.GREEN + f"Found {len(all_results)} search results.")
        print(Fore.GREEN + f"Using the top {len(ranked_results)} results.")
        print(Fore.YELLOW + "Generating answer...")
        print()

        answer = generate_answer(
            query, 
            ranked_results,
            conversation.get_history()
        )

        if answer.startswith("Unable to generate an AI answer:"):
            print("\n" + answer)
            print()
            continue

        valid_citations, invalid_citations = validate_citations(
            answer,
            ranked_results
        )

        if valid_citations:
            unique_citations = sorted(set(valid_citations))

            print(
                f"Verified citations: "
                f"{', '.join(f'[{c}]' for c in unique_citations)}"
            )

        if invalid_citations:
            print(
                f"Warning: invalid citations found: "
                f"{invalid_citations}"
            )

            answer = remove_invalid_citations(
                answer,
                ranked_results
            )

        conversation.add_message("user", query)
        conversation.add_message("assistant", answer)

        print()
        print(Fore.GREEN + "=" * 60)
        print(Fore.GREEN + "                          ANSWER")
        print(Fore.GREEN + "=" * 60)
        print()

        print(Fore.WHITE + answer)

        display_sources(ranked_results)


if __name__ == "__main__":
    main()