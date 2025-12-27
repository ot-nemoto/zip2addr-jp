import argparse
import json
import logging
from typing import Optional

from . import __version__
from .api import Zip2AddrService


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lookup Japanese address from postal code"
    )
    parser.add_argument(
        "postal", nargs="?", help="Postal code to lookup (with or without hyphen)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args(argv)

    # Check if postal code was provided
    if not args.postal:
        parser.error("postal code is required")

    # Configure logging based on debug flag
    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    service = Zip2AddrService()
    res = service.lookup(args.postal)
    if not res:
        print(json.dumps(None))
        return 1
    # Convert list of Zip2Addr objects to list of dicts
    results = [r.to_dict() for r in res]
    # Output single result as dict if only one, otherwise as list
    output = results[0] if len(results) == 1 else results
    print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
