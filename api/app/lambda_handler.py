"""
AWS Lambda entry point. Wraps the FastAPI app behind a Lambda Function URL.
CloudFront forwards /api/* to this function, so the prefix is stripped.
"""

from mangum import Mangum

from app.main import create_app

handler = Mangum(create_app(), lifespan="off", api_gateway_base_path="/api")
