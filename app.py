import re
from bs4 import BeautifulSoup

# Dictionary mapping character names to CSS class names
character_classes = {
    "Disney": "disney",
    "Hello Kitty": "hello-kitty",
    "Mickey Mouse & Friends": "mickey-mouse-and-friends",
    "Disney Princess": "disney-princess",
    "Justice League": "justice-league",
    "Frozen": "frozen",
    "Disney Baby": "disney-baby",
    "Marvel": "marvel",
    "DC Comics": "dc-comics",
    "Fisher Price": "fisher-price",
    "Hot Wheels": "hot-wheels",
    "Spider-Man": "spider-man",
    "Disney Junior": "disney-junior",
    "Star Wars": "star-wars",
    "Disney Ariel": "disney-ariel",
    "Beauty": "beauty",
    "Belle": "belle",
    "Toy Story": "toy-story",
    "Frozen 2": "frozen-2",
    "LOL Surprise": "lol-surprise",
    "Grogu": "grogu",
    "Minnie Mouse": "minnie-mouse",
    "Jasmine": "jasmine",
    "Coca-Cola": "coca-cola",
    "Blue's Clues": "blues-clues",
    "Crayola": "crayola",
    "Tiana": "tiana",
    "Moana": "moana",
    "Iron Man": "iron-man",
    "Superman": "superman",
    "Batman": "batman",
    "Rapunzel": "rapunzel",
    "Black Panther": "black-panther",
    "Hulk": "hulk",
    "Encanto": "encanto"
}

# Read and parse the input HTML file
with open("input.html", "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

# Step 1: Remove the extra .alphabet CSS definition
style_tag = soup.find("style")
if style_tag:
    style_lines = style_tag.string.splitlines()
    style_lines = [line for line in style_lines if not line.startswith(".alphabet")]
    style_tag.string = "\n".join(style_lines)

# Step 2: Ensure "All Licensed Characters" section has correct highlighting
for link in soup.select(".character-list a"):
    character_name = link.get_text(strip=True)
    if character_name in character_classes:
        # Add the CSS class to the link if it matches a popular licensed character
        css_class = character_classes[character_name]
        link['class'] = link.get('class', []) + [css_class]  # Append the class if not present

# Step 3: Populate links for "Popular Licensed Characters" based on matches in "All Licensed Characters"
character_links = {}  # Store links for popular characters based on "All Licensed Characters" section
for link in soup.select(".character-list a"):
    character_name = link.get_text(strip=True)
    if character_name in character_classes:
        character_links[character_name] = link["href"]

# Step 4: Generate the "Popular Licensed Characters" section with updated links
popular_section = soup.find("div", class_="popular-characters")
popular_section.clear()  # Clear existing content

for character, css_class in character_classes.items():
    # Retrieve the correct link from character_links; default to "#" if not found
    character_link = character_links.get(character, "#")
    # Create a new `a` tag with the required classes and styles
    popular_link_tag = soup.new_tag("a", href=character_link)
    popular_link_tag['class'] = css_class  # Ensure class is correctly added
    popular_link_tag.string = character
    popular_link_tag['style'] = "padding: 5px; border-radius: 5px;"  # Add inline styles if necessary
    popular_section.append(popular_link_tag)
    popular_section.append(" ")  # Add a space between items

# Write the modified HTML back to output.html
with open("output.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

print("HTML generation complete. Output saved to output.html")
