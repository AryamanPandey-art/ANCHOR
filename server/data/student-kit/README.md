# Samsung PRISM Student Kit Drop-in Directory

Place official Samsung PRISM Student Kit files here.

### Expected Files:
1. `evidence.json` (or `siis_dataset.json`):
```json
[
  {
    "id": "#SIIS-023",
    "source": "Samsung SIIS",
    "section": "Display > Screen rotation",
    "title": "Screen Rotation & Auto-Rotate Settings",
    "content": "... To enable auto rotate, go to Settings > Display > Screen rotation and turn on Auto rotate ...",
    "intent": "SCREEN_ROTATION",
    "entities": ["screen", "rotate", "auto rotate"],
    "supportedActions": [
      {
        "action": "Enable Auto Rotate",
        "direction": "ENABLE",
        "deeplink": "settings://display/screen_rotation",
        "proof": "Turn on Auto rotate in display settings"
      }
    ]
  }
]
```

2. `deeplinks.json` (or `catalog.json`):
```json
[
  {
    "path": "settings://display/screen_rotation",
    "title": "Screen Rotation Settings",
    "allowedDirections": ["ENABLE", "DISABLE", "TOGGLE"],
    "category": "Display",
    "verified": true
  }
]
```

When files are placed here, ANCHOR automatically detects them and switches `isDemoMode: false`.
If absent, ANCHOR isolates the demo dataset in `server/data/demo/` and reports `isDemoMode: true` with full provenance disclosure.
