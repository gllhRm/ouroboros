# Ouroboros

Ouroboros gera pequenos peptídeos aleatórios em formato FASTA. Cada letra da sequência representa um aminoácido sorteado de forma independente entre os 20 aminoácidos canônicos, todos com a mesma probabilidade.

## Gerar um lote

Na pasta do repositório, execute o comando abaixo com Python 3.9 ou superior. O gerador usa apenas a biblioteca padrão. Este exemplo gera dois peptídeos de oito aminoácidos cada.

```sh
python -m ouroboros --quantidade 2 --tamanho 8 --semente 42
```

```text
>pep_0001
AKIIFEVD
>pep_0002
CADHITYA
```

Para reproduzir o lote, guarde a semente e os parâmetros junto com a versão do Python e o commit do projeto. O sorteio admite repetições de aminoácidos e de sequências.

## Variar o comprimento e salvar em arquivo

O comando abaixo gera 20 peptídeos e grava o resultado em `peptideos.fasta`. Para cada sequência, o comprimento é sorteado entre 6 e 10 aminoácidos. Todos os inteiros da faixa têm a mesma probabilidade, incluindo os dois limites.

```sh
python -m ouroboros --quantidade 20 --tamanho 6 10 --saida peptideos.fasta
```

| Opção | Uso | Padrão |
| --- | --- | --- |
| `-n`, `--quantidade` | Número de peptídeos, a partir de 1 | 5 |
| `-t`, `--tamanho` | Um comprimento fixo ou os comprimentos mínimo e máximo, entre 2 e 50 aminoácidos | 5 a 12 |
| `--semente` | Inteiro que permite repetir o sorteio | Semente automática |
| `-o`, `--saida` | Caminho do arquivo FASTA. Um arquivo existente é substituído quando o lote fica pronto | Terminal |

## Executar os testes

```sh
python -m unittest discover -s tests -v
```

O GitHub Actions executa a mesma suíte a cada push ou pull request.
