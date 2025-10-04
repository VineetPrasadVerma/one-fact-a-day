# import requests

# YOUR_API_KEY = "your_api_key_here"

# r = requests.post(
#     'https://clipdrop-api.co/text-to-image/v1',
#     files={
#         'prompt': (None, 'There are more stars in the observable universe than all the grains of sand on every beach on Earth? Let that staggering number sink in! Wild, right?', 'text/plain')
#     },
#     headers={'x-api-key': ''}
# )

# if r.ok:
#     # Save the image locally
#     with open("vaporwave_dog.png", "wb") as f:
#         f.write(r.content)
#     print("Image saved as vaporwave_dog.png")
# else:
#     r.raise_for_status()

# import requests
# import os

# YOUR_API_KEY = "your_clipdrop_api_key"
# folder_path = "one_fact_a_day/images"
# os.makedirs(folder_path, exist_ok=True)

# script = "Did you know? Octopuses are absolutely incredible! They don't just have one heart like us; they actually have a whopping three! Two pump blood through their gills, and the third circulates it to their whole amazing body. Mind blown, right? Like, share, and subscribe for more!"
# intro = "Did you know?"
# outro = "Like, share, and subscribe for more!"

# # Step 1: Extract fact
# def get_fact(script, intro, outro):
#     start_idx = script.find(intro) + len(intro)
#     end_idx = script.find(outro)
#     fact_text = script[start_idx:end_idx].strip()
#     return fact_text

# fact = get_fact(script, intro, outro)

# # Step 2: Split fact into 2 parts for 2 images
# words = fact.split()
# mid = len(words) // 2
# fact_parts = [" ".join(words[:mid]), " ".join(words[mid:])]

# # Step 3: Generate images
# for i, part in enumerate(fact_parts):
#     print(part)
#     prompt = f"An artistic, eye-catching illustration of: {part}"
#     response = requests.post(
#         'https://clipdrop-api.co/text-to-image/v1',
#         files={'prompt': (None, prompt, 'text/plain')},
#         headers={'x-api-key': ""}
#     )
#     if response.ok:
#         file_path = os.path.join(folder_path, f"fact_image_{i+1}.png")
#         with open(file_path, "wb") as f:
#             f.write(response.content)
#         print(f"Saved: {file_path}")
#     else:
#         print("Failed to generate image:", response.status_code)


import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
import base64

load_dotenv()

folder_path = "assets/images"
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai_client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/", api_key=os.getenv("NEBIUS_API_KEY")
)

script = "Did you know? There are more stars in the observable universe than all the grains of sand on every beach on Earth? Let that staggering number sink in! Wild, right? Like, share, and subscribe for more!"
intro = "Did you know?"
outro = "Like, share, and subscribe for more!"


def get_fact(script, intro, outro):
    start_idx = script.find(intro) + len(intro)
    end_idx = script.find(outro)
    fact_text = script[start_idx:end_idx].strip()
    return fact_text


def convert_fact_into_image_generate_prompt(fact):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
          You are an image prompt generator.
          Your job is to take a fact and create two different text-to-image prompts.

          Rules:
          - Both prompts must come ONLY from the content of the fact.
          - The two prompts must NOT describe the same idea in different words.
          - Each should highlight a different aspect, object, or perspective of the fact.
          - Add styling cues so that the image looks eye-catching, vibrant, and crisp, with rich colors and clear details.
          - Do not invent unrelated objects or information.
          - Keep each prompt self-contained, simple, and descriptive.
          - Return the result as a list of 2 strings.

          Fact: {fact}
        """,
    )

    return response.text

  
def generate_image_from_prompt(text_to_image_prompt, idx):
  response = openai_client.images.generate(
      model="black-forest-labs/flux-dev",
      response_format="b64_json",
      extra_body={
          "response_extension": "png",
          "width": 576,
          "height": 1024,
          "num_inference_steps": 28,
          "negative_prompt": "",
          "seed": -1,
          "loras": None,
      },
      prompt=text_to_image_prompt,
  )
  
  # Convert response to dict
  response_json = response.to_dict()

  # Extract base64 image string
  image_base64 = response_json["data"][0]["b64_json"]

  # Decode base64 into raw bytes
  image_bytes = base64.b64decode(image_base64)

  file_path = os.path.join(folder_path, f"fact_image_{idx+1}.png")

  # Save locally
  with open(file_path, "wb") as f:
      f.write(image_bytes)

  print(f"✅ Image saved as {file_path}")

# txt_to_img_prompts_arr = convert_fact_into_image_generate_prompt(get_fact(script, intro, outro))

txt_to_img_prompts_arr = [
  "A breathtaking, vibrant nebula filled with an uncountable multitude of stars, sparkling like diamonds across the deep, rich indigo and violet expanse of the observable universe. Crisp, clear details with brilliant, eye-catching light. Ultra-high definition, cosmic grandeur, breathtaking, rich colors.",
  "A stunning, expansive aerial view of a pristine, golden beach stretching infinitely along the vivid blue ocean, representing all the grains of sand on Earth. The sand is depicted with rich, warm colors and intricate, crisp details, sparkling under a bright, eye-catching sunlight, emphasizing its vast, countless quantity. Ultra-realistic, vibrant, clear focus."
]

for idx, prompt in enumerate(txt_to_img_prompts_arr):
  generate_image_from_prompt(prompt, idx)
