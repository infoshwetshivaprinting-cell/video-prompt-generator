from importlib import import_module

MODULES = [
    'config',
    'voiceover_generator',
    'image_generator',
    'video_editor',
    'seo_helper',
    'logger'
]

if __name__ == '__main__':
    ok = True
    for m in MODULES:
        try:
            import_module(m)
            print(f"Imported {m}")
        except Exception as e:
            print(f"Failed to import {m}: {e}")
            ok = False
    if ok:
        print("All basic modules import successfully.")
    else:
        raise SystemExit(1)
