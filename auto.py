import os
import json
import re
import aiohttp
import asyncio
from aiohttp import ClientSession

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/png" href="/images/favicon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon.png">
    <link rel="apple-touch-icon" href="/images/favicon.png">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Play {GAME_NAME} | GN-Math Unblocked Games</title>
    <meta name="description" content="Play {GAME_NAME} unblocked on GN-Math - No downloads required! Enjoy this fun HTML5 game at school or work with our fast, secure gaming platform.">
    <meta name="keywords" content="{GAME_NAME}, {GAME_NAME} unblocked, play {GAME_NAME}, free {GAME_NAME}, html5 games, unblocked games, school games, no flash games">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://genizymath.github.io/">
    <meta property="og:title" content="Play {GAME_NAME} | GN-Math Unblocked Games">
    <meta property="og:description" content="Play {GAME_NAME} unblocked on GN-Math - No downloads required! Enjoy this fun HTML5 game at school or work.">
    <meta property="og:image" content="{GAME_COVER}">
	<meta name="google-adsense-account" content="ca-pub-5521219086088837">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://genizymath.github.io/">
    <meta property="twitter:title" content="Play {GAME_NAME} | GN-Math Unblocked Games">
    <meta property="twitter:description" content="Play {GAME_NAME} unblocked on GN-Math - No downloads required! Enjoy this fun HTML5 game at school or work.">
    <meta property="twitter:image" content="{GAME_COVER}">
    
    <link rel="stylesheet" href="/styles/style.css">
    <style>
        .game-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        
        .game-header {
            margin-bottom: 20px;
        }
        
        .game-title {
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: var(--primary-color);
        }
        
        .game-frame-container {
            position: relative;
            margin: 0 auto;
            max-width: 900px;
            border: 2px solid var(--card-border);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px var(--shadow);
            margin-bottom: 30px;
        }
        
        .game-frame {
            width: 100%;
            height: 600px;
            border: none;
            background: var(--card-bg);
        }
        
        .fullscreen-btn {
            position: absolute;
            bottom: 10px;
            right: 10px;
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            z-index: 10;
        }

        .newtab-btn {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            z-index: 10;
        }
        
        .game-info {
            margin-top: 20px;
            text-align: left;
            padding: 20px;
            background: var(--card-bg);
            border-radius: 8px;
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
        }
        
        .game-cover {
            flex: 1;
            min-width: 300px;
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px var(--shadow);
            object-fit: contain;
            align-self: flex-start;
        }
        
        .game-details {
            flex: 2;
            min-width: 300px;
        }
        
        .game-description {
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .features-list {
            columns: 2;
            column-gap: 20px;
        }
        
        @media (max-width: 768px) {
            .game-title {
                font-size: 1.8rem;
            }
            
            .game-frame {
                height: 400px;
            }
            
            .features-list {
                columns: 1;
            }
            
            .game-cover {
                min-width: 100%;
            }
        }
    </style>
</head>
<body class="dark-mode">
    <div id="ad-top" style="text-align: center; margin: 1rem 0;">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5521219086088837"
     crossorigin="anonymous"></script>
    </div>
    <header>
        <div class="header-content">
            <a class="logo" href="/index.html" style="text-decoration: none; color: inherit;">genizymath</a>
            <div class="control-buttons">
                <button id="settings" style="background-color: var(--primary-color); color: white; border: none; border-radius: 4px; padding: 0.5rem 1rem; font-size: 16px; cursor: pointer;">Settings</button>
            </div>
        </div>
    </header>

    <main class="game-container">
        <div class="game-header">
            <h1 class="game-title">{GAME_NAME}</h1>
        </div>
        
        <div class="game-frame-container">
            <iframe class="game-frame" id="gameFrame" allowfullscreen></iframe>
            <button class="fullscreen-btn" onclick="document.getElementById('gameFrame').requestFullscreen()">Fullscreen</button>
            <button class="newtab-btn" onclick="window.open('https://genizymath.github.io/iframe/{PATHNAME}', '_blank')">Open in New Tab</button>
        </div>

        <div id="ad-middle" style="text-align: center; margin: 2rem 0;">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5521219086088837"
     crossorigin="anonymous"></script>
        
        <div class="game-info">
            <img class="game-cover" id="coverImage" alt="{GAME_NAME} Game Cover">
            
            <div class="game-details">
                <h2>About {GAME_NAME}</h2>
                <p class="game-description">
                    Play {GAME_NAME} unblocked on GN-Math! Our platform provides fast, secure access to this popular HTML5 game without any downloads. 
                    Perfect for school, work, or home, {GAME_NAME} runs directly in your browser with no installation required.
                </p>
                
                <h3>How to Play</h3>
                <ul>
                    <li>Use the fullscreen button for the best gaming experience</li>
                    <li>Game controls are typically keyboard (WASD or arrow keys) and mouse</li>
                    <li>Save your progress - high scores may be saved between sessions</li>
                </ul>
                
                <h3>Features</h3>
                <ul class="features-list">
                    <li>No downloads or installations required</li>
                    <li>Works on Chromebooks and school computers</li>
                    <li>Fast loading times with our optimized servers</li>
                    <li>Regularly updated game library</li>
                    <li>Mobile-friendly gameplay</li>
                    <li>Dark mode support</li>
                    <li>Privacy-focused platform</li>
                    <li>Works behind school filters</li>
                </ul>
            </div>
        </div>
    </main>

    <script>
        const params = new URLSearchParams(window.location.search);
        const title = "{GAME_NAME}";
        const cover = "{GAME_COVER}";
        const url = "{GAME_URL}";

        document.getElementById("coverImage").src = cover;
        document.getElementById("coverImage").alt = `${title} Game Cover`;
        document.getElementById("gameFrame").src = url;
    </script>

    <div id="popupOverlay">
      <div class="popup">
          <div class="popup-header">
              <h3 id="popupTitle">Title</h3>
              <button id="popupClose" onclick="closePopup()">×</button>
          </div>
          <div id="popupBody">
              Content will be here
          </div>
      </div>
    </div>
    
    <footer>
        <div class="footer-links">
            <a href="#" onclick="showContact(); return false;">Contact</a>
            <a href="#" onclick="loadPrivacy(); return false;">Privacy Policy</a>
            <a href="javascript:saveData()">Export Data</a>
            <label for="importData" style="color: var(--primary-color); cursor: pointer;">Import Data</label>
            <input type="file" id="importData" style="display: none;" onchange="loadData(event)">
        </div>
    </footer>

        <div id="ad-bottom" style="text-align: center; margin: 2rem 0;">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5521219086088837"
     crossorigin="anonymous"></script>
        </div>

    <script src="/javascript/script.js"></script>
</body>
</html>
"""

sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset 
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

  <url>
    <loc>https://genizymath.github.io/</loc>
  </url>
""";

async def fetch_json(session: ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()

async def fetch_text(session: ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()

async def process_game(session: ClientSession, game: dict, OUTPUT_DIR: str, GAME_DIR: str) -> str:
    game_id = str(game['id'])
    if game_id == '-1':
        return None
    
    game_name = game['name']
    game_cover = game['cover']
	pathname = f"{game['url'].split("/")[1]}"
    game_name_url = re.sub(r'[^a-zA-Z0-9-]', '', game_name.replace(' ', '-').lower()).replace('--', '-')
    
    game_folder = os.path.join(OUTPUT_DIR, game_name_url)
    os.makedirs(game_folder, exist_ok=True)
    os.makedirs(GAME_DIR, exist_ok=True)
    
    html_content = TEMPLATE_HTML.replace('{GAME_NAME}', game_name)\
                               .replace('{GAME_ID}', game_id)\
                               .replace('{GAME_COVER}', game_cover.replace(
                                   "{COVER_URL}", 
                                   "https://cdn.jsdelivr.net/gh/gn-math/covers@main"))\
                               .replace('{GAME_URL}', "/iframe/"+pathname)\
                               .replace('{PATHNAME}', pathname)
    game_url = f'https://cdn.jsdelivr.net/gh/gn-math/html@main/{pathname}'
    game_html = await fetch_text(session, game_url)
    
    game_file_path = os.path.join(GAME_DIR, f"{pathname}")
    with open(game_file_path, 'w', encoding='utf-8') as f:
        f.write(game_html)
    
    index_path = os.path.join(OUTPUT_DIR, game_name_url, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    global sitemap
    sitemap += f"""
    <url>
        <loc>https://genizymath.github.io/games/{game_name_url}/</loc>
    </url>
    """
    print(f"Made {index_path}")
    return game_file_path

async def main():
    OUTPUT_DIR = 'games'
    GAME_DIR = 'iframe'
    
    async with ClientSession() as session:
        hash_response = await fetch_json(session, "https://api.github.com/repos/gn-math/assets/commits")
        hash = hash_response[0]['sha']
        print(f"latest hash: {hash}")
        
        zones_url = f'https://cdn.jsdelivr.net/gh/gn-math/assets@{hash}/zones.json'
        games = await fetch_json(session, zones_url)
        print("loaded zones")
        
        tasks = [process_game(session, game, OUTPUT_DIR, GAME_DIR) for game in games]
        game_paths = await asyncio.gather(*tasks)
        
        game_paths = [path for path in game_paths if path is not None]
        
        json_string = json.dumps(game_paths, indent=4)
        try:
            with open('games.json', 'w', encoding='utf-8') as f:
                f.write(json_string)
            print("games.json done")
        except Exception as e:
            print("Error games.json:", e)
        try:
            global sitemap
            sitemap += "</urlset>"
            with open('sitemap.xml', 'w', encoding='utf-8') as f:
                f.write(sitemap)
            with open('newsitemap.xml', 'w', encoding='utf-8') as f:
                f.write(sitemap)
            print("sitemap done")
        except Exception as e:
            print("Error sitemap.xml:", e)
    print("done")

if __name__ == '__main__':
    asyncio.run(main())
