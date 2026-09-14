"""Command-line entry point for the RegModelTrace v1 service."""

import argparse
import json


def main():
    parser = argparse.ArgumentParser(prog="regmodeltrace")
    sub = parser.add_subparsers(dest="command", required=True)
    ask_parser = sub.add_parser("ask", help="Answer one question using the local RAG system")
    ask_parser.add_argument("question")
    serve_parser = sub.add_parser("serve", help="Start the local HTTP service")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.command == "ask":
        from .service import ask

        print(json.dumps(ask(args.question), indent=2, ensure_ascii=False))
        return

    import uvicorn

    uvicorn.run("regmodeltrace.server:app", host=args.host, port=args.port, workers=1)


if __name__ == "__main__":
    main()

