# Kodi 14 IPTV Repo

Repositorio compatible con **Kodi 14.2 Helix** (Python 2) — Apple TV 3 (A1469).

## Instalación en Kodi

1. **Ajustes → Administrador de archivos → Añadir fuente**
2. URL: `https://TU-USUARIO.github.io/kodi-repo/`
3. Nombre: `Mi IPTV Repo`
4. **Ajustes → Add-ons → Instalar desde zip**
5. Selecciona la fuente → `repository.mi-iptv` → instala el `.zip`
6. **Instalar desde repositorio → Mi IPTV Repo → Video → Mi IPTV**
7. En los ajustes del add-on, coloca la URL de tu archivo `.m3u`

## Estructura
```
kodi-repo/
├── addons.xml
├── addons.xml.md5
├── repository.mi-iptv/
│   ├── addon.xml
│   └── repository.mi-iptv-1.0.0.zip
└── plugin.video.mi-iptv/
    ├── addon.xml
    ├── default.py
    ├── resources/settings.xml
    └── plugin.video.mi-iptv-1.0.0.zip
```
