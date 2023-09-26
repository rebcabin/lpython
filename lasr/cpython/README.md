# LASR

is based on
[MASR](https://github.com/rebcabin/masr). It's a
type-checker for ASR.

# Pull

```bash
git clone https://github.com/rebcabin/lpython
cd lpython
git checkout brian-lasr
```

# Build & Run

```c
mamba env create -f environment_unix.yml --force
conda activate lp
conda install pytest
conda install pydantic
pytest
pytest -s
```
