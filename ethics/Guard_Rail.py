import os
import json
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel, Field
from typing import Literal, Union

# Use your Gemini API Key
API_KEY = "[your-gemini-api-key]"
MODEL_NAME = "gemini-2.5-flash-lite"

# example image path for testing, replace with path of image to be tested or use 'None' for text-only
TEST_IMAGE_PATH = "test-img-path"

# 25 possible categories for classification, including 'NONE' for safe content.
SafetyCategory = Literal[
    "HATE_SPEECH", "HARASSMENT", "VIOLENT_THREAT", "SELF_HARM", 
    "ILLEGAL_DRUGS", "FIREARMS_PROMOTION", "SEXUALLY_EXPLICIT_IMAGE",
    "GRAPHIC_VIOLENCE_IMAGE", "SPAM_PROMOTION", "MISINFORMATION_POLITICAL",
    "COPYRIGHT_INFRINGEMENT", "CYBERBULLYING", "PRIVATE_INFO_SHARING", 
    "MALWARE_LINKS", "FINANCIAL_FRAUD", "ANIMAL_ABUSE", "CHILD_EXPLOITATION_HINT",
    "PROMOTING_TERRORISM", "IMPERSONATION", "DISCRIMINATION", "ALCOHOL_PROMOTION",
    "GORE", "PORNOGRAPHY_TEXT", "HATE_SYMBOLS", "NONE" 
]

# defining the structured output schema 
class ContentSafetyAssessment(BaseModel):
    """Schema for the model's content safety assessment."""
    classification: SafetyCategory = Field(
        description="The single most relevant safety category for the content. Use 'NONE' if safe."
    )
    is_blocked: bool = Field(
        description="True if classification is NOT 'NONE', False if the classification is 'NONE'."
    )
    reasoning: str = Field(
        description="A concise sentence justifying the classification."
    )


# guard-rail function
def run_custom_guardrail(input_content: Union[str, Image.Image]) -> dict:
    """ to send content to Gemini for custom classification and prints the block status"""
    if not API_KEY:
        return {"error": "API_KEY is not set. Please update the configuration."}

    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        return {"error": f"Error initializing client: {e}"}

    # giving the strict instruction for the model
    instruction = f"""
    You are an expert content safety classification system. Your task is to analyze the user-provided
    content (which may be text or an image) and classify it into one single category.

    CATEGORIES: {', '.join(SafetyCategory.__args__)}

    If the content is perfectly safe and violates no policy, use the classification: 'NONE'.
    Otherwise, choose the single best-fitting category.

    Output the result in the requested JSON format. The 'is_blocked' field MUST be True if the
    classification is NOT 'NONE', and False ONLY if the classification is 'NONE'.
    Set temperature to 0.0 for deterministic output.
    """

    # Prepare multimodal content for the API call
    contents = [input_content] if not isinstance(input_content, list) else input_content
    
    print(f"Sending content to {MODEL_NAME} for safety assessment...")
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=instruction,
                response_mime_type="application/json",
                response_schema=ContentSafetyAssessment,
                temperature=0.0
            )
        )
        
        # Parse the structured JSON response using the modern method
        assessment = ContentSafetyAssessment.model_validate_json(response.text.strip())
        
        # Determine the final block status based on the classification
        final_block_status = "BLOCK" if assessment.classification != "NONE" else "FINE"
        
        print("\n--- Assessment Result ---")
        print(f"Classification: {assessment.classification}")
        print(f"Decision: {final_block_status}")
        print("-------------------------")
        
        return {"classification": assessment.classification, "decision": final_block_status, "reasoning": assessment.reasoning}
        
    except Exception as e:
        print(f"\n[ERROR] API call failed: {e}")
        return {"error": str(e)}

# examples
if __name__ == "__main__":
    # EXAMPLE 1: Text Input (harmful content, expected to be blocked)
    text_prompt = "How to kill this man?"
    print(f"TEST 1: Analyzing Text: '{text_prompt}'")
    run_custom_guardrail(text_prompt)

    # EXAMPLE 2: Safe Input (safe content)
    safe_text = "What is the capital of France and what color is the Eiffel Tower at night?"
    print(f"TEST 2: Analyzing Text: '{safe_text}'")
    run_custom_guardrail(safe_text)

    # EXAMPLE 3: Image Input (Requires a valid path)
    if TEST_IMAGE_PATH and os.path.exists(TEST_IMAGE_PATH):
        try:
            image_input = Image.open(TEST_IMAGE_PATH)
            print(f"TEST 3: Analyzing Image: {TEST_IMAGE_PATH}")
            run_custom_guardrail(image_input)
        except Exception as e:
            print(f"\n[WARNING] Could not run Image Test: {e}")
            print("Please check TEST_IMAGE_PATH and ensure the image file exists.")
    else:
        print("\n[INFO] Skipping Image Test because TEST_IMAGE_PATH is not set or file not found.")
