FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.4.17 /uv /bin/uv
WORKDIR /usr/src/cbis_ddsm_dataloader
COPY pyproject.toml /usr/src/cbis_ddsm_dataloader/pyproject.toml
COPY uv.lock  /usr/src/cbis_ddsm_dataloader/uv.lock
COPY datasets /usr/src/cbis_ddsm_dataloader/datasets
COPY examples /usr/src/cbis_ddsm_dataloader/examples
COPY resources /usr/src/cbis_ddsm_dataloader/resources
COPY transforms /usr/src/cbis_ddsm_dataloader/transforms
COPY utils /usr/src/cbis_ddsm_dataloader/utils
COPY config.json /usr/src/cbis_ddsm_dataloader/config.json
COPY ddsm_dataset_factory.py /usr/src/cbis_ddsm_dataloader/ddsm_dataset_factory.py
COPY pyproject.toml /usr/src/cbis_ddsm_dataloader/pyproject.toml
COPY setup.py /usr/src/cbis_ddsm_dataloader/setup.py
RUN uv sync --frozen
ENV PATH="/usr/src/cbis_ddsm_dataloader/.venv/bin:$PATH"
CMD ["python", "setup.py", "-c", "config.json", "--output", "output"]