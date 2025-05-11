@echo off
echo Setting up Code Snippet Generator in hybrid mode...

REM Create .env file
echo Creating .env file...
echo # Path configurations for content > generator-service\src\.env
echo BLOG_POSTS_PATH=D:/Coek/Work/Social Media Nikola/Content/Blog/Blog Posts >> generator-service\src\.env
echo OUTPUT_PATH=D:/Coek/Apps/CodeSnippetGenerator/output >> generator-service\src\.env
echo LINKEDIN_POSTS_PATH=D:/Coek/Work/Social Media Nikola/Content/LinkedIn/Posts >> generator-service\src\.env
echo LINKEDIN_BLOG_POSTS_PATH=D:/Coek/Work/Social Media Nikola/Content/Blog/Blog Posts >> generator-service\src\.env
echo. >> generator-service\src\.env
echo # Renderer service configuration >> generator-service\src\.env
echo RENDERER_SERVICE_URL=http://localhost:3000 >> generator-service\src\.env

REM Start Docker renderer service
echo Starting renderer service in Docker...
docker-compose -f docker-compose.renderer.yml up -d

echo.
echo Setup complete! 
echo.
echo To run the generator service:
echo cd generator-service
echo python -m src.main
echo.
echo The renderer service is running in Docker and is accessible at http://localhost:3000
echo Images and HTML files will be saved to D:\Coek\Work\Social Media Nikola 