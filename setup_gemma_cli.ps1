# GEMMA 3 COMMAND LINE INTERFACE SETUP
# Direct PowerShell integration - No web interface bullshit

Write-Host "🚀 Setting up Gemma 3 Command Line Interface..." -ForegroundColor Green

# Navigate to JuggernautAI directory
if (Test-Path "D:\JuggernautAI") {
    Set-Location "D:\JuggernautAI"
    Write-Host "✅ In D:\JuggernautAI directory" -ForegroundColor Green
} else {
    Write-Host "❌ D:\JuggernautAI directory not found" -ForegroundColor Red
    exit 1
}

# Install required Python packages
Write-Host "📦 Installing required packages..." -ForegroundColor Yellow
pip install requests psutil

# Check if Ollama is running
Write-Host "🔍 Checking Ollama status..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get
    Write-Host "✅ Ollama is running" -ForegroundColor Green
    
    # List available models
    Write-Host "📋 Available models:" -ForegroundColor Cyan
    foreach ($model in $response.models) {
        Write-Host "  - $($model.name)" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Ollama not running. Please start Ollama first." -ForegroundColor Red
    Write-Host "💡 Run: ollama serve" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "USAGE EXAMPLES:" -ForegroundColor Cyan
Write-Host "  python gemma_cli.py                    # Interactive mode" -ForegroundColor White
Write-Host "  python gemma_cli.py -m 'Fix my files'  # Single message" -ForegroundColor White
Write-Host "  python gemma_cli.py -c 'dir D:\'       # Execute command" -ForegroundColor White
Write-Host "  python gemma_cli.py --sysinfo          # System info" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Starting Gemma CLI in interactive mode..." -ForegroundColor Green
Write-Host ""

# Start the CLI
python gemma_cli.py

