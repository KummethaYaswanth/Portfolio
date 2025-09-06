# Comic Generation System for ComfyUI

This system allows you to generate 6-panel comics using ComfyUI workflows with character consistency maintained through the Flux-Kontext model.

## System Overview

The comic generation system consists of:
1. **Template Workflow**: `workflows/6panel_comic_example.json` - Base ComfyUI workflow
2. **Prompt Files**: JSON files in `6panel prompt files/` containing comic prompts
3. **Python Generator**: `comic_generator.py` - Script to generate workflows
4. **Output Workflows**: Generated workflows saved to `generated workflows/`

## How It Works

### 1. Template Structure
The base workflow creates a 3x2 grid (6 panels) comic layout:
- **Row 1**: Panels 1-2 (nodes 89, 112)
- **Row 2**: Panels 3-4 (nodes 114, 137) 
- **Row 3**: Panels 5-6 (nodes 142, 151)

### 2. Character Consistency
- **Input Image** (node 43): Your source character image
- **T-pose Generation** (node 6): Creates a reference T-pose of your character
- **Reference System**: All panels use the T-pose as a character reference
- **Style Transfer**: Each panel maintains character appearance while changing scenes

### 3. Prompt Structure
Each prompt JSON file contains:
```json
{
  "metadata": {
    "title": "Comic Title",
    "description": "Comic description",
    "style": "Art style notes"
  },
  "tpose_prompt": "T-pose generation prompt with character appearance",
  "panel_prompts": [
    "Panel 1 scene description",
    "Panel 2 scene description", 
    "Panel 3 scene description",
    "Panel 4 scene description",
    "Panel 5 scene description",
    "Panel 6 scene description"
  ]
}
```

## Usage Instructions

### Step 1: Prepare Your Character Image
1. Place your character image in the ComfyUI input folder
2. Use a clear image showing the character's face and features
3. Name it descriptively (e.g., `my_character.png`)

### Step 2: Create Your Comic Prompts
1. Create a new JSON file in `6panel prompt files/`
2. Follow the prompt structure above
3. Write 6 panel descriptions that tell your story
4. Include a T-pose prompt describing your character's appearance

### Step 3: Generate the Workflow
```bash
python comic_generator.py <prompts_file.json> <input_image_name> [output_name]
```

**Example:**
```bash
python comic_generator.py hogwarts_sorting.json default_character.png hogwarts_comic
```

### Step 4: Run in ComfyUI
1. Load the generated workflow JSON in ComfyUI
2. Ensure all required models are installed:
   - `flux1-kontext-dev.safetensors`
   - `clip_l.safetensors`
   - `t5xxl_fp16.safetensors`
   - `ae.safetensors`
3. Execute the workflow to generate your comic

## Example: Hogwarts Sorting Comic

The included example creates a 6-panel comic story:
1. **Panel 1**: Character standing nervously in the Great Hall
2. **Panel 2**: Walking to the front as name is called
3. **Panel 3**: Sitting on stool with Sorting Hat placed
4. **Panel 4**: Close-up with hat deliberating 
5. **Panel 5**: Hat shouts "GRYFFINDOR!" with crowd cheering
6. **Panel 6**: Walking proudly to Gryffindor table

## Writing Effective Prompts

### T-pose Prompt Tips
- Describe character's basic appearance (clothing, style)
- Specify art style (comic book, realistic, etc.)
- Include "t pose" for proper reference generation
- Keep background simple (grey background recommended)

### Panel Prompt Tips
- Start each with "he/she is..." for consistency
- Include detailed scene descriptions
- Specify lighting and mood
- Mention speech bubbles or text if needed
- Maintain consistent art style across panels
- Consider the story flow between panels

### Style Consistency
- Use consistent art style terms across all prompts
- For serious comics: "serious comic book art style"
- For cartoons: "cartoon style" or "animated style" 
- For realism: "photorealistic" or "realistic style"

## Technical Details

### Required Models
- **Flux-Kontext**: Character-consistent image generation
- **CLIP Models**: Text encoding and understanding
- **VAE**: Image encoding/decoding

### Node Functions
- **Nodes 89, 112, 114, 137, 142, 151**: Panel text prompts
- **Node 6**: T-pose reference prompt
- **Node 43**: Input character image
- **Nodes 153-170**: Reference latent connections
- **Nodes 155-159**: Image stitching for final comic layout

### Output Structure
- Individual panel images are generated
- Images are automatically stitched into 3x2 grid
- Final comic saved as single image
- Optional animated WEBP output available

## Troubleshooting

### Common Issues
1. **Character doesn't look consistent**
   - Ensure T-pose prompt clearly describes character appearance
   - Check that input image is clear and well-lit
   - Verify reference latent connections are working

2. **Poor panel quality**
   - Increase sampling steps (20-30 recommended)
   - Adjust guidance values (2.5 default)
   - Ensure prompts are detailed enough

3. **Style inconsistency**
   - Use identical style descriptions across all prompts
   - Be specific about art style preferences
   - Include style terms in every panel prompt

### File Structure
```
USE THIS separate workflows/
├── workflows/
│   └── 6panel_comic_example.json (template)
├── 6panel prompt files/
│   └── your_prompts.json
├── generated workflows/
│   └── generated_comic.json
├── comic_generator.py
└── Comic_Generation_README.md
```

## Advanced Usage

### Custom Panel Layouts
The current system generates 3x2 grids. To modify:
1. Edit the ImageStitch nodes (155-159) in the template
2. Adjust panel arrangements and spacing
3. Update the Python script for different panel counts

### Batch Generation
Create multiple prompt files and generate several comics:
```bash
python comic_generator.py story1.json character.png comic1
python comic_generator.py story2.json character.png comic2
python comic_generator.py story3.json character.png comic3
```

### Style Variations
Create prompt files with different art styles:
- `superhero_comic.json` - "classic superhero comic book style"
- `manga_style.json` - "black and white manga style"
- `newspaper_comic.json` - "newspaper comic strip style"

## Credits

This system leverages:
- **ComfyUI**: Node-based image generation interface
- **Flux-Kontext**: Character-consistent AI model by Black Forest Labs
- **CLIP**: Text-image understanding by OpenAI
- **Stable Diffusion**: Base diffusion architecture

---

*For questions or issues, refer to the workflow documentation or ComfyUI community resources.* 