# Code Structure

## Directory Layout

| Directory           | Purpose                                        |
|---------------------|------------------------------------------------|
| app/                | Main program, pipelines, Streamlit UI          |
| app/detectors/      | All detection and classification models        |
| app/utils/          | Helper functions, drawing, input/output        |
| deployment/         | Docker, Kubernetes, CI/CD configuration        |
| docs/               | All documentation files                        |
| static/sample_videos| Demo media files for testing                   |
| tests/              | Unit/integration tests for application logic   |

## Flow Chart

**High-level Flow:**

1. User selects image/video stream via Streamlit UI.
2. Video processing pipeline loads frames.
3. Object and face detections are run, analytics data extracted.
4. Annotated graphics drawn on output frames and visualized in the web dashboard.

[Streamlit UI] -> [video_processor.py] -> [detectors/*] -> [draw.py] -> [Streamlit Output]