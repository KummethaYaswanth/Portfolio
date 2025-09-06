@echo off
REM Comic Generator Batch Script
REM Usage: generate_comic.bat <prompts_file.json> <input_image_name> [output_name]

if "%~1"=="" goto usage
if "%~2"=="" goto usage

echo Generating comic workflow...
echo Prompts: %1
echo Image: %2
echo.

if "%~3"=="" (
    python comic_generator.py "%~1" "%~2"
) else (
    python comic_generator.py "%~1" "%~2" "%~3"
)

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Comic workflow generated!
    echo Check the 'generated workflows' folder for your new workflow.
    echo.
    echo Next steps:
    echo 1. Open ComfyUI
    echo 2. Load the generated workflow JSON file
    echo 3. Execute the workflow to create your comic
) else (
    echo.
    echo ERROR: Failed to generate comic workflow
    echo Check the error message above for details
)

goto end

:usage
echo.
echo Comic Generator for ComfyUI
echo.
echo Usage: generate_comic.bat ^<prompts_file.json^> ^<input_image_name^> [output_name]
echo.
echo Examples:
echo   generate_comic.bat hogwarts_sorting.json default_character.png
echo   generate_comic.bat my_story.json my_character.png my_comic
echo.
echo The prompts file should be in the '6panel prompt files' folder
echo The input image should be in your ComfyUI input folder
echo.

:end
pause 