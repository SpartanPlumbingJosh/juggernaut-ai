# GPU Setup for Juggernaut AI
Write-Host " Installing CUDA-enabled dependencies for RTX GPU..." -ForegroundColor Green
pip uninstall llama-cpp-python -y
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
pip install -r requirements.txt
Write-Host " GPU setup complete!" -ForegroundColor Green
