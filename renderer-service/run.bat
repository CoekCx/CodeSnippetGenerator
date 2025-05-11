@echo off
echo Building Docker image...
docker build -t renderer-service .

echo Starting container...
docker run -d ^
    --name renderer-service ^
    -p 3000:3000 ^
    -v "D:/Coek/Work/Social Media Nikola:/output" ^
    --restart unless-stopped ^
    renderer-service

echo Renderer service is now running on port 3000 