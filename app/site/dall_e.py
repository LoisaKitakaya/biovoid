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

      except:

        flash("Something went wrong", "error")
        return None

      response = generate['data']

      return response

  def photo_to_image(self):
      
      try:
          
        generate = openai.Image.create(
          prompt=self.prompt,
          n=self.n,
          size=self.size
        )

      except:

        flash("Something went wrong", "error")
        return None

      response = generate['data']

      return response

  def edit_image(self):
      
      try:
          
        generate = openai.Image.create(
          prompt=self.prompt,
          n=self.n,
          size=self.size
        )

      except:

        flash("Something went wrong", "error")
        return None

      response = generate['data']

      return response