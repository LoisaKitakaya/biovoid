import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

response = openai.Image.create(
  prompt="nostalgic city skyline at a sunset in a dystopian future. Style: Realism",
  n=3,
  size="256x256"
)
image_url = response['data']
for image in image_url:

    print(image.url)