"""
Simple CLI to manage Azure AI Search indexes and indexers.

Commands:
  - indexes: create or update indexes
  - indexers: create or update data sources, skillsets, and indexers; then optionally run
  - run: trigger indexers once
  - status: show indexer statuses
"""

import argparse
import sys
from typing import NoReturn

from dotenv import load_dotenv


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="core.cli", description="Manage Azure AI Search resources")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # indexes
    p_indexes = subparsers.add_parser("indexes", help="Create or update search indexes")
    p_indexes.add_argument("--reset", action="store_true", help="Delete existing indexes first")
    p_indexes.add_argument("--verbose", action="store_true", help="Verbose logging")

    # indexers
    p_indexers = subparsers.add_parser("indexers", help="Create or update data sources, skillsets, and indexers; then run")
    p_indexers.add_argument("--reset", action="store_true", help="Delete existing resources first")
    p_indexers.add_argument("--verbose", action="store_true", help="Verbose logging")

    # run
    p_run = subparsers.add_parser("run", help="Trigger indexers once")
    p_run.add_argument("--verbose", action="store_true", help="Verbose logging")

    # status
    p_status = subparsers.add_parser("status", help="Show indexer statuses")
    p_status.add_argument("--verbose", action="store_true", help="Verbose logging")

    return parser.parse_args(argv)


def _cmd_indexes(reset: bool, verbose: bool) -> None:
    from core.search.indexes import create_indexes
    create_indexes(reset=reset, verbose=verbose)


def _cmd_indexers(reset: bool, verbose: bool) -> None:
    from core.search.indexers import setup_azure_indexers
    setup_azure_indexers(reset=reset, verbose=verbose)


def _cmd_run(verbose: bool) -> None:
    from core.search.indexers import AzureIndexerManager
    m = AzureIndexerManager()
    if verbose:
        print("Triggering items-indexer and authors-indexer ...")
    m.client.run_indexer("items-indexer")
    m.client.run_indexer("authors-indexer")
    print("Triggered items-indexer and authors-indexer")


def _cmd_status(verbose: bool) -> None:
    from core.search.indexers import AzureIndexerManager
    m = AzureIndexerManager()
    items = m.client.get_indexer_status("items-indexer")
    authors = m.client.get_indexer_status("authors-indexer")
    if verbose:
        print("Items indexer status:")
    print(items)
    if verbose:
        print("\nAuthors indexer status:")
    print(authors)


def main(argv: list[str] | None = None) -> NoReturn:
    load_dotenv()
    ns = _parse_args(argv if argv is not None else sys.argv[1:])

    if ns.command == "indexes":
        _cmd_indexes(reset=ns.reset, verbose=ns.verbose)
    elif ns.command == "indexers":
        _cmd_indexers(reset=ns.reset, verbose=ns.verbose)
    elif ns.command == "run":
        _cmd_run(verbose=ns.verbose)
    elif ns.command == "status":
        _cmd_status(verbose=ns.verbose)
    else:
        raise SystemExit(2)

    raise SystemExit(0)


if __name__ == "__main__":
    main()


