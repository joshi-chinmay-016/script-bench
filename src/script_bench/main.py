"""CLI entry point for Script Bench."""

import argparse
import json
from pathlib import Path
import sys

# Ensure project root is on sys.path when executed directly as a file
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from pydantic import ValidationError

from src.script_bench.generator import ScriptGenerator
from src.script_bench.models import ScriptRequest
from src.script_bench.provider import GeminiProvider, ProviderError
from src.script_bench.validator import ScriptValidationError


def main() -> None:
    """Parse arguments or prompt interactively, then execute generation."""
    if len(sys.argv) == 1:
        # Step-by-step interactive mode when run without command-line arguments
        try:
            print("--- Script Bench Generation ---")
            niche = input("1. Enter niche (e.g. personal finance): ").strip()
            topic = input("2. Enter topic: ").strip()
            seconds_input = input("3. Enter target runtime in seconds (15-180): ").strip()
            target_seconds = int(seconds_input)
        except ValueError:
            print("Error: Target runtime must be an integer.", file=sys.stderr)
            sys.exit(1)
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.", file=sys.stderr)
            sys.exit(1)
    else:
        # Command-line flag mode
        parser = argparse.ArgumentParser(
            description="Script Bench: Production-minded short-form video script generator."
        )
        parser.add_argument(
            "--niche",
            type=str,
            required=True,
            help="Creator niche (e.g. 'personal finance')",
        )
        parser.add_argument(
            "--topic",
            type=str,
            required=True,
            help="Video topic or idea",
        )
        parser.add_argument(
            "--target-seconds",
            type=int,
            required=True,
            help="Target video runtime in seconds (15-180)",
        )

        args = parser.parse_args()
        niche = args.niche
        topic = args.topic
        target_seconds = args.target_seconds

    try:
        request = ScriptRequest(
            niche=niche,
            topic=topic,
            target_seconds=target_seconds,
        )
    except ValidationError as e:
        print(f"Input validation error:\n{e}", file=sys.stderr)
        sys.exit(1)

    try:
        provider = GeminiProvider()
        generator = ScriptGenerator(provider=provider)
        output = generator.generate(request)
        print(json.dumps(output.model_dump(), indent=2, ensure_ascii=False))
    except (ProviderError, ScriptValidationError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
