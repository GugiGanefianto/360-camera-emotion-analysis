# System Overview : real_cv_project

This application delivers real-time video (and image) analytics including object/person detection, demographic estimation, and emotion analysis.

## Architecture

- **Frontend:** Streamlit dashboard for data visualization.
- **Backend:** Modular Python application with YOLOv8, OpenCV, DeepFace.
- **Data Versioning:** With DVC and S3.
- **Experiment Tracking:** MLflow.
- **Containerization:** Docker for portability.
- **Deployment:** Kubernetes on AWS (EKS), CI/CD via Jenkins.
- **Orchestration:** Astro/Airflow for batch and pipeline jobs.

## MLOps Setup (Sample Steps)

1. **Initialize MLflow**
   - Install: `pip install mlflow`
   - Start MLflow UI: `mlflow ui`
2. **Enable DVC**
   - `dvc init`
   - `dvc remote add -d myremote s3://yourbucket/path`
   - To add data: `dvc add path/to/data`
3. **Run Tests**
   - `pytest tests/`
4. **Containerization and Deployment**
   - Build image: `docker build -t real_cv_project .`
   - Run local: `docker run -p 8501:8501 real_cv_project`
   - Deploy with Kubernetes using: `kubectl apply -f deployment/k8s/deployment.yaml`
