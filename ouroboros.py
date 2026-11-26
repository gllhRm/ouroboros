"""Generate short random peptides and write them in FASTA format."""

import argparse
import random
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, Iterator, Optional, TextIO


AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"


def generate_peptides(
    count: int, min_length: int, max_length: int, *, seed: Optional[int] = None
) -> Iterator[str]:
    """Yield peptides with uniformly sampled lengths and amino acids."""
    if count < 1:
        raise ValueError("count must be at least 1")
    if not 2 <= min_length <= max_length <= 50:
        raise ValueError(
            "lengths must be between 2 and 50 amino acids, with the minimum first"
        )

    rng = random.Random(seed)
    for _ in range(count):
        length = rng.randint(min_length, max_length)
        yield "".join(rng.choice(AMINO_ACIDS) for _ in range(length))


def write_fasta(sequences: Iterable[str], stream: TextIO) -> None:
    """Write one numbered FASTA record per sequence to a text stream."""
    for index, sequence in enumerate(sequences, start=1):
        stream.write(f">pep_{index:04d}\n{sequence}\n")


def save_fasta(sequences: Iterable[str], destination: Path) -> None:
    """Replace the destination after the entire batch has been written."""
    with TemporaryDirectory(dir=destination.parent) as folder:
        temporary = Path(folder) / "batch.fasta"
        with temporary.open("w", encoding="ascii", newline="\n") as stream:
            write_fasta(sequences, stream)
        temporary.replace(destination)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m ouroboros",
        description="Generate short random peptides in FASTA format.",
    )
    parser.add_argument(
        "-n", "--count", type=int, default=5, metavar="N",
        help="number of peptides to generate (default %(default)s)",
    )
    parser.add_argument(
        "-l", "--length", "-t", type=int, nargs="+", default=(5, 12), metavar="AA",
        help="one fixed length or two inclusive bounds from 2 to 50 (default 5 to 12)",
    )
    parser.add_argument(
        "--seed", type=int, metavar="N", help="integer seed for a reproducible batch",
    )
    parser.add_argument(
        "-o", "--output", type=Path, metavar="FILE",
        help="write FASTA to this file (default standard output)",
    )
    args = parser.parse_args()
    if len(args.length) > 2:
        parser.error("--length accepts one fixed length or two bounds")

    sequences = generate_peptides(
        args.count, args.length[0], args.length[-1], seed=args.seed
    )
    try:
        if args.output is None:
            write_fasta(sequences, sys.stdout)
        else:
            save_fasta(sequences, args.output)
    except ValueError as error:
        parser.error(str(error))
    except OSError as error:
        parser.exit(1, f"Could not write FASTA. {error}\n")


if __name__ == "__main__":
    main()
