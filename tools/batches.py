"""batches.py: translation batches (docs/translator-brief.md).

    python -X utf8 tools/batches.py split [--kind script|code|records] [--chars 3500]
    python -X utf8 tools/batches.py check bNNN          validate work/tl/bNNN.out.tsv; prints OK or the errors
    python -X utf8 tools/batches.py merge bNNN [...]    check, then write the English into script/
    python -X utf8 tools/batches.py fit "English" [--lines 2] [--list]   dry-run wrap / width
    python -X utf8 tools/batches.py labels              fill every speaker label from glossary.md
    python -X utf8 tools/batches.py pairs bNNN          work/tl/bNNN.pairs.txt for the reviewer

Units: a script message box (its text lines; the speaker label is filled by `labels`), deduplicated by speaker +
Japanese + line count; a code string (script/code.json, not `keep` windows); a record name/description,
deduplicated by Japanese. Batch TSV: id, speaker, form, limit, jp (' / ' between the box's lines). Output TSV:
id, English; a script box is word-wrapped onto its lines (' / ' forces a break). Not batched: CH_ESC.SPC (debug,
stays Japanese) and the 2 composed item boxes (`concat`, set by hand).
"""
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import lint  # noqa: E402

TL = ROOT / 'work' / 'tl'
TERMS = ROOT / 'build'
SCRIPT = ROOT / 'script'
SKIP = {'CH_ESC'}
HONOR = {'さん': '-san', 'くん': '-kun', 'ちゃん': '-chan', 'さま': '-sama', '様': '-sama', '君': '-kun'}


def load_store():
    """{path: [entries]} for every file of script/ (merge edits these dicts, save() writes them back)."""
    ps = sorted((SCRIPT / 'spc').glob('*.json')) + [SCRIPT / 'code.json', SCRIPT / 'records.json']
    return OrderedDict((p, lint.load(p)) for p in ps)


def save(store):
    for p, ents in store.items():
        s = json.dumps(ents, ensure_ascii=False, indent=1) + '\n'
        if s != p.read_text(encoding='utf-8'):
            p.write_text(s, encoding='utf-8', newline='\n')


def units(store=None):
    """OrderedDict {unit id: dict(kind, speaker, form, limit, jp, members, ...)} in story-file order."""
    store = store or load_store()
    out, seen, bx = OrderedDict(), {}, OrderedDict()
    for p, ents in store.items():
        if p.parent.name == 'spc':
            for e in ents:
                bx.setdefault((p.stem, e['box']), []).append(e)
    for (spc, box), v in bx.items():
        if spc in SKIP:
            continue
        lab = [e for e in v if lint.is_label(e)]
        slots = [e for e in v if e not in lab]
        if not any(e['jp'] for e in slots) or any(e.get('concat') for e in slots):
            continue
        spk = lab[0]['jp'].split('［')[1].split('］')[0] if lab else '-'
        key = (spk, tuple(e['jp'] for e in slots if e['jp']), len(slots))
        if key in seen:
            out[seen[key]]['members'].append(slots)
            continue
        uid = next(e['id'] for e in slots if e['jp'])
        seen[key] = uid
        out[uid] = dict(kind='script', speaker=spk, form='dlg' if lab else 'narration', lines=len(slots),
                        limit='%dx%dpx' % (len(slots), lint.LINE_PX), jp=' / '.join(key[1]), members=[slots])
    wins = lint.code_windows()
    for e in store[SCRIPT / 'code.json']:
        w = wins.get(e['id'], {'name': '?'})
        if w.get('keep'):
            continue
        note = w.get('composed', {}).get(e['id'], '')
        lim = '%spx %s' % (w.get('px', '?'), w.get('renderer', '?')) + (' (%s)' % note if note else '')
        out[e['id']] = dict(kind='code', speaker=w['name'], form='code', limit=lim, jp=e['jp'], members=[e], win=w)
    rec = {}
    for e in store[SCRIPT / 'records.json']:
        f ='arm_name' if e['id'].endswith('.name') else 'arm_desc'
        k = (f, e['jp'])
        if k in rec:
            out[rec[k]]['members'].append(e)
            continue
        rec[k] = e['id']
        out[e['id']] = dict(kind='records', speaker='-', form=f,
                            limit='%dpx/%dB' % (lint.WIN[f]['px'], e['max']), jp=e['jp'], members=[e])
    return out


def done(u):
    if u['kind'] == 'script':
        return all(e.get('en') or not e['jp'] for e in u['members'][0])
    return bool(u['members'][0].get('en'))


def read_tsv(p):
    rows = []
    for ln in Path(p).read_text(encoding='utf-8').splitlines():
        if ln.strip():
            rows.append(ln.split('\t'))
    return rows


# --- glossary -------------------------------------------------------------------------------------------------

def glossary():
    """[(section, jp, en, notes, avoid)] from the tables of glossary.md."""
    rows, sec = [], ''
    for ln in (ROOT / 'glossary.md').read_text(encoding='utf-8').splitlines():
        if ln.startswith('## '):
            sec = ln[3:].strip()
        elif ln.startswith('|') and not set(ln) <= set('|- '):
            c = [x.strip() for x in ln.strip('|').split('|')]
            if len(c) >= 2 and c[0] not in ('JP', '') and c[1]:
                rows.append((sec, c[0], c[1], c[3] if len(c) > 3 else '', c[4] if len(c) > 4 else ''))
    return rows


def _cls(ch):
    o = ord(ch)
    return 'k' if 0x30A0 <= o <= 0x30FF or 0xFF21 <= o <= 0xFF5A else 'h' if 0x3040 <= o <= 0x309F else \
        'c' if 0x4E00 <= o <= 0x9FFF else 'o'


def has_term(jp, term):
    """term occurs in jp as a whole run: the characters around it are not of the term's script class
    (no ミン inside タイミング); hiragana terms always need an exact class break too."""
    for m in re.finditer(re.escape(term), jp):
        a, b = m.start(), m.end()
        if (a == 0 or _cls(jp[a - 1]) != _cls(term[0])) and (b == len(jp) or _cls(jp[b]) != _cls(term[-1])):
            return True
    return False


def terms_for(jps, rows=None):
    rows = rows if rows is not None else glossary()
    return [r for r in rows if any(has_term(j, r[1]) for j in jps)]


# --- split ----------------------------------------------------------------------------------------------------

def split(kind='script', chars=3500):
    TL.mkdir(parents=True, exist_ok=True)
    TERMS.mkdir(parents=True, exist_ok=True)
    taken = {u for p in TL.glob('b[0-9][0-9][0-9].tsv') for u in (r[0] for r in read_tsv(p))}
    n = max([int(p.stem[1:4]) for p in TL.glob('b[0-9][0-9][0-9].tsv')] + [0])
    todo = [(i, u) for i, u in units().items() if u['kind'] == kind and not done(u) and i not in taken]
    batches, cur, size = [], [], 0
    for i, u in todo:
        if cur and size + len(u['jp']) > chars:
            batches.append(cur)
            cur, size = [], 0
        cur.append((i, u))
        size += len(u['jp'])
    if cur:
        batches.append(cur)
    rows = glossary()
    for b in batches:
        n += 1
        name = 'b%03d' % n
        p = TL / (name + '.tsv')
        assert not p.exists(), p
        p.write_text(''.join('%s\t%s\t%s\t%s\t%s\n' % (i, u['speaker'], u['form'], u['limit'], u['jp'])
                             for i, u in b), encoding='utf-8', newline='\n')
        t = terms_for([u['jp'] for _, u in b], rows)
        (TERMS / ('terms_%s.txt' % name)).write_text(
            ''.join('%s\t%s\t%s%s\n' % (r[1], r[2], r[3], '\tAVOID: ' + r[4] if r[4] else '') for r in t),
            encoding='utf-8', newline='\n')
        print('%s: %d units, %d JP chars, %d terms' % (name, len(b), sum(len(u['jp']) for _, u in b), len(t)))
    if not batches:
        print('nothing to split')


# --- check / merge --------------------------------------------------------------------------------------------

def check_unit(u, en, rows):
    errs = lint.char_errors(en)
    if '\\u' in en or '\t' in en:
        errs.append('escape or tab in English')
    if u['kind'] == 'script':
        _, err = lint.wrap(en, u['lines'])
        if err:
            errs.append(err)
        if lint.codes(en) != lint.codes(u['jp']):
            errs.append('codes %s != jp %s' % (lint.codes(en), lint.codes(u['jp'])))
        elif re.match(r'\{C', u['jp']) and not en.startswith(u['jp'][:7]):
            errs.append('must start with %s like the Japanese' % u['jp'][:7])
    elif u['kind'] == 'code':
        errs += lint.code_errors(u['members'][0], en, u['win'])
    else:
        errs += lint.record_errors(u['members'][0], en)
    for sec, jp, ten, notes, avoid in rows:
        if 'loose' in notes or not (ten[:1].isupper() or ten[:1] == 'Ä') or not has_term(u['jp'], jp):
            continue
        forms = [f.strip() for f in ten.split('/')]
        if not any(f.lower() in en.lower() for f in forms):
            errs.append('glossary: %s -> %s missing' % (jp, ten))
        for a in filter(None, (x.strip() for x in avoid.split(','))):
            if re.search(r'\b%s\b' % re.escape(a), en):
                errs.append('glossary: avoid %r (%s)' % (a, jp))
    names = {jp for sec, jp, *_ in rows if sec == 'Characters'}
    for m in re.finditer(r'([ァ-ヶー]+)(さん|くん|ちゃん|さま|様|君)', u['jp']):
        if m.group(1) in names and HONOR[m.group(2)] not in en:  # ガイドさん, オレさま: not a name
            errs.append('honorific %s: expected %s' % (m.group(0), HONOR[m.group(2)]))
    return errs


def check(name, us=None, quiet=False):
    us = us or units()
    inp = [r[0] for r in read_tsv(TL / (name + '.tsv'))]
    outp = TL / (name + '.out.tsv')
    if not outp.exists():
        print('%s: no %s' % (name, outp.name))
        return None
    out, errs = OrderedDict(), []
    for r in read_tsv(outp):
        if len(r) != 2:
            errs.append('line %r: need id<TAB>English' % '\t'.join(r)[:60])
            continue
        if r[0] in out:
            errs.append('%s: duplicate id' % r[0])
        out[r[0]] = r[1].strip()
    errs += ['%s: missing' % i for i in inp if i not in out]
    errs += ['%s: not in the batch' % i for i in out if i not in inp]
    rows = glossary()
    for i, en in out.items():
        if i in us and i in inp:
            errs += ['%s: %s' % (i, x) for x in check_unit(us[i], en, rows)]
    if not quiet or errs:
        for x in errs:
            print(x)
        print('%s: %s' % (name, 'OK' if not errs else '%d errors' % len(errs)))
    return out if not errs else None


def place(lines, slots):
    """English lines -> one string per slot. Starts at the Japanese's first used line when the English still fits
    from there (a narration line in the middle of the box stays there); a Japanese line centred with fullwidth
    spaces gets its English centred with spaces."""
    first = next(k for k, e in enumerate(slots) if e['jp'])
    k = first if first + len(lines) <= len(slots) else 0
    out = [''] * k + list(lines) + [''] * (len(slots) - k - len(lines))
    if all(e['jp'].startswith('　　') for e in slots if e['jp']):
        sp = lint.width(' ')
        out = [' ' * ((lint.LINE_PX - lint.width(s)) // 2 // sp) + s if s else s for s in out]
    return out


def merge(names):
    store = load_store()
    us = units(store)
    for name in names:
        out = check(name, us)
        if out is None:
            return 1
        for i, en in out.items():
            u = us[i]
            for m in u['members']:
                if u['kind'] == 'script':
                    lines = place(lint.wrap(en, u['lines'])[0], m)
                    for e, ln in zip(m, lines):
                        e['en'] = ln if ln or not e['jp'] else ' '  # a Japanese line the English doesn't need: blank
                else:
                    m['en'] = en
    save(store)
    print('merged %s' % ' '.join(names))
    return 0


def labels():
    """Speaker labels: ［name］ -> [English] from the glossary's Characters table (＆ joins two names)."""
    names = {jp: en for sec, jp, en, _, _ in glossary() if sec == 'Characters'}
    store, missing = load_store(), set()
    for p, ents in store.items():
        for e in ents:
            if p.parent.name == 'spc' and p.stem not in SKIP and lint.is_label(e):
                jp = e['jp'].split('［')[1].split('］')[0]
                parts = [names.get(x) for x in jp.split('＆')]
                if names.get(jp) or all(parts):
                    e['en'] = e['jp'].split('［')[0] + '[%s]' % (names.get(jp) or ' & '.join(parts)) + \
                        e['jp'].split('］')[1]
                else:
                    missing.add(jp)
    for m in sorted(missing):
        print('no Characters row for', m)
    save(store)
    return 1 if missing else 0


def pairs(name):
    us = units()
    out = dict((r[0], r[1]) for r in read_tsv(TL / (name + '.out.tsv')))
    lines = ['>> %s | %s | %s | %s\n   %s\n' % (i, us[i]['speaker'], us[i]['limit'], us[i]['jp'], out.get(i, ''))
             for i in (r[0] for r in read_tsv(TL / (name + '.tsv')))]
    (TL / (name + '.pairs.txt')).write_text(''.join(lines), encoding='utf-8', newline='\n')
    print(TL / (name + '.pairs.txt'))


def main(a):
    cmd = a[0] if a else ''
    opt = {a[k][2:]: a[k + 1] for k in range(len(a) - 1) if a[k].startswith('--') and a[k] != '--list'}
    if cmd == 'split':
        split(opt.get('kind', 'script'), int(opt.get('chars', 3500)))
    elif cmd == 'check':
        return 0 if all(check(n) is not None for n in a[1:]) else 1
    elif cmd == 'merge':
        return merge(a[1:])
    elif cmd == 'labels':
        return labels()
    elif cmd == 'pairs':
        for n in a[1:]:
            pairs(n)
    elif cmd == 'fit':
        en = a[1]
        if '--list' in a:
            print('%d px (list)' % lint.list_width(en))
        else:
            lines, err = lint.wrap(en, int(opt.get('lines', 2)))
            for ln in lines:
                print('%3d px | %s' % (lint.width(ln), ln))
            print(err or 'fits')
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
