"""AI-powered image generation for presentation slides."""

import base64
import json
import logging
import os
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Slide types that should receive generated images
IMAGE_SLIDE_TYPES = {"title", "section", "hero"}

# Style modifiers based on theme
THEME_STYLES = {
    "keynote_minimalist": {
        "style": "minimalist, clean, professional, subtle gradients",
        "mood": "elegant, sophisticated, modern",
        "colors": "dark background with subtle blue accents",
    },
    "technical_blueprint": {
        "style": "technical, blueprint aesthetic, geometric patterns",
        "mood": "innovative, precise, cutting-edge",
        "colors": "dark blue background with cyan accents",
    },
}

DEFAULT_STYLE = {
    "style": "professional, modern, clean",
    "mood": "polished, business-appropriate",
    "colors": "complementary color palette",
}


class ImageGenerator:
    """Generates images for presentation slides using Gemini's native image generation."""

    def __init__(self, api_key: Optional[str] = None, model: str = "nano-banana-pro-preview"):
        """Initialize the image generator.
        
        Args:
            api_key: Gemini API key. If not provided, reads from GEMINI_API_KEY env var.
            model: Model to use for image generation. Options:
                   - "nano-banana-pro-preview" (Gemini 3 Pro, default)
                   - "gemini-2.0-flash-exp-image-generation"
                   - "imagen-4.0-generate-001" (uses different API)
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("No GEMINI_API_KEY found - image generation disabled")
        
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self._use_imagen_api = model.startswith("imagen-")
        
    @property
    def enabled(self) -> bool:
        """Check if image generation is available."""
        return bool(self.api_key)

    def generate_images_for_slides(
        self,
        slides: List[Dict[str, Any]],
        theme_name: str,
        deck_context: str = "",
    ) -> List[Dict[str, Any]]:
        """Generate images for slides that need them.
        
        Args:
            slides: List of slide specifications
            theme_name: Name of the theme being used
            deck_context: Overall context/topic of the presentation
            
        Returns:
            Updated slides with image data added
        """
        if not self.enabled:
            logger.info("Image generation disabled - no API key")
            return slides
        
        theme_style = THEME_STYLES.get(theme_name, DEFAULT_STYLE)
        
        updated_slides = []
        for i, slide in enumerate(slides):
            slide_type = slide.get("layout", "")
            
            # Determine if this slide should have an image
            should_generate = (
                slide_type in IMAGE_SLIDE_TYPES or
                slide.get("generate_image", False) or
                i == 0  # Always generate for first slide (title)
            )
            
            if should_generate:
                logger.info("Generating image for slide %d (%s)", i + 1, slide_type)
                
                prompt = self._build_prompt(slide, theme_style, deck_context)
                image_data = self._generate_image(prompt)
                
                if image_data:
                    slide = {**slide, "background_image": image_data}
                    logger.debug("Image generated successfully for slide %d", i + 1)
                else:
                    logger.warning("Failed to generate image for slide %d", i + 1)
            
            updated_slides.append(slide)
        
        generated_count = sum(1 for s in updated_slides if "background_image" in s)
        logger.info("Generated %d images for %d slides", generated_count, len(slides))
        
        return updated_slides

    def _build_prompt(
        self,
        slide: Dict[str, Any],
        theme_style: Dict[str, str],
        deck_context: str,
    ) -> str:
        """Build an image generation prompt from slide content.
        
        Args:
            slide: Slide specification
            theme_style: Style modifiers from theme
            deck_context: Overall presentation context
            
        Returns:
            Image generation prompt
        """
        content = slide.get("content", {})
        title = content.get("title", "")
        subtitle = content.get("subtitle", "")
        slide_type = slide.get("layout", "title")
        
        # Base description from slide content
        subject = title or subtitle or deck_context or "abstract presentation"
        
        # Build the prompt
        prompt_parts = [
            f"Create a {theme_style['style']} background image for a presentation slide.",
            f"Theme: {theme_style['mood']}.",
            f"Topic: {subject}.",
            f"Color palette: {theme_style['colors']}.",
            "The image should be subtle enough to allow white text overlay.",
            "No text or words in the image.",
            "Aspect ratio: 16:9, landscape orientation.",
        ]
        
        # Add slide-type specific guidance
        if slide_type == "title":
            prompt_parts.append("This is a title slide - make it visually striking but not overwhelming.")
        elif slide_type == "section":
            prompt_parts.append("This is a section divider - use abstract shapes or subtle patterns.")
        
        prompt = " ".join(prompt_parts)
        logger.debug("Generated prompt: %s", prompt[:100] + "...")
        
        return prompt

    def _generate_image(self, prompt: str) -> Optional[str]:
        """Generate an image using Gemini or Imagen API.
        
        Args:
            prompt: Text prompt for image generation
            
        Returns:
            Base64-encoded image data, or None if generation failed
        """
        if self._use_imagen_api:
            return self._generate_image_imagen(prompt)
        else:
            return self._generate_image_gemini(prompt)
    
    def _generate_image_gemini(self, prompt: str) -> Optional[str]:
        """Generate image using Gemini's native image generation (nano-banana, etc.)."""
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        # Prepend "Generate an image:" to make intent clear
        full_prompt = f"Generate an image: {prompt}"
        
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }],
            "generationConfig": {
                "responseModalities": ["image"]
            }
        }
        
        try:
            request = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            
            with urllib.request.urlopen(request, timeout=90) as response:
                result = json.loads(response.read().decode())
            
            # Extract base64 image from Gemini response
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    if "inlineData" in part:
                        return part["inlineData"].get("data")
            
            logger.warning("No image data in Gemini response: %s", result.keys())
            return None
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if hasattr(e, 'read') else ""
            logger.error("Gemini API error %d: %s", e.code, error_body[:300])
            return None
        except urllib.error.URLError as e:
            logger.error("Network error: %s", e.reason)
            return None
        except Exception as e:
            logger.error("Image generation failed: %s", e)
            return None
    
    def _generate_image_imagen(self, prompt: str) -> Optional[str]:
        """Generate image using Imagen API (predict endpoint)."""
        url = f"{self.base_url}/models/{self.model}:predict?key={self.api_key}"
        
        payload = {
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9",
                "personGeneration": "dont_allow",
                "safetySetting": "block_low_and_above",
            }
        }
        
        try:
            request = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode())
            
            # Extract base64 image from response
            predictions = result.get("predictions", [])
            if predictions and "bytesBase64Encoded" in predictions[0]:
                return predictions[0]["bytesBase64Encoded"]
            
            logger.warning("No image data in Imagen response")
            return None
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if hasattr(e, 'read') else ""
            logger.error("Imagen API error %d: %s", e.code, error_body[:200])
            return None
        except urllib.error.URLError as e:
            logger.error("Network error: %s", e.reason)
            return None
        except Exception as e:
            logger.error("Image generation failed: %s", e)
            return None

    def generate_single_image(self, prompt: str) -> Optional[str]:
        """Generate a single image from a custom prompt.
        
        Args:
            prompt: Custom prompt for image generation
            
        Returns:
            Base64-encoded image data, or None if generation failed
        """
        if not self.enabled:
            logger.warning("Image generation disabled - no API key")
            return None
        
        return self._generate_image(prompt)
