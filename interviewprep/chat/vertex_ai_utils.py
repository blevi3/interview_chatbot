import os
import vertexai
from vertexai.language_models import TextGenerationModel
from django.conf import settings

# Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS

# Initialize Vertex AI
project_id = "static-booster-423512-j6"
location = "us-central1"  # or other supported location

vertexai.init(project=project_id, location=location)

def generate_text(prompt):
    parameters = {
        "temperature": 0.7,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }
    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(prompt, **parameters)
    return response.text
