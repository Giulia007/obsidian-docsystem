from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import os
import yaml
from datetime import date, datetime

app = FastAPI()

DOCS_DIR = "docs"  # Project-relative docs directory


def extract_yaml_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines or lines[0].strip() != "---":
            return {}

        yaml_block = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            yaml_block.append(line)

        data = yaml.safe_load("".join(yaml_block)) or {}
        return data if isinstance(data, dict) else {}

    except Exception:
        return {}


def serialize_metadata(metadata):
    if isinstance(metadata, dict):
        return {k: serialize_metadata(v) for k, v in metadata.items()}
    if isinstance(metadata, list):
        return [serialize_metadata(v) for v in metadata]
    if isinstance(metadata, (date, datetime)):
        return metadata.isoformat()
    return metadata


@app.get("/api/metadata")
async def get_metadata(
    file: str = Query(..., description="Relative path under docs/, e.g. 'system/Documentation Structure MOC.md'")
):
    filepath = os.path.join(DOCS_DIR, file)

    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File not found.")

    metadata = extract_yaml_metadata(filepath)

    if not metadata:
        raise HTTPException(status_code=404, detail="No YAML frontmatter found.")

    return JSONResponse(content=serialize_metadata(metadata))
