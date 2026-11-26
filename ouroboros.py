"""Geração de peptídeos aleatórios em formato FASTA."""

import argparse
import random
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, Iterator, Optional, TextIO


AMINOACIDOS = "ACDEFGHIKLMNPQRSTVWY"


def gerar_peptideos(
    quantidade: int, tamanho_min: int, tamanho_max: int, *, semente: Optional[int] = None
) -> Iterator[str]:
    """Sorteia cada comprimento e cada aminoácido com distribuição uniforme."""
    if quantidade < 1:
        raise ValueError("a quantidade deve ser pelo menos 1")
    if not 2 <= tamanho_min <= tamanho_max <= 50:
        raise ValueError(
            "use comprimentos entre 2 e 50 aminoácidos, do menor para o maior"
        )

    sorteio = random.Random(semente)
    for _ in range(quantidade):
        tamanho = sorteio.randint(tamanho_min, tamanho_max)
        yield "".join(sorteio.choice(AMINOACIDOS) for _ in range(tamanho))


def escrever_fasta(sequencias: Iterable[str], arquivo: TextIO) -> None:
    for indice, sequencia in enumerate(sequencias, start=1):
        arquivo.write(f">pep_{indice:04d}\n{sequencia}\n")


def salvar_fasta(sequencias: Iterable[str], destino: Path) -> None:
    """Substitui o destino somente depois de gravar o lote completo."""
    with TemporaryDirectory(dir=destino.parent) as pasta:
        temporario = Path(pasta) / "lote.fasta"
        with temporario.open("w", encoding="ascii", newline="\n") as arquivo:
            escrever_fasta(sequencias, arquivo)
        temporario.replace(destino)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m ouroboros",
        description="Gera sequências de peptídeos curtos em formato FASTA.",
    )
    parser.add_argument(
        "-n", "--quantidade", type=int, default=5, metavar="N",
        help="quantidade de sequências (padrão %(default)s)",
    )
    parser.add_argument(
        "-t", "--tamanho", type=int, nargs="+", default=(5, 12), metavar="AA",
        help="um comprimento fixo ou dois limites inclusivos entre 2 e 50 (padrão de 5 a 12)",
    )
    parser.add_argument(
        "--semente", type=int, metavar="N", help="semente inteira para reproduzir o lote",
    )
    parser.add_argument(
        "-o", "--saida", type=Path, metavar="ARQUIVO",
        help="caminho do arquivo FASTA de destino (por padrão, escreve no terminal)",
    )
    args = parser.parse_args()
    if len(args.tamanho) > 2:
        parser.error("--tamanho aceita um comprimento fixo ou dois limites")

    sequencias = gerar_peptideos(
        args.quantidade, args.tamanho[0], args.tamanho[-1], semente=args.semente
    )
    try:
        if args.saida is None:
            escrever_fasta(sequencias, sys.stdout)
        else:
            salvar_fasta(sequencias, args.saida)
    except ValueError as erro:
        parser.error(str(erro))
    except OSError as erro:
        parser.exit(1, f"Falha ao escrever o FASTA. {erro}\n")


if __name__ == "__main__":
    main()
