#!/usr/bin/env python3
"""기술영향평가팀 게이트 기계 점검 (표준 라이브러리만).

    python3 ta_check.py ta/ --gate G1        # 한 게이트
    python3 ta_check.py ta/ --gate all       # 있는 파일 모두
    python3 ta_check.py ta/ --gate all --json

기준의 단일 출처는 references/gates.md. 이 점검기는 형식(칸이 채워졌나, 첫 행이 현상 유지인가 등)만 본다.
★ 표시 기준(내용 판단)은 검수관(ta-reviewer)이 본다. 통과 = 형식이 맞음 ≠ 내용이 맞음.
종료 코드: [필수]가 있으면 1, 없으면 0, 입력 폴더가 없으면 2.
"""
import argparse, json, pathlib, re, sys, unicodedata

PLACEHOLDER = re.compile(r'^\s*〔[^〕]*〕\s*$')
LEADER = '〔리더 판단〕'

def nfc(s):
    return unicodedata.normalize('NFC', s)

def read(p):
    return nfc(pathlib.Path(p).read_text(encoding='utf-8'))

def empty(cell):
    c = (cell or '').strip()
    return c == '' or bool(PLACEHOLDER.match(c)) or c in ('-', '—')

def sections(text):
    """'## ' 제목 기준으로 나눈 {제목: 본문}"""
    out, cur, buf = {}, '_head', []
    for line in text.splitlines():
        if line.startswith('## '):
            out[cur] = '\n'.join(buf)
            cur, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out[cur] = '\n'.join(buf)
    return out

def find_section(secs, *keys):
    for k, v in secs.items():
        if any(key in k for key in keys):
            return k, v
    return None, ''

def tables(text):
    """마크다운 표 목록. 각 표 = (머리 목록, 행 목록[dict])"""
    res, lines = [], text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            head = [h.strip() for h in lines[i].strip().strip('|').split('|')]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].strip().startswith('|'):
                cells = [c.strip() for c in lines[j].strip().strip('|').split('|')]
                cells += [''] * (len(head) - len(cells))
                rows.append(dict(zip(head, cells)))
                j += 1
            res.append((head, rows))
            i = j
        else:
            i += 1
    return res

def table_with(text, *cols):
    for head, rows in tables(text):
        if all(any(c in h for h in head) for c in cols):
            return head, rows
    return None, []

def col(head, key):
    for h in head or []:
        if key in h:
            return h
    return None

def kv_lines(text):
    """'- 키: 값' 줄을 dict로"""
    d = {}
    for line in text.splitlines():
        m = re.match(r'^\s*-\s*([^:：]+)[:：]\s*(.*)$', line)
        if m:
            d[m.group(1).strip()] = m.group(2).strip()
    return d

class Report:
    def __init__(self):
        self.items = []
    def add(self, level, gate, where, msg):
        self.items.append({'level': level, 'gate': gate, 'where': where, 'msg': msg})

# ── G1 ─────────────────────────────────────────────────────────────
def g1(root, r):
    p = root / '01_scope.md'
    if not p.exists():
        r.add('필수', 'G1', '01_scope.md', '파일 없음')
        return
    secs = sections(read(p))
    _, s1 = find_section(secs, '평가 질문')
    head, rows = table_with(s1, '질문', '갈래')
    qs = [x for x in rows if not empty(x.get(col(head, '질문'), ''))]
    if not qs:
        r.add('필수', 'G1', '1. 평가 질문', '채운 평가 질문이 없음')
    if len(qs) > 3:
        r.add('권고', 'G1', '1. 평가 질문', f'질문 {len(qs)}개 — 2~3개 권장')
    for x in qs:
        g = x.get(col(head, '갈래'), '')
        if empty(g) or not re.search(r'현황|기회|과제|정책', g):
            r.add('필수', 'G1', f"질문 {x.get(col(head, '번호'), '?')}", '갈래(현황 / 기회·과제 / 정책) 표시 없음')
    _, s3 = find_section(secs, '평가 범위')
    h3, rows3 = table_with(s3, '제외')
    if not any(not empty(x.get(col(h3, '제외'), '')) for x in rows3):
        r.add('필수', 'G1', '3. 평가 범위', '범위 제외 기록이 없음 — 무엇을 왜 뺐는지 적기')
    _, s4 = find_section(secs, '설계 매트릭스')
    h4, rows4 = table_with(s4, '판단 기준', '방법', '한계')
    filled_q = set()
    for x in rows4:
        q = x.get(col(h4, '질문'), '').strip()
        blanks = [h for h in h4 if empty(x.get(h, ''))]
        if blanks and not empty(q):
            r.add('필수', 'G1', f'4. 설계 매트릭스 {q}', '빈 칸: ' + ', '.join(blanks))
        elif not empty(q):
            filled_q.add(q)
    for x in qs:
        qn = x.get(col(head, '번호'), '').strip()
        if qn and qn not in filled_q and not any(qn in fq for fq in filled_q):
            r.add('필수', 'G1', f'4. 설계 매트릭스', f'{qn} 행이 없거나 덜 채워짐')
    _, s6 = find_section(secs, '정책 목표')
    if empty(kv_lines(s6).get('정책 목표', '')):
        r.add('권고', 'G1', '6. 정책 목표', "정책 목표가 비었음 — 없으면 '두지 않음'이라고 적기")
    _, s7 = find_section(secs, '수행 가능성')
    kv7 = kv_lines(s7)
    for k in ('기간', '자료', '위험'):
        if empty(kv7.get(k, '')):
            r.add('권고', 'G1', '7. 수행 가능성', f'{k} 비었음')
    _, s8 = find_section(secs, '리더 승인')
    ap = kv_lines(s8).get('승인', '')
    if empty(ap) or LEADER in ap:
        r.add('필수', 'G1', '8. 리더 승인', '리더 승인 칸이 비었음(사람이 이름·날짜를 씀)')

# ── G2 ─────────────────────────────────────────────────────────────
ITEM_KEYS = {
    '①': r'①|편익|산업',
    '②': r'②|경제|사회|문화|윤리|환경',
    '③': r'③|부작용',
    '④': r'④|성별|특성',
}

def g2(root, r):
    p = root / '02_impact.md'
    if not p.exists():
        r.add('필수', 'G2', '02_impact.md', '파일 없음')
        return
    text = read(p)
    head, rows = table_with(text, '시행령 항목', '크기', '출처')
    rows = [x for x in rows if not empty(x.get(col(head, '영향 영역'), ''))]
    if not rows:
        r.add('필수', 'G2', '1. 영향 행렬', '채운 행이 없음')
        return
    items = ' '.join(x.get(col(head, '시행령 항목'), '') for x in rows)
    for k, pat in ITEM_KEYS.items():
        if not re.search(pat, items):
            r.add('필수', 'G2', '1. 영향 행렬', f'시행령 제23조② 항목 {k}에 해당하는 행이 없음')
    by_area = {}
    for x in rows:
        no = x.get(col(head, '번호'), '?')
        size = x.get(col(head, '크기'), '')
        src = x.get(col(head, '출처'), '')
        if not empty(size) and empty(src):
            r.add('필수', 'G2', f'행 {no}', '크기가 있는데 출처가 없음')
        if '모의' in src and not empty(size):
            r.add('필수', 'G2', f'행 {no}', '모의 패널에서 온 행에 크기를 채움 — 확인 전에는 비워 둠')
        imp = x.get(col(head, '중요도'), '')
        if empty(imp) and LEADER not in imp:
            r.add('권고', 'G2', f'행 {no}', "중요도 칸이 비었음 — '〔리더 판단〕'으로 두거나 리더가 채움")
        area = x.get(col(head, '영향 영역'), '').strip()
        by_area.setdefault(area, set()).add(x.get(col(head, '방향'), '').strip())
    gap_k, gap = find_section(sections(text), '공백')
    gh, grows = table_with(gap, '위치')
    gap_text = ' '.join(' '.join(g.values()) for g in grows if not empty(g.get(col(gh, '위치'), '')))
    for area, dirs in by_area.items():
        has_pos = any('긍정' in d for d in dirs)
        has_neg = any('부정' in d for d in dirs)
        if not (has_pos and has_neg) and area not in gap_text:
            r.add('권고', 'G2', f'영역 {area}', '긍정·부정 짝이 없고 공백 표에도 없음')
    if not gap_text:
        r.add('권고', 'G2', '2. 공백', '공백 표가 비었음 — 빈 칸·한쪽 출처뿐인 곳을 적기')
    q = root / '02b_stakeholders.md'
    if not q.exists():
        r.add('필수', 'G2', '02b_stakeholders.md', '파일 없음')
    else:
        sh, srows = table_with(read(q), '집단')
        if not [x for x in srows if not empty(x.get(col(sh, '집단'), ''))]:
            r.add('필수', 'G2', '02b_stakeholders.md', '채운 집단이 없음')

# ── G3 ─────────────────────────────────────────────────────────────
STATES = ('후보', '선정', '보관', '출처 추적 불가')

def g3(root, r):
    d = root / '03_signals'
    cards = sorted(d.glob('*.md')) if d.exists() else []
    if not cards:
        r.add('필수', 'G3', '03_signals/', '신호 카드가 없음')
    selected = 0
    for c in cards:
        kv = kv_lines(read(c))
        for k in ('제목', '날짜', '출처', '요약', '새로움', '상태'):
            if empty(kv.get(k, '')):
                r.add('필수', 'G3', c.name, f'{k} 칸이 비었음')
        st = kv.get('상태', '').strip()
        if st and st not in STATES:
            r.add('필수', 'G3', c.name, f'상태 값이 규칙 밖: {st}')
        src = kv.get('출처', '')
        if not empty(src) and not re.search(r'https?://|/|\.pdf|\.md', src) and st != '출처 추적 불가':
            r.add('필수', 'G3', c.name, "출처가 추적 가능한 주소·파일이 아님 — 상태를 '출처 추적 불가'로")
        if st == '선정':
            selected += 1
    reps = sorted(root.glob('03_watch_*.md'))
    if not reps:
        r.add('필수', 'G3', '03_watch_*.md', '주간 감시 보고가 없음')
    for rp in reps:
        secs = sections(read(rp))
        _, s2 = find_section(secs, '검토한 출처')
        h2, rows2 = table_with(s2, '출처')
        if not [x for x in rows2 if not empty(x.get(col(h2, '출처'), ''))]:
            r.add('필수', 'G3', rp.name, '검토한 출처 목록이 비었음')
        _, s5 = find_section(secs, '리더 선정')
        sel = kv_lines(s5).get('선정', '')
        if selected and (empty(sel) or LEADER in sel):
            r.add('필수', 'G3', rp.name, "'선정' 카드가 있는데 리더 선정 기록이 비었음 — 선정은 리더가 함")

# ── G4 ─────────────────────────────────────────────────────────────
TYPES = ('증언', '문서', '물리', '자료분석')
NATURES = ('공식 통계', '측정', '업체 자가보고', '추정', '전문가 판단')

def g4(root, r):
    p = root / '04_evidence.md'
    if not p.exists():
        r.add('필수', 'G4', '04_evidence.md', '파일 없음')
        return
    text = read(p)
    secs = sections(text)
    _, s1 = find_section(secs, '증거표')
    head, rows = table_with(s1, '유형', '성격', '출처')
    rows = [x for x in rows if not empty(x.get(col(head, '내용'), ''))]
    if not rows:
        r.add('필수', 'G4', '1. 증거표', '채운 증거가 없음')
    counts = {}
    for x in rows:
        no = x.get(col(head, '번호'), '?')
        t = x.get(col(head, '유형'), '').strip()
        n = x.get(col(head, '성격'), '').strip()
        src = x.get(col(head, '출처'), '')
        if not any(k in t for k in TYPES):
            r.add('필수', 'G4', f'증거 {no}', f'유형이 규칙 밖: {t or "(빈 칸)"}')
        if not any(k in n for k in NATURES):
            r.add('필수', 'G4', f'증거 {no}', f'성격이 규칙 밖: {n or "(빈 칸)"}')
        if empty(src):
            r.add('필수', 'G4', f'증거 {no}', '출처가 없음')
        if '자료분석' in t and not re.search(r'/|\.py|\.csv|\.ipynb|\.R\b|analysis', src):
            r.add('필수', 'G4', f'증거 {no}', '자료분석인데 결과 파일·코드 경로가 없음(다시 돌릴 수 있게)')
        if '모의' in src:
            r.add('필수', 'G4', f'증거 {no}', '모의 패널 내용을 증거로 넣음')
        key = next((k for k in TYPES if k in t), t)
        counts[key] = counts.get(key, 0) + 1
    if len(rows) >= 5:
        top = max(counts.values())
        if top / len(rows) > 0.8:
            r.add('권고', 'G4', '3. 분포', f'증거 유형이 한쪽에 쏠림({counts}) — 한계에 적기')
    _, s2 = find_section(secs, '발견사항')
    h2, rows2 = table_with(s2, '발견사항', '근거')
    rows2 = [x for x in rows2 if not empty(x.get(col(h2, '발견사항'), ''))]
    if not rows2:
        r.add('필수', 'G4', '2. 발견사항', '채운 발견사항이 없음')
    for x in rows2:
        no = x.get(col(h2, '번호'), '?')
        if not re.search(r'E\d', x.get(col(h2, '근거'), '')):
            r.add('필수', 'G4', f'발견 {no}', '근거 증거 번호(E…)가 없음')
        for k in ('충분', '불확실성'):
            if empty(x.get(col(h2, k), '')):
                r.add('필수', 'G4', f'발견 {no}', f'{k} 칸이 비었음')

# ── G5 ─────────────────────────────────────────────────────────────
def g5(root, r):
    p = root / '06_report.md'
    if not p.exists():
        r.add('필수', 'G5', '06_report.md', '파일 없음')
        return
    text = read(p)
    secs = sections(text)
    for n, name in [('1', '평가 질문'), ('3', '영향'), ('5', '근거'), ('6', '정책 옵션'), ('7', '의견 수렴'), ('8', '생략')]:
        if not any(k.startswith(n + '.') or name in k for k in secs):
            r.add('필수', 'G5', '06_report.md', f'{n}장({name}) 제목이 없음')
    body = '\n'.join(v for k, v in secs.items() if re.match(r'^[1-6]\.', k))
    if re.search(r'모의 패널|모의 검토|\bP\d+\b|페르소나', body):
        r.add('필수', 'G5', '1~6장', '모의 패널·페르소나 내용이 본문 근거로 들어감 — 7.2로 옮기기')
    nosrc = []
    for line in body.splitlines():
        bare = re.sub(r'\b[QIEFOHP]\d+\b|S-\d{6}-\d+|\d+\.\d*장|\d+장', '', line)   # 번호표(Q1·I2·O0 등)는 수치가 아님
        if re.match(r'^\s*[-□○]', line) and re.search(r'\d', bare) and not re.search(r'\(|https?://|출처|〔|E\d|I\d|F\d', line):
            nosrc.append(line.strip()[:40])
    if nosrc:
        r.add('권고', 'G5', '1~6장', f'수치가 있는데 출처 표시가 안 보이는 줄 {len(nosrc)}개 — 예: {nosrc[0]}')

# ── G6 ─────────────────────────────────────────────────────────────
def g6(root, r):
    p = root / '05_options.md'
    if not p.exists():
        r.add('필수', 'G6', '05_options.md', '파일 없음')
        return
    text = read(p)
    head, rows = table_with(text, '옵션', '주체')
    if any('순위' in h for h in head or []):
        r.add('필수', 'G6', '옵션 표', '순위 열이 있음 — 옵션은 순위 없는 메뉴')
    rows = [x for x in rows if not empty(x.get(col(head, '옵션'), ''))]
    if not rows:
        r.add('필수', 'G6', '옵션 표', '채운 옵션이 없음')
        return
    if '현상 유지' not in rows[0].get(col(head, '옵션'), ''):
        r.add('필수', 'G6', '옵션 표', '첫 행이 현상 유지가 아님')
    for x in rows:
        no = x.get(col(head, '번호'), '?')
        if empty(x.get(col(head, '주체'), '')):
            r.add('필수', 'G6', f'옵션 {no}', '받는 주체가 없음')
        if not re.search(r'[IF]\d', x.get(col(head, '근거'), '')):
            r.add('필수', 'G6', f'옵션 {no}', '근거 행 번호(I… 또는 F…)가 없음')
        if re.search(r'해야 한다|하여야 한다|해야 함', ' '.join(x.values())):
            r.add('권고', 'G6', f'옵션 {no}', "'해야 한다' — 옵션은 권고가 아님, '방안이 있음'으로")
    _, pri = find_section(sections(text), '우선순위')
    if re.search(r'\d+\s*점|\b\d+\s*/\s*10\b', pri) and not re.search(r'매김|매긴|채점', pri):
        r.add('권고', 'G6', '우선순위', '점수가 있는데 누가 매겼는지 없음')
    rep = root / '06_report.md'
    if rep.exists():
        rt = read(rep)
        if not re.search(r'실제 검토', rt) or not re.search(r'모의 검토', rt):
            r.add('필수', 'G6', '06_report.md 7장', '실제 검토와 모의 검토를 나눈 절이 없음')
    for pf in sorted(root.glob('07_panel_*.md')):
        if pf.name == '07_panel_personas.md':
            continue
        first = next((l for l in read(pf).splitlines() if l.startswith('# ')), '')
        if '증거 아님' not in first:
            r.add('필수', 'G6', pf.name, "제목에 '증거 아님' 표지가 없음")

GATES = {'G1': g1, 'G2': g2, 'G3': g3, 'G4': g4, 'G5': g5, 'G6': g6}
FILES = {'G1': ['01_scope.md'], 'G2': ['02_impact.md'], 'G3': ['03_signals', '03_watch_'],
         'G4': ['04_evidence.md'], 'G5': ['06_report.md'], 'G6': ['05_options.md']}

def present(root, gate):
    for f in FILES[gate]:
        if f.endswith('_'):
            if list(root.glob(f + '*.md')):
                return True
        elif (root / f).exists():
            return True
    return False

def main():
    ap = argparse.ArgumentParser(description='기술영향평가팀 게이트 기계 점검')
    ap.add_argument('root', help='작업 폴더(보통 ta/)')
    ap.add_argument('--gate', default='all', help='G1~G6 또는 all')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    if not root.is_dir():
        print(f'작업 폴더가 없음: {root}', file=sys.stderr)
        sys.exit(2)
    r = Report()
    gates = list(GATES) if a.gate == 'all' else [g.strip().upper() for g in a.gate.split(',')]
    for g in gates:
        if g not in GATES:
            print(f'모르는 게이트: {g}', file=sys.stderr)
            sys.exit(2)
        if a.gate == 'all' and not present(root, g):
            continue
        GATES[g](root, r)
    must = sum(1 for i in r.items if i['level'] == '필수')
    if a.json:
        print(json.dumps(r.items, ensure_ascii=False, indent=1))
    else:
        order = {'필수': 0, '권고': 1}
        for i in sorted(r.items, key=lambda i: (i['gate'], order[i['level']])):
            print(f"[{i['level']}] {i['gate']} | {i['where']} | {i['msg']}")
        rec = sum(1 for i in r.items if i['level'] == '권고')
        print(f'→ 필수 {must} · 권고 {rec}  (형식 점검만 함 — ★ 기준은 검수관이 판정)')
    sys.exit(1 if must else 0)

if __name__ == '__main__':
    main()
