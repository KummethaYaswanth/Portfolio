# 📸 Project Images

This folder contains screenshots and visual assets for portfolio projects.

## 🖼️ Adding Project Images

When adding new projects to your portfolio:

1. **Create project subfolder**: `images/project-name/`
2. **Add screenshots**: 
   - `hero-image.png` - Main project showcase image
   - `demo.gif` - Interactive demo (optional)
   - `architecture.png` - System architecture (optional)
   - `results.png` - Results/outputs (optional)

## 📏 Recommended Image Specifications

- **Hero Images**: 1200x600px (2:1 ratio)
- **Screenshots**: 1920x1080px or similar HD resolution
- **GIFs**: Max 5MB, optimized for web
- **Format**: PNG for screenshots, JPG for photos, GIF for animations

## 🗂️ Folder Structure Example

```
images/
├── all-things-ml/
│   ├── hero-image.png
│   ├── demo.gif
│   ├── classification-demo.png
│   ├── regression-demo.png
│   └── clustering-demo.png
├── future-project-1/
│   └── hero-image.png
└── future-project-2/
    └── hero-image.png
```

## 🎨 Design Guidelines

- **Consistent Style**: Maintain visual consistency across project images
- **High Quality**: Use high-resolution images for crisp display
- **Descriptive Names**: Use clear, descriptive filenames
- **Optimization**: Compress images for faster loading while maintaining quality

## 📝 Usage in Portfolio

Images can be referenced in your `config.json` projects:

```json
{
  "title": "All Things ML",
  "description": "...",
  "image": "images/all-things-ml/hero-image.png",
  "gallery": [
    "images/all-things-ml/demo.gif",
    "images/all-things-ml/classification-demo.png"
  ]
}
```

**Note**: Update your JavaScript and CSS accordingly to display images when implementing this feature. 