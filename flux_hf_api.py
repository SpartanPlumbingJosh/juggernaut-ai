import os
import requests
from datetime import datetime

def generate_flux_image(prompt):
    """Generate image using Hugging Face FLUX API"""
    try:
        print(f"Generating FLUX image for: '{prompt}'")
        print("Using Hugging Face Inference API...")
        
        # Get HF token from environment variable
        hf_token = os.getenv('HF_TOKEN', '')
        
        if not hf_token:
            print("❌ Please set HF_TOKEN environment variable with your Hugging Face token")
            print("Example: set HF_TOKEN=your_hf_token_here")
            print("Get your token from: https://huggingface.co/settings/tokens")
            return None
        
        # Hugging Face Inference API endpoint for FLUX
        api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 4,
                "guidance_scale": 0.0
            }
        }
        
        print("Sending request to Hugging Face...")
        response = requests.post(api_url, headers=headers, json=data, timeout=120)
        
        if response.status_code == 200:
            # Create output directory
            output_dir = "generated_images"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"flux_hf_{timestamp}.png"
            output_path = os.path.join(output_dir, filename)
            
            # Save image
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Image saved successfully: {output_path}")
            return output_path
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The model might be loading, try again in a moment.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        result = generate_flux_image(prompt)
        if result:
            print(f"Image generated: {result}")
        else:
            print("Image generation failed")
    else:
        print("Usage: python flux_hf_api.py \"your prompt here\"")
        print("Example: python flux_hf_api.py \"a red sports car\"")
        print("Note: Set HF_TOKEN environment variable first")

