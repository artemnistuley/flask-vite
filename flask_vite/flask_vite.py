from os import path as _path
from urllib.parse import urljoin
from flask import _app_ctx_stack, Markup
import json

class Vite():
    
    def __init__(self, app = None):
        self.app = app
        self._manifest = None
        if self.app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        app.config.setdefault('VITE_DEV_MODE', False)
        app.config.setdefault('VITE_DEV_SERVER_PROTOCOL', 'http')
        app.config.setdefault('VITE_DEV_SERVER_HOST', 'localhost')
        app.config.setdefault('VITE_DEV_SERVER_PORT', '5173')
        app.config.setdefault('VITE_WS_CLIENT_URL', '@vite/client')
        app.config.setdefault('VITE_STATIC_ROOT', self.static_root)
        app.config.setdefault('VITE_STATIC_URL', self.static_url)

        static_root = app.config.get('VITE_STATIC_ROOT')
        static_url = app.config.get('VITE_STATIC_URL')

        vite_static_dist_url = _path.join(static_url, 'dist/')
        app.config.setdefault('VITE_STATIC_DIST_URL', vite_static_dist_url)

        vite_manifest_path = _path.join(static_root, 'dist', 'manifest.json')
        app.config.setdefault('VITE_MANIFEST_PATH', vite_manifest_path)

        if not app.config['VITE_DEV_MODE']:
            self.parse_manifest()

        @app.context_processor
        def context_processor():
            return dict(
                vite_asset = self.vite_asset,
                vite_hmr_client = self.vite_hmr_client,
            )

        app.teardown_appcontext(self.teardown)

    @property
    def static_root(self):
        return _path.join(self.app.root_path, self.app.static_folder)
    
    @property
    def static_url(self):
        return self.app.static_url_path

    def teardown(self, exception):
        # using for clear
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'xxx'):
            pass

    def parse_manifest(self):
        vite_manifest_path = self.app.config.get('VITE_MANIFEST_PATH')
        try:
            with open(vite_manifest_path, "r") as manifest_file:
                manifest_content = manifest_file.read()
            self._manifest = json.loads(manifest_content)
        except Exception:
            raise RuntimeError(
                f"Cannot read Vite manifest file at {vite_manifest_path}"
            )
        
    def generate_vite_server_url(self, path):
        protocol = self.app.config.get('VITE_DEV_SERVER_PROTOCOL')
        host = self.app.config.get('VITE_DEV_SERVER_HOST')
        port = self.app.config.get('VITE_DEV_SERVER_PORT')

        base_path = "{protocol}://{host}:{port}".format(
            protocol=protocol,
            host=host,
            port=port
        )
        return urljoin(base_path, path if path is not None else "")

    def generate_vite_asset(self, path, script_attrs, with_imports):
        if self.app.config['VITE_DEV_MODE']:
            return self.generate_script_tag(self.generate_vite_server_url(path), {"type": "module"})
        
        if path not in self._manifest:
            vite_manifest_path = self.app.config['VITE_MANIFEST_PATH']
            raise RuntimeError(
                f"Cannot find {path} in Vite manifest at {vite_manifest_path}"
            )
        
        tags = []
        manifest_entry = self._manifest.get(path)
        if not script_attrs:
            script_attrs = {"type": "module"}

        static_dist_url = self.app.config['VITE_STATIC_DIST_URL']
        
        if "css" in manifest_entry:
            for css_path in manifest_entry.get("css"):
                tags.append(
                    self.generate_stylesheet_tag(
                        urljoin(static_dist_url, css_path)
                    )
                )

        if with_imports and "imports" in manifest_entry:
            for vendor_path in manifest_entry.get("imports"):
                tags.append(
                    self.generate_vite_asset(
                        vendor_path, 
                        script_attrs = script_attrs, 
                        with_imports = with_imports
                    )
                )

        tags.append(
            self.generate_script_tag(
                urljoin(static_dist_url, manifest_entry.get("file")),
                attrs = script_attrs,
            )
        )

        return "\n".join(tags)

    def generate_vite_ws_client(self):
        if not self.app.config['VITE_DEV_MODE']:
            return ""
        
        ws_client_url = self.generate_vite_server_url(self.app.config['VITE_WS_CLIENT_URL'])
        return self.generate_script_tag(ws_client_url, {"type": "module"})
    
    def generate_stylesheet_tag(self, href):
        return f'<link href="{href}" rel="stylesheet" />'

    def generate_script_tag(self, src, attrs):
        attrs_str = ""
        if attrs is not None:
            attrs_str = " ".join([f'{key}="{value}"' for key, value in attrs.items() ])

        return f'<script src="{src}" {attrs_str}></script>'

    def vite_asset(self, path, script_attrs = None, with_imports = True):
        return Markup(self.generate_vite_asset(path, script_attrs = script_attrs, with_imports = with_imports))

    def vite_hmr_client(self):
        return Markup(self.generate_vite_ws_client())
