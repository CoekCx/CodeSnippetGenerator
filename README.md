# Code Snippet Generator

A system for generating syntax-highlighted code snippets as images, using a Python generator service and a Node.js renderer service.

## Setup

1. Create a `.env` file in the `generator-service/src` directory with the following content:
```
# Path configurations
BLOG_POSTS_PATH=/path/to/your/blog/posts
OUTPUT_PATH=/path/to/your/output
LINKEDIN_POSTS_PATH=/path/to/your/linkedin/posts
LINKEDIN_BLOG_POSTS_PATH=/path/to/your/linkedin/blog/posts

# Renderer service configuration
RENDERER_SERVICE_URL=http://localhost:3000

# Output directory for generated images
# This path will be mounted in Docker containers
OUTPUT_DIR=/path/to/output/directory
```

2. Run the services using Docker Compose:
```bash
docker-compose up -d
```

## Architecture

- **Generator Service**: Python service that tokenizes and prepares HTML for code snippets
- **Renderer Service**: Node.js service that uses Puppeteer to render HTML as images

## Using with Python directly

If you're not using Docker, you can still run the generator service directly:

1. Install the Python dependencies:
```bash
cd generator-service
pip install -r requirements.txt
```

2. Make sure the Node.js renderer service is running:
```bash
cd renderer-service
npm install
node server.js
```

3. Use the API in your Python code:
```python
from generators.html_generator import HtmlGenerator

# Your code snippet
code = '''
def hello_world():
    print("Hello, world!")
'''

# Token classifications (from your tokenizer)
tokens = {...}  # your token classifications

# Generate an image
HtmlGenerator.render_code_snippet_image(
    code, 
    tokens,
    dest_path="my_snippets",
    filename="hello_world.png"
)
```
