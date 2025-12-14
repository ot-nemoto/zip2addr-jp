import argparse
import json
from typing import Optional

from .api import Zip2AddrService


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lookup Japanese address from postal code"
    )
    parser.add_argument("postal", help="Postal code to lookup (with or without hyphen)")
    parser.add_argument("--db", help="Path to sqlite DB file (optional)")
    args = parser.parse_args(argv)

    service = Zip2AddrService(db_path=args.db)
    res = service.lookup(args.postal)
    if not res:
        print(json.dumps(None))
        return 1
    print(json.dumps(res.to_dict(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
