"""Run the orchestrator in the command line.
"""
import argparse

from colorama import Fore, Style

from your_assistant.core.orchestrator import *

ORCHESTRATORS = {
    "ChatGPT": ChatGPTOrchestrator,
    "RevChatGPT": RevChatGPTOrchestrator,
    "RevBard": RevBardOrchestrator,
    "QA": QAOrchestrator,
    "KnowledgeIndex": KnowledgeIndexOrchestrator,
}


# Define the function that initialize the argument parser that has the param of the prompt.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Orchestrator")
    parser.add_argument(
        "-v",
        "--verbose",
        default=True,
        action="store_true",
        help="Whether to print the verbose output.",
    )

    subparsers = parser.add_subparsers(
        help="orchestrator", dest="orchestrator", required=True
    )

    for name, orchestrator in ORCHESTRATORS.items():
        subparser = subparsers.add_parser(name)
        orchestrator.add_arguments_to_parser(subparser)  # type: ignore

    args = parser.parse_args()
    return args


# Define the function that runs the orchestrator.
def run():
    args = parse_args()
    orchestrator_cls = ORCHESTRATORS[args.orchestrator]
    # orchestrator_cls = getattr(sys.modules[__name__], args.orchestrator)
    orchestrator = orchestrator_cls.create_from_args(args)

    print(f"You are using {args.orchestrator}.")
    # Init path as user_input if is KnowledgeIndexOrchestrator.
    if args.orchestrator == "KnowledgeIndex":
        response = orchestrator.process(args)
        print(response)
    elif args.orchestrator in [
        "ChatGPT",
        "RevChatGPT",
        "RevBard",
        "QA",
    ]:
        # Init prompt as user_input if is RevChatGPTOrchestrator, RevBardOrchestrator, QAOrchestrator.
        while True:
            try:
                user_input = input(
                    Fore.GREEN
                    + "\nEnter your conversation (exit with ctrl + C): "
                    + Style.RESET_ALL
                )
                args.prompt = user_input
                response = orchestrator.process(args)
                print(response)
            except KeyboardInterrupt:
                exit(0)
    else:
        raise ValueError("The orchestrator is not supported.")


if __name__ == "__main__":
    run()
