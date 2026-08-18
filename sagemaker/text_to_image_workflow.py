# Text to Image with Generative AI
# Converted from the provided SageMaker notebook for repository-friendly source review.

import boto3
import json
import sagemaker
from sagemaker import get_execution_role

aws_role = get_execution_role()
aws_region = boto3.Session().region_name
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

for bucket in s3.buckets.all():
    if bucket.name.startswith('cloudage-text-to-image-webapp'):
        mybucket = bucket.name
        print(mybucket)

sess = sagemaker.Session(default_bucket=mybucket)

model_id, model_version = "model-txt2img-stabilityai-stable-diffusion-v2", "1.2.*"

from sagemaker import image_uris, model_uris, script_uris
from sagemaker.model import Model
from sagemaker.predictor import Predictor
from sagemaker.utils import name_from_base

endpoint_name = name_from_base(f"cloudage-endpoint-text-to-image-{model_id}")
model_name = name_from_base("cloudage-model-")
inference_instance_type = "ml.g5.2xlarge"

deploy_image_uri = image_uris.retrieve(
    region=None,
    framework=None,
    image_scope="inference",
    model_id=model_id,
    model_version=model_version,
    instance_type=inference_instance_type,
    sagemaker_session=sess,
)

deploy_source_uri = script_uris.retrieve(
    model_id=model_id, model_version=model_version, script_scope="inference"
)

model_uri = model_uris.retrieve(
    model_id=model_id,
    model_version=model_version,
    model_scope="inference",
    sagemaker_session=sess,
)

env = {"MMS_MAX_RESPONSE_SIZE": "20000000"}

model = Model(
    image_uri=deploy_image_uri,
    source_dir=deploy_source_uri,
    model_data=model_uri,
    entry_point="inference.py",
    role=aws_role,
    name=model_name,
    env=env,
    sagemaker_session=sess,
)

base_model_predictor = model.deploy(
    initial_instance_count=1,
    instance_type=inference_instance_type,
    endpoint_name=endpoint_name,
    model_name=model_name,
)

model_predictor = Predictor(endpoint_name=endpoint_name)

import matplotlib.pyplot as plt
import numpy as np


def query(model_predictor, text):
    encoded_text = text.encode("utf-8")
    return model_predictor.predict(
        encoded_text,
        {"ContentType": "application/x-text", "Accept": "application/json"},
    )


def parse_response(query_response):
    response_dict = json.loads(query_response)
    return response_dict["generated_image"], response_dict["prompt"]


def display_img_and_prompt(img, prmpt):
    plt.figure(figsize=(12, 12))
    plt.imshow(np.array(img))
    plt.axis("off")
    plt.title(prmpt)
    plt.show()

text = "cottage in impressionist style"
query_response = query(model_predictor, text)
img, prmpt = parse_response(query_response)
display_img_and_prompt(img, prmpt)

payload = {
    "prompt": "astronaut on a horse",
    "width": 512,
    "height": 512,
    "num_images_per_prompt": 1,
    "num_inference_steps": 50,
    "guidance_scale": 7.5,
}


def query_endpoint_with_json_payload(model_predictor, payload):
    encoded_payload = json.dumps(payload).encode("utf-8")
    return model_predictor.predict(
        encoded_payload,
        {"ContentType": "application/json", "Accept": "application/json"},
    )


def parse_response_multiple_images(query_response):
    response_dict = json.loads(query_response)
    return response_dict["generated_images"], response_dict["prompt"]

query_response = query_endpoint_with_json_payload(model_predictor, payload)
generated_images, prompt = parse_response_multiple_images(query_response)

for img in generated_images:
    display_img_and_prompt(img, prompt)

# Clean up the SageMaker endpoint when finished:
# model_predictor.delete_model()
# model_predictor.delete_endpoint()
