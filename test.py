from rich.console import Console
from rich.markdown import Markdown
import time

console = Console()

def typewriter_effect(text, delay=0.05):
    """Prints text with a typewriter effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # Move to a new line

markdown_text = """
# Title
**Bold text** and _italic text_
- Item 1
- Item 2
"""

# Render markdown
console.clear()
md = Markdown(markdown_text)

# Simulate typewriter effect
for line in markdown_text.split("\n"):
    typewriter_effect(line)
    time.sleep(0.1)  # Extra delay between lines

console.print(md)
