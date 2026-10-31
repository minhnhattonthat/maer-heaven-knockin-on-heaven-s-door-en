"""release.py: build the English ROM and package the patch, stopping at the first failed gate.

    python -X utf8 tools/release.py [VERSION] [--force]      VERSION defaults to 1.0

Gates in order: build -> tests + lint (check.py) -> smoke boot -> jp_left (known noise in tools/jp_left_known.txt)
-> qa_gate check on every work/qa/**/manifest.tsv -> no unticked line in docs/polish.md -> debug scripts unchanged
-> BPS patch -> re-apply to the clean original and compare -> zip (patch + README.txt from docs/release-readme.txt).
Output: release/MAER_Heaven_EN_vVERSION.{bps,zip}. Refuses to overwrite them without --force. Never publishes.
"""
import hashlib
import re
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))


def run(*cmd):
    print('$', ' '.join(str(c) for c in cmd), flush=True)
    if subprocess.call([str(c) for c in cmd], cwd=ROOT):
        sys.exit('release stopped: %s failed' % Path(str(cmd[2])).name)


def main(a):
    if '-h' in a or '--help' in a:
        sys.exit(__doc__)
    force = '--force' in a
    a = [x for x in a if not x.startswith('--')]
    ver = a[0] if a else '1.0'
    out = ROOT / 'release'
    bps_path, zip_path = out / ('MAER_Heaven_EN_v%s.bps' % ver), out / ('MAER_Heaven_EN_v%s.zip' % ver)
    if not force and (bps_path.exists() or zip_path.exists()):
        sys.exit('%s exists: pass --force to overwrite' % zip_path.name)

    import bps
    import build
    import nfp
    py = [sys.executable, '-X', 'utf8']
    skill = Path(subprocess.check_output(py + [ROOT / 'tools' / 'skill.py'], text=True).strip()) / 'scripts'
    rom_path, built = build.ROM, build.OUT

    run(*py, ROOT / 'tools' / 'build.py')
    run(*py, ROOT / 'tools' / 'check.py')
    run(*py, skill / 'emu.py', built, '--out', ROOT / 'work' / 'qa' / 'smoke', '--route',
        ROOT / 'tools' / 'routes' / 'boot.txt', '--smoke')
    run(*py, skill / 'jp_left.py', built, '--orig', rom_path, '--sjis', '--gba-ptrs',
        '--known', ROOT / 'tools' / 'jp_left_known.txt')
    manifests = sorted((ROOT / 'work' / 'qa').rglob('manifest.tsv'))
    if len(manifests) < 2:  # visual tour + story pass
        sys.exit('release stopped: expected the tour and story manifests, found %s' % manifests)
    for m in manifests:
        run(*py, skill / 'qa_gate.py', 'check', m, m.parent / 'verdicts')
    open_items = [x for x in (ROOT / 'docs' / 'polish.md').read_text('utf-8').splitlines() if x.startswith('- [ ]')]
    if open_items:
        sys.exit('release stopped: %d unticked lines in docs/polish.md, first: %s' % (len(open_items), open_items[0]))

    src, tgt = rom_path.read_bytes(), built.read_bytes()
    orig, new = dict(nfp.unpack(src)), dict(nfp.unpack(tgt))
    for name in ('DBG_ESC.SPC', 'CH_ESC.SPC'):  # debug room / chapter select stay as shipped (unreachable in game)
        if orig[name] != new[name]:
            sys.exit('release stopped: debug script %s changed' % name)

    patch = bps.make(src, tgt)
    if bps.apply(src, patch) != tgt:
        sys.exit('release stopped: patch does not reproduce the build')
    out.mkdir(exist_ok=True)
    bps_path.write_bytes(patch)
    readme = (ROOT / 'docs' / 'release-readme.txt').read_text('utf-8').format(
        version=ver, patch=bps_path.name, base_size=len(src), base_crc32='%08X' % zlib.crc32(src),
        base_md5=hashlib.md5(src).hexdigest(), base_sha1=hashlib.sha1(src).hexdigest(),
        out_crc32='%08X' % zlib.crc32(tgt), out_sha1=hashlib.sha1(tgt).hexdigest())
    assert not re.search(r'\{\w+\}', readme), 'unfilled placeholder in docs/release-readme.txt'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr(bps_path.name, patch)
        z.writestr('README.txt', readme.replace('\n', '\r\n'))
    with zipfile.ZipFile(zip_path) as z:  # what the player gets reproduces the build
        if bps.apply(src, z.read(bps_path.name)) != tgt:
            sys.exit('release stopped: zipped patch does not reproduce the build')
    print('%s: %d bytes; patch sha1 %s; patched crc32 %08X' % (zip_path, zip_path.stat().st_size,
                                                                 hashlib.sha1(patch).hexdigest(), zlib.crc32(tgt)))


if __name__ == '__main__':
    main(sys.argv[1:])
