import os
import openai
from flask import flash

openai.api_key = os.environ.get("OPENAI_API_KEY")

class AIArtGenerator:

  def __init__(self, prompt, n, size) -> None:
      
      self.prompt = prompt
      self.n = n
      self.size = size

  def generate_art(self):
      
      try:
          
        generate = openai.Image.create(
          prompt=self.prompt,
          n=self.n,
          size=self.size
        )

      except Exception as e:

        flash(f"Error: {str(e)}", "error")
        return None

      response = generate['data']

      return response

  def photo_to_art(self, image):
      
      try:
          
        generate = openai.Image.create_edit(
          image=image,
          prompt=self.prompt,
          n=self.n,
          size=self.size
        )

      except Exception as e:

        flash(f"Error: {str(e)}", "error")
        return None

      response = generate['data']

      return response
  
  def image_variation(self, image):
      
      try:
          
        generate = openai.Image.create_variation(
          image=image,
          n=self.n,
          size=self.size
        )

      except Exception as e:

        flash(f"Error: {str(e)}", "error")
        return None

      response = generate['data']

      return response