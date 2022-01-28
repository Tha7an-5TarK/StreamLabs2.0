import subprocess
lnk = "magnet:?xt=urn:btih:28D54353D45E508B7F4E3F65D3091D4068C09EA4&dn=Batman+The+Long+Halloween+Part+One.2021.BDRip.XviD.AC3-EVO&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2F47.ip-51-68-199.eu%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce" 

def run_file(magnet_link: str, download: bool):
    cmd = ""
    cmd= cmd + "webtorrent"
    cmd=cmd+" download "
    cmd=cmd+'"{}"'.format(magnet_link)
    if not download:
        print('streamming...')
        cmd=cmd+' --vlc'
        subprocess.call(cmd, shell=True)
        # print(cmd)

run_file(lnk, False)