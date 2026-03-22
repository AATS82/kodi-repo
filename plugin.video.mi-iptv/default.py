# -*- coding: utf-8 -*-
# Plugin IPTV para Kodi 14.2 Helix (Python 2)
# Compatible con Apple TV 3 (A1469)

import sys
import urllib
import urllib2
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

ADDON    = xbmcaddon.Addon()
HANDLE   = int(sys.argv[1])
BASE_URL = sys.argv[0]

# ─────────────────────────────────────────────
# CONFIGURACIÓN — edita sólo estas dos líneas
# ─────────────────────────────────────────────
M3U_URL  = ADDON.getSetting('m3u_url')   # se configura desde ajustes del add-on
# Si prefieres hardcodear para pruebas, comenta la línea de arriba y usa:
# M3U_URL = "https://tu-servidor.com/lista.m3u"
# ─────────────────────────────────────────────


def build_url(query):
    """Construye una URL de plugin con parámetros."""
    return BASE_URL + '?' + urllib.urlencode(query)


def parse_m3u(url):
    """
    Descarga y parsea una lista M3U.
    Retorna lista de dicts: [{'name': ..., 'url': ..., 'logo': ...}, ...]
    """
    channels = []
    try:
        req      = urllib2.Request(url)
        response = urllib2.urlopen(req, timeout=10)
        content  = response.read().decode('utf-8', errors='ignore')
        response.close()
    except Exception as e:
        xbmc.log('Mi-IPTV: Error descargando M3U -> ' + str(e), xbmc.LOGERROR)
        xbmcgui.Dialog().notification('Mi IPTV', 'Error al cargar la lista M3U', xbmcgui.NOTIFICATION_ERROR, 5000)
        return channels

    lines   = content.splitlines()
    channel = {}

    for line in lines:
        line = line.strip()

        if line.startswith('#EXTM3U'):
            continue

        elif line.startswith('#EXTINF'):
            # Ejemplo: #EXTINF:-1 tvg-logo="http://..." group-title="Noticias",Canal 24H
            channel = {'name': '', 'url': '', 'logo': '', 'group': ''}

            # Extraer nombre (lo que va después de la última coma)
            if ',' in line:
                channel['name'] = line.split(',', 1)[-1].strip()

            # Extraer logo
            if 'tvg-logo="' in line:
                try:
                    channel['logo'] = line.split('tvg-logo="')[1].split('"')[0]
                except Exception:
                    pass

            # Extraer grupo
            if 'group-title="' in line:
                try:
                    channel['group'] = line.split('group-title="')[1].split('"')[0]
                except Exception:
                    pass

        elif line and not line.startswith('#') and channel.get('name'):
            channel['url'] = line
            channels.append(channel)
            channel = {}

    return channels


def list_channels():
    """Muestra todos los canales de la lista M3U."""
    if not M3U_URL:
        xbmcgui.Dialog().ok('Mi IPTV', 'Configura la URL del archivo M3U en los ajustes del add-on.')
        ADDON.openSettings()
        return

    xbmc.log('Mi-IPTV: Cargando lista desde ' + M3U_URL, xbmc.LOGINFO)
    channels = parse_m3u(M3U_URL)

    if not channels:
        xbmcgui.Dialog().notification('Mi IPTV', 'No se encontraron canales', xbmcgui.NOTIFICATION_WARNING, 4000)
        return

    for ch in channels:
        list_item = xbmcgui.ListItem(label=ch['name'])
        list_item.setProperty('IsPlayable', 'true')
        list_item.setInfo('video', {'title': ch['name'], 'genre': ch.get('group', '')})

        if ch.get('logo'):
            list_item.setThumbnailImage(ch['logo'])

        url = build_url({'action': 'play', 'url': ch['url']})
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=False)

    xbmcplugin.setContent(HANDLE, 'episodes')
    xbmcplugin.endOfDirectory(HANDLE)


def play_channel(url):
    """Reproduce un canal."""
    xbmc.log('Mi-IPTV: Reproduciendo -> ' + url, xbmc.LOGINFO)
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)


# ── Router principal ──────────────────────────
def router():
    params = {}
    if len(sys.argv) > 2 and sys.argv[2]:
        query_string = sys.argv[2].lstrip('?')
        pairs        = query_string.split('&')
        for pair in pairs:
            if '=' in pair:
                k, v    = pair.split('=', 1)
                params[urllib.unquote_plus(k)] = urllib.unquote_plus(v)

    action = params.get('action', '')

    if action == 'play':
        play_channel(params.get('url', ''))
    else:
        list_channels()


if __name__ == '__main__':
    router()
