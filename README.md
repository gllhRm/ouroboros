# Ouroboros

Ouroboros generates short random peptides in FASTA format. Each position is sampled independently from the 20 canonical amino acids with equal probability. You can generate fixed-length peptides or sample a length for each sequence.

## Set up with Anaconda

In Anaconda Prompt or a terminal with Conda available, change to the repository root. Create and activate the project environment there.

```sh
conda env create --file environment.yml
conda activate ouroboros
```

The environment pins Python and the Jupyter tools and installs this checkout as an editable package. Both the notebooks and the CLI import the same generator. To update an existing environment after pulling changes, run `conda env update --name ouroboros --file environment.yml` from the repository root. [Environment definition](environment.yml)

## Jupyter notebooks

Start JupyterLab from the active environment and use its **Python 3 (ipykernel)** kernel.

```sh
jupyter lab
```

- Set the batch size, length range, and seed, preview the FASTA records, and save them to a file. [Generate a peptide batch](notebooks/generate_peptides.ipynb)
- Sample a batch and count how many peptides have each length. This notebook runs independently and keeps only the counts in memory. [Inspect peptide lengths](notebooks/inspect_lengths.ipynb)

## Command line

Generate two peptides of eight amino acids with a fixed seed.

```sh
python -m ouroboros --count 2 --length 8 --seed 42
```

```text
>pep_0001
AKIIFEVD
>pep_0002
CADHITYA
```

To write 20 peptides to a file, give a minimum and a maximum length. Each integer from 6 through 10 has the same probability of being sampled.

```sh
python -m ouroboros --count 20 --length 6 10 --output peptides.fasta
```

| Option | Meaning | Default |
| --- | --- | --- |
| `-n`, `--count` | Number of peptides, at least 1 | 5 |
| `-l`, `-t`, `--length` | One fixed length or two inclusive bounds, from 2 to 50 amino acids | 5 to 12 |
| `--seed` | Integer seed for reproducing a batch | Automatic |
| `-o`, `--output` | FASTA file to replace once the batch is complete | Standard output |

To reproduce a batch, record the seed, count, length bounds, Python version, and project commit. Amino acids and entire sequences can repeat.

## Run the checks

Run these commands in the active environment. GitHub Actions uses the same environment file to test the CLI and execute both notebooks.

```sh
python -m unittest discover -s tests -v
jupyter nbconvert --to notebook --execute --output-dir build/executed notebooks/*.ipynb
```

## Authors

Co-authored by Guilherme Baiocchi and [OpenAI Codex](https://github.com/codex).
