import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ouroboros import salvar_fasta


RAIZ = Path(__file__).resolve().parents[1]


def executar(*argumentos: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "ouroboros", *argumentos],
        cwd=RAIZ, capture_output=True, text=True, encoding="utf-8",
    )


class TestGerador(unittest.TestCase):
    def test_quantidade_alfabeto_e_limites_inclusivos(self):
        resultado = executar("-n", "1000", "-t", "2", "50", "--semente", "7")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        sequencias = resultado.stdout.splitlines()[1::2]
        self.assertEqual(len(sequencias), 1000)
        self.assertEqual({len(seq) for seq in sequencias}, set(range(2, 51)))
        self.assertEqual(set("".join(sequencias)), set("ACDEFGHIKLMNPQRSTVWY"))

    def test_exemplo_reproduzivel_do_readme(self):
        resultado = executar("--quantidade", "2", "--tamanho", "8", "--semente", "42")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertEqual(resultado.stdout, ">pep_0001\nAKIIFEVD\n>pep_0002\nCADHITYA\n")

    def test_padrao_e_saida_em_arquivo(self):
        terminal = executar("--semente", "0")
        self.assertEqual(terminal.returncode, 0, terminal.stderr)
        linhas = terminal.stdout.splitlines()
        self.assertEqual(linhas[::2], [f">pep_{i:04d}" for i in range(1, 6)])
        self.assertEqual(len(linhas), 10)
        self.assertTrue(all(5 <= len(seq) <= 12 for seq in linhas[1::2]))

        with TemporaryDirectory() as pasta:
            destino = Path(pasta) / "meus peptídeos.fasta"
            destino.write_bytes(b"arquivo anterior\n")
            resultado = executar("--semente", "0", "--saida", str(destino))
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertEqual(resultado.stdout, "")
            self.assertEqual(destino.read_bytes(), terminal.stdout.encode("ascii"))

    def test_rejeita_argumentos_invalidos(self):
        for argumentos in (
            ("-n", "0"), ("-t", "1"), ("-t", "51"), ("-t", "9", "4"), ("-t", "3", "4", "5"),
        ):
            with self.subTest(argumentos=argumentos):
                resultado = executar(*argumentos)
                self.assertEqual(resultado.returncode, 2, resultado.stderr)
                self.assertEqual(resultado.stdout, "")
                self.assertTrue(resultado.stderr.strip())

    def test_gravacao_interrompida_preserva_arquivo(self):
        def lote_interrompido():
            yield "AC"
            raise OSError("gravação interrompida")

        with TemporaryDirectory() as pasta:
            destino = Path(pasta) / "lote.fasta"
            destino.write_bytes(b"original\n")
            with self.assertRaises(OSError):
                salvar_fasta(lote_interrompido(), destino)
            self.assertEqual(destino.read_bytes(), b"original\n")
            self.assertEqual(list(Path(pasta).iterdir()), [destino])
