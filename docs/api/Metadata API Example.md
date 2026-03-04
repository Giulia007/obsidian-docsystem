---
title: Metadata API Example
created: 2025-12-29T18:46
updated: 2025-12-29T18:46
tags:
  - documentation
version:
status:
  - in progress
---
### Metadata API Example

#### Purpose

This example demonstrates the use of the documentation system's metadata API endpoint. It provides a simple, real-world illustration of how structured metadata can be accessed and integrated.

#### Endpoint

**GET** `/api/metadata`

**Query parameter:** `file` — Relative path under `docs/`, e.g. `system/Documentation Structure MOC.md`

#### Example Request
```
GET /api/metadata?file=system/Documentation%20Structure%20MOC.md
```

#### Example Success Response
```json
{
  "title": "Documentation Structure MOC",
  "created": "2025-11-27",
  "updated": "2025-11-27",
  "tags": [
    "documentation"
  ],
  "status": [
    "in progress"
  ],
  "version": null
}
```

#### Example Error Response
```json
{
  "detail": "File not found."
}
```

#### Notes

- The API is self-documented and testable via Swagger UI at `/docs`.