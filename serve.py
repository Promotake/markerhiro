"""Minimal dependency-free local web server for testing in a desktop browser.
For a phone, deploy the directory to an HTTPS hosting service (e.g. GitHub Pages).
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from functools import partial

PORT = 8000
ROOT = Path(__file__).resolve().parent

class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        '.glb': 'model/gltf-binary',
        '.gltf': 'model/gltf+json',
        '.bin': 'application/octet-stream',
        '.js': 'text/javascript',
    }

if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', PORT), partial(Handler, directory=str(ROOT)))
    print(f'Serving {ROOT}')
    print(f'Open: http://localhost:{PORT}/')
    print(f'Model preview: http://localhost:{PORT}/preview.html')
    print('Press Ctrl+C to stop. Mobile camera requires HTTPS, not a LAN http:// IP.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopping server...')
    finally:
        server.server_close()
