#!/bin/bash
uv run python -m main --runner=apache_beam.runners.render.RenderRunner --render_output=pipeline_graph.png