# AWS Text-to-Image Generative AI

An end-to-end Generative AI application that generates images from text prompts using AWS services.

## Architecture

User → CloudFront → Amazon S3 → API Gateway → AWS Lambda → Amazon SageMaker → Stable Diffusion → Amazon S3 → CloudFront → Generated Image

## AWS Services

- Amazon SageMaker AI
- Stable Diffusion
- AWS Lambda
- Amazon API Gateway
- Amazon S3
- Amazon CloudFront
- AWS IAM

## Project Components

- `index.html` - Web frontend
- `start_process_function.py` - Starts asynchronous processing
- `endpoint_call_function.py` - Invokes the SageMaker endpoint
- `display_image.py` - Retrieves the generated image
- `text_2_image_with_generative_ai.ipynb` - SageMaker model workflow
- API Gateway configuration
- S3 and CloudFront policies

## Project Workflow

1. User enters a text prompt.
2. The frontend sends the request to API Gateway.
3. API Gateway invokes Lambda.
4. Lambda starts the image-generation process.
5. Lambda invokes the SageMaker endpoint.
6. Stable Diffusion generates the image.
7. The generated image is uploaded to Amazon S3.
8. CloudFront provides access to the generated image.
9. The frontend displays the generated image.

## Deployment Status

The AWS infrastructure used for this project has been decommissioned.

The repository contains the project source code, SageMaker notebook, Lambda functions, API Gateway configuration, frontend, and AWS policy examples required to recreate the application.

## Security

AWS credentials, secrets, and environment-specific configuration should not be committed to the repository.

## Author

Mahek Shaikh
