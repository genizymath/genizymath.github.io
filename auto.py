import os
import json
import requests

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{GAME_NAME} | Play Now on Gn-Math</title>
    <meta name="title" content="{GAME_NAME} | Play Now on Gn-Math">
    <meta name="description" content="Play {GAME_NAME} online unblocked on Gn-Math! Enjoy unique and exclusive games at school, work, or anywhere. No downloads needed!">
    <link rel="canonical" href="https://genizymath.github.io/games/{GAME_NAME_URL}/">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://genizymath.github.io/games/{GAME_NAME_URL}/">
    <meta property="og:title" content="{GAME_NAME} | Play Now on Gn-Math">
    <meta property="og:description" content="Play {GAME_NAME} online unblocked on Gn-Math! Free, easy, and fast to play.">
    <meta property="og:image" content="https://cdn.jsdelivr.net/gh/gn-math/covers@main/{GAME_ID}.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://genizymath.github.io/games/{GAME_NAME_URL}/">
    <meta name="twitter:title" content="{GAME_NAME} | Play Now on Gn-Math">
    <meta name="twitter:description" content="Play {GAME_NAME} online unblocked on Gn-Math! Free, easy, and fast to play.">
    <meta name="twitter:image" content="https://cdn.jsdelivr.net/gh/gn-math/covers@main/{GAME_ID}.png">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow">
    <meta name="author" content="Gn-Math">
    <link rel="icon" href="/images/favicon.png" type="image/x-icon">
    <meta name="Keywords" content="Unblocked, Games, Unblocked Games, Online Games, Unblocked Games Online, {GAME_NAME} Unblocked, {GAME_NAME} Online, {GAME_NAME} Free, {GAME_NAME} Unblocked Online, {GAME_NAME}, {GAME_NAME} Game">
    <style>
        body {
            font-family: sans-serif;
            text-align: center;
            padding: 50px;
            background-color: #333;
            color: #fff;
        }

        img {
            max-width: 100%;
            height: auto;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }

        a.play-button {
            display: inline-block;
            padding: 14px 24px;
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }

        a.play-button:hover {
            background-color: #45a049;
        }

        .official-link {
            display: block;
            margin-top: 30px;
            color: #fff;
            font-size: 14px;
        }

        .official-link:hover {
            text-decoration: underline;
        }
        
    </style>
</head>

<body>
    <h1>{GAME_NAME}</h1>
    <img src="https://cdn.jsdelivr.net/gh/gn-math/covers@main/{GAME_ID}.png" style="max-width: 100%; height: auto; width: 200px;" alt="{GAME_NAME} Cover">
    <br>
    <a class="play-button" href="https://gn-math.github.io/?id={GAME_ID}">▶ Play Now</a>
    <a class="official-link" href="https://gn-math.github.io/" target="_blank">Official Gn-Math Site</a>
</body>

</html>
"""

hashresponse = requests.get("https://api.github.com/repos/gn-math/assets/commits")
hash = json.loads(hashresponse.text)[0]['sha']
print(f"latest hash: {hash}")

OUTPUT_DIR = 'games'
response = requests.get(f'https://cdn.jsdelivr.net/gh/gn-math/assets@{hash}/zones.json')
os.makedirs(OUTPUT_DIR, exist_ok=True)
games = json.loads(response.text)
print("loaded zones")

game_paths = []

for game in games:
    game_id = str(game['id'])
    if game_id == '-1':
        continue
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
    game_paths.append(game_folder)
    print(f"Made {index_path}")

json_string = json.dumps(game_paths, indent=4)
try:
    with open('games.json', 'w', encoding='utf-8') as f:
        f.write(json_string)
    print("games.json done")
except Exception as e:
    print("Error games.json:", e)

print("done")
