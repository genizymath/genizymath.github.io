import os
import json

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{GAME_NAME} | Play Now on Gn-Math</title>
    <meta name="title" content="{GAME_NAME} | Play Now on Gn-Math">
    <meta name="description" content="Play {GAME_NAME} online unblocked on Gn-Math! Enjoy unique and exclusive games at school, work, or anywhere. No downloads needed!">
    <link rel="canonical" href="https://gnmaths.github.io/games/{GAME_NAME_URL}/">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://gnmaths.github.io/games/{GAME_NAME_URL}/">
    <meta property="og:title" content="{GAME_NAME} | Play Now on Gn-Math">
    <meta property="og:description" content="Play {GAME_NAME} online unblocked on Gn-Math! Free, easy, and fast to play.">
    <meta property="og:image" content="https://cdn.jsdelivr.net/gh/gn-math/covers@main/{GAME_ID}.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://gnmaths.github.io/games/{GAME_NAME_URL}/">
    <meta name="twitter:title" content="{GAME_NAME} | Play Now on Gn-Math">
    <meta name="twitter:description" content="Play {GAME_NAME} online unblocked on Gn-Math! Free, easy, and fast to play.">
    <meta name="twitter:image" content="https://cdn.jsdelivr.net/gh/gn-math/covers@main/{GAME_ID}.png">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow">
    <meta name="author" content="Gn-Math">
    <link rel="icon" href="/images/favicon.png" type="image/x-icon">
    <meta name="Keywords" content="Unblocked, Games, Unblocked Games, Online Games, Unblocked Games Online, {GAME_NAME} Unblocked, {GAME_NAME} Online, {GAME_NAME} Free, {GAME_NAME} Unblocked Online, {GAME_NAME}, {GAME_NAME} Game">
    <script>
        window.location.href = "https://gn-math.github.io/?id={GAME_ID}";
    </script>
</head>

<body></body>

</html>"""

ZONES_JSON_PATH = 'zones.json'
OUTPUT_DIR = 'games' 
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(ZONES_JSON_PATH, 'r', encoding='utf-8') as f:
    games = json.load(f)

for game in games:
    game_id = str(game['id'])
    game_name = game['name']
    game_name_url = game_name.lower().replace("-", "").replace("  ", "-").replace(' ', '-').replace('_', '-').replace(":", "").replace(".", "")
    
    game_folder = os.path.join(OUTPUT_DIR, game_name_url)
    os.makedirs(game_folder, exist_ok=True)
    html_content = TEMPLATE_HTML.replace('{GAME_NAME}', game_name)\
                                 .replace('{GAME_ID}', game_id)\
                                 .replace('{GAME_NAME_URL}', game_name_url)
    index_path = os.path.join(game_folder, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Made {index_path}")

print("done")
