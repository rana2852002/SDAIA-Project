
import argparse
from pathlib import Path
import sys


from src.csv_profiler.io import read_csv_rows
from src.csv_profiler.profiling import profile_rows
from src.csv_profiler.render import write_markdown, write_json 


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a profile report for a CSV file and write outputs to the 'outputs' folder."
    )
    parser.add_argument("path", type=Path, help="Path to the CSV file to profile.")
    
    args = parser.parse_args(argv)
    
    csv_path = args.path
    
    try:
        print(f"Reading CSV file: {csv_path}")
        rows = read_csv_rows(csv_path)

        print("Profiling rows...")
        report = profile_rows(rows)

 
    except FileNotFoundError as e:
        print(f"ERROR: File not found: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"ERROR: Data error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return 1

    
    base_name = csv_path.stem 
    output_dir = Path("outputs")
    output_markdown = output_dir / f"{base_name}_report.md"
    output_json = output_dir / f"{base_name}_report.json"
    
    print(f"Writing Markdown report to: {output_markdown}")
    write_markdown(report, output_markdown)
    
    print(f"Writing JSON report to: {output_json}")
    write_json(report, output_json)

    print("--- Profile generation complete! ---")
    return 0

if __name__ == "__main__":
    sys.exit(main())