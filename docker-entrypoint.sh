#!/bin/sh
python -m uvicorn index:api --host 0.0.0.0 --port 8080
