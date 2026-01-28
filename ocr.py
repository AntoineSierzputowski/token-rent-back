import base64
import io
import json
import re
from PIL import Image
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
import torch

# Configuration
MODEL_ID = "Qwen/Qwen2-VL-2B-Instruct" 

class ValidationAI:
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        if self.model is None:
            print(f"Loading model: {MODEL_ID} on {self.device}...")
            # Note: trust_remote_code=True is often needed for Qwen-VL
            self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                MODEL_ID, 
                torch_dtype=torch.float16 if self.device == "cuda" else "auto",
                device_map="auto"
            )
            self.processor = AutoProcessor.from_pretrained(MODEL_ID)
            print("Model loaded successfully.")

    def decode_image(self, base64_string: str) -> Image.Image:
        try:
            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data))
            return image
        except Exception as e:
            raise ValueError(f"Invalid image data: {e}")

    def analyze_id_card(self, base64_image: str) -> dict:
        self.load_model()
        image = self.decode_image(base64_image)
        
        prompt = "Extract the following fields from the ID card image in JSON format: last_name, first_name, date_of_birth (YYYY-MM-DD)."
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.device)

        generated_ids = self.model.generate(**inputs, max_new_tokens=128)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]
        
        # Parse JSON from output
        try:
            # Naive JSON extraction
            json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                return data
            else:
                # Fallback manual parsing if model doesn't output pure JSON
                # This is a placeholder for more robust parsing
                return {} 
        except Exception as e:
            print(f"Failed to parse OCR output: {output_text} error: {e}")
            return {}

    def analyze_salary_slip(self, base64_image: str) -> float:
        self.load_model()
        image = self.decode_image(base64_image)
        
        prompt = "Extract the net salary amount from this salary slip. Output only the number."
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.device)

        generated_ids = self.model.generate(**inputs, max_new_tokens=50)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]
        
        # Parse float
        try:
            # Remove currency symbols and non-numeric chars except dot
            clean_text = re.sub(r'[^\d.]', '', output_text)
            return float(clean_text)
        except:
            return 0.0

from qwen_vl_utils import process_vision_info

ocr_service = ValidationAI()
