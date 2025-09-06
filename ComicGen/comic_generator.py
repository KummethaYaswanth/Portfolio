#!/usr/bin/env python3
"""
Comic Generator for ComfyUI
Generates 6-panel comic workflows from prompt JSON files.
"""

import json
import os
import sys
from pathlib import Path

def load_template_workflow():
    """Load the base 6-panel comic workflow template."""
    template_path = Path("workflows/6panel_comic_example.json")
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template workflow not found: {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_prompts(prompts_file):
    """Load prompts from JSON file."""
    prompts_path = Path("6panel prompt files") / prompts_file
    
    if not prompts_path.exists():
        raise FileNotFoundError(f"Prompts file not found: {prompts_path}")
    
    with open(prompts_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_workflow(prompts_data, input_image_name):
    """
    Generate a ComfyUI workflow from prompts and input image.
    
    Args:
        prompts_data: Dictionary containing the prompts
        input_image_name: Name of the input character image
    
    Returns:
        Generated workflow dictionary
    """
    # Load template workflow
    workflow = load_template_workflow()
    
    # Validate prompts structure
    required_keys = ['tpose_prompt', 'panel_prompts']
    for key in required_keys:
        if key not in prompts_data:
            raise ValueError(f"Missing required key in prompts: {key}")
    
    if len(prompts_data['panel_prompts']) != 6:
        raise ValueError(f"Expected 6 panel prompts, got {len(prompts_data['panel_prompts'])}")
    
    # Update input image (node 43)
    workflow["43"]["inputs"]["image"] = input_image_name
    
    # Update T-pose reference prompt (node 6)
    workflow["6"]["inputs"]["text"] = prompts_data['tpose_prompt']
    
    # Update panel prompts (nodes 89, 112, 114, 137, 142, 151)
    panel_node_ids = [89, 112, 114, 137, 142, 151]
    
    for i, node_id in enumerate(panel_node_ids):
        if str(node_id) in workflow:
            workflow[str(node_id)]["inputs"]["text"] = prompts_data['panel_prompts'][i]
        else:
            raise ValueError(f"Panel node {node_id} not found in template workflow")
    
    # Note: We don't add metadata to the workflow as ComfyUI doesn't expect custom fields
    # The metadata is only used for documentation purposes in the prompts file
    
    return workflow

def save_workflow(workflow, output_name):
    """Save the generated workflow to the generated workflows folder."""
    output_path = Path("generated workflows") / f"{output_name}.json"
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    return output_path

def main():
    """Main function to handle command line arguments and generate workflows."""
    if len(sys.argv) not in [3, 4]:
        print("Usage: python comic_generator.py <prompts_file.json> <input_image_name> [output_name]")
        print("Example: python comic_generator.py hogwarts_sorting.json default_character.png hogwarts_comic")
        sys.exit(1)
    
    prompts_file = sys.argv[1]
    input_image_name = sys.argv[2]
    output_name = sys.argv[3] if len(sys.argv) == 4 else Path(prompts_file).stem
    
    try:
        # Load prompts
        print(f"Loading prompts from: {prompts_file}")
        prompts_data = load_prompts(prompts_file)
        
        # Generate workflow
        print(f"Generating workflow for input image: {input_image_name}")
        workflow = generate_workflow(prompts_data, input_image_name)
        
        # Save workflow
        output_path = save_workflow(workflow, output_name)
        print(f"Generated workflow saved to: {output_path}")
        
        # Print summary
        print("\n=== Workflow Summary ===")
        print(f"Input Image: {input_image_name}")
        print(f"T-pose Prompt: {prompts_data['tpose_prompt'][:100]}...")
        print(f"Panel Prompts:")
        for i, prompt in enumerate(prompts_data['panel_prompts'], 1):
            print(f"  Panel {i}: {prompt[:80]}...")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 