import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ouroboros import save_fasta


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "ouroboros", *arguments],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )


class TestPeptideGenerator(unittest.TestCase):
    def test_count_alphabet_and_inclusive_bounds(self):
        result = run_cli("-n", "1000", "-l", "2", "50", "--seed", "7")
        self.assertEqual(result.returncode, 0, result.stderr)
        sequences = result.stdout.splitlines()[1::2]
        self.assertEqual(len(sequences), 1000)
        self.assertEqual({len(seq) for seq in sequences}, set(range(2, 51)))
        self.assertEqual(set("".join(sequences)), set("ACDEFGHIKLMNPQRSTVWY"))

    def test_seeded_readme_example(self):
        result = run_cli("--count", "2", "--length", "8", "--seed", "42")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, ">pep_0001\nAKIIFEVD\n>pep_0002\nCADHITYA\n")

    def test_defaults_and_file_output(self):
        terminal = run_cli("--seed", "0")
        self.assertEqual(terminal.returncode, 0, terminal.stderr)
        lines = terminal.stdout.splitlines()
        self.assertEqual(lines[::2], [f">pep_{i:04d}" for i in range(1, 6)])
        self.assertEqual(len(lines), 10)
        self.assertTrue(all(5 <= len(seq) <= 12 for seq in lines[1::2]))

        with TemporaryDirectory() as folder:
            destination = Path(folder) / "sample β peptides.fasta"
            destination.write_bytes(b"previous file\n")
            result = run_cli("--seed", "0", "--output", str(destination))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(destination.read_bytes(), terminal.stdout.encode("ascii"))

    def test_invalid_arguments(self):
        for arguments in (
            ("-n", "0"),
            ("-l", "1"),
            ("-l", "51"),
            ("-l", "9", "4"),
            ("-l", "3", "4", "5"),
        ):
            with self.subTest(arguments=arguments):
                result = run_cli(*arguments)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr.strip())

    def test_interrupted_write_preserves_existing_file(self):
        def interrupted_batch():
            yield "AC"
            raise OSError("interrupted write")

        with TemporaryDirectory() as folder:
            destination = Path(folder) / "batch.fasta"
            destination.write_bytes(b"original\n")
            with self.assertRaises(OSError):
                save_fasta(interrupted_batch(), destination)
            self.assertEqual(destination.read_bytes(), b"original\n")
            self.assertEqual(list(Path(folder).iterdir()), [destination])
