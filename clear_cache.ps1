# Clear Python Cache Script for Windows PowerShell
# Run this if you're seeing errors from cached bytecode

Write-Host "Clearing Python cache files..." -ForegroundColor Yellow

# Remove __pycache__ directories
Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force

# Remove .pyc files
Get-ChildItem -Path . -Include *.pyc -Recurse -File | Remove-Item -Force

# Remove .pyo files (optimized bytecode)
Get-ChildItem -Path . -Include *.pyo -Recurse -File | Remove-Item -Force

Write-Host "Cache cleared successfully!" -ForegroundColor Green
Write-Host "You can now run: python main.py" -ForegroundColor Cyan

