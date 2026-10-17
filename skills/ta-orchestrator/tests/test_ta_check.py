"""ta_check.py 시험: python3 -m unittest discover -s skills/ta-orchestrator/tests"""
import pathlib, shutil, subprocess, sys, tempfile, unittest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE.parent / 'scripts' / 'ta_check.py'
SKILLS = HERE.parent.parent

GOOD = {
'01_scope.md': """# 평가 설계서
- 의뢰자: 강의자
- 대상 기술: AI 에이전트
## 1. 평가 질문
| 번호 | 질문 | 갈래 |
|---|---|---|
| Q1 | AI 에이전트는 공공 업무에서 어디까지 쓰이나 | 현황 |
| Q2 | 이익을 키우고 피해를 줄일 정책 옵션은 무엇인가 | 정책 |
## 2. 대상 기술의 조작적 정의
- 목표를 받아 계획하고 도구를 써서 실행하는 AI(KISTEP 2025, 11쪽)
## 3. 평가 범위
| 축 | 포함 | 제외(이유) |
|---|---|---|
| 기술 범위 | 소프트웨어 에이전트 | 물리적 AI(로봇) — 수업 기간 |
## 4. 설계 매트릭스
| 질문 | 판단 기준 | 필요 정보와 출처 | 방법 | 한계 |
|---|---|---|---|---|
| Q1 | 도입 사례 수 | 기관 발표 | 문헌 | 공개 사례만 |
| Q2 | 옵션의 기회·고려사항 | 정책 문서 | 문헌·모의 패널 | 실제 참여 없음 |
## 6. 정책 목표와 치우침 점검
- 정책 목표: 공공 업무에서 이익은 키우고 피해는 줄인다
- 치우침 점검: 규제·진흥 어느 쪽도 미리 정하지 않음
## 7. 수행 가능성
- 기간: 5주
- 자료: 공개 보고서
- 위험: 자료 편중
## 8. 리더 승인 (G1)
- 승인: 박주이 2026. 10. 31.
""",
'02_impact.md': """# 영향 행렬
- 대상 기술 자체 근거: 크기 칸이 찬 행 4개 중 1건
## 1. 영향 행렬
| 번호 | 영향 영역 | 시행령 항목 | 영향받는 집단 | 방향 | 크기(근거 있는 사실) | 출처 | 중요도(리더) |
|---|---|---|---|---|---|---|---|
| I1 | 업무 생산성 | ① | 공무원 | 긍정 | 과제 약 30% 완수(연구 1건) | GAO-25-108519 1쪽 | 높음 |
| I2 | 업무 생산성 | ① | 공무원 | 부정 | 감독 부담 | GAO-25-108519 2쪽 | 〔리더 판단〕 |
| I3 | 책임 | ② | 시민 | 부정 | 책임 소재 불분명 | KISTEP 2025 18쪽 | 〔리더 판단〕 |
| I4 | 책임 | ③ | 시민 | 긍정 | 법적 지위 규정 제안 | KISTEP 2025 43쪽 | 〔리더 판단〕 |
| I5 | 접근성 | ④ | 고령자 | 부정 | 〔채울 것〕 | 〔채울 것〕 | 〔리더 판단〕 |
| I6 | 접근성 | ④ | 고령자 | 긍정 | 〔채울 것〕 | 〔채울 것〕 | 〔리더 판단〕 |
## 2. 공백
| 위치 | 왜 공백인가 | 다음에 할 일 |
|---|---|---|
| I5·I6 | 근거 없음 | 조사 |
""",
'02b_stakeholders.md': """# 이해관계자 목록
| 번호 | 집단 | 어떤 영향(02 행 번호) | 이 집단의 공개 입장 자료 | 출처 |
|---|---|---|---|---|
| H1 | 공무원 | I1 | 찾지 못함 | — |
""",
'03_signals/S-261107-01.md': """- id: S-261107-01
- 제목: 새 에이전트 규제 공지
- 날짜: 2026. 11. 5.
- 출처: https://example.org/notice
- 요약: 규제 기관이 공지함 판별: 〔에이전트〕
- 새로움: 처음 나온 지침
- 상태: 선정
""",
'03_watch_261107.md': """# 주간 감시 보고
## 2. 검토한 출처
| 출처 | 감시 주기 | 이번에 본 범위 |
|---|---|---|
| 과기정통부 보도자료 | 매주 | 11. 1.~7. |
## 5. 리더 선정 (G3)
- 선정: S-261107-01 (박주이)
""",
'04_evidence.md': """# 증거표와 발견사항
## 1. 증거표
| 번호 | 내용 | 유형 | 성격 | 출처 | 연결 |
|---|---|---|---|---|---|
| E1 | 최고 성능 에이전트가 과제 약 30% 완수 | 문서 | 측정 | GAO-25-108519 1쪽 | I1 |
| E2 | AI 안건 연도별 건수 | 자료분석 | 공식 통계 | ta/analysis/count.py → out.csv | Q1 |
## 2. 발견사항
| 번호 | 발견사항 | 근거 | 충분·적절 | 불확실성 |
|---|---|---|---|---|
| F1 | 성능은 제한적 | E1 | 부족 — 연구 1건 | 높음 |
## 3. 증거 유형 분포와 한계
- 문서 1, 자료분석 1
""",
'05_options.md': """# 정책 옵션
| 번호 | 옵션 | 실행 방안 예시 | 기회 | 고려사항 | 주체 | 근거 |
|---|---|---|---|---|---|---|
| O0 | 현상 유지 | 지금 그대로 | 부담 없음 | 위험 지속 | 과기정통부 | I3 |
| O1 | 도입 전 성능 평가 | 시험 절차 | 신뢰 | 비용 | 도입 기관 | F1 |
""",
'06_report.md': """# AI 에이전트 기술영향평가
## 0. 요약
- 발견 F1
## 1. 평가 질문과 범위
- Q1·Q2(01_scope.md)
## 3. 영향 분석
- I1~I6
## 5. 근거와 불확실성
- F1
## 6. 정책 옵션
- O0·O1
## 7. 의견 수렴과 검토
### 7.1 실제 검토(사람)
### 7.2 모의 검토(AI 페르소나)
## 8. 생략한 단계
- 시민포럼
""",
'07_panel_citizen_261121.md': """# 모의 검토(AI 페르소나) — 증거 아님
""",
}

def write(root, files):
    for name, body in files.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding='utf-8')

def run(root, gate='all'):
    return subprocess.run([sys.executable, str(SCRIPT), str(root), '--gate', gate],
                          capture_output=True, text=True)

class T(unittest.TestCase):
    def setUp(self):
        self.d = pathlib.Path(tempfile.mkdtemp())
    def tearDown(self):
        shutil.rmtree(self.d)

    def test_good_passes(self):
        write(self.d, GOOD)
        r = run(self.d)
        self.assertEqual(r.returncode, 0, r.stdout)

    def mutate(self, name, old, new, gate, expect):
        files = dict(GOOD)
        self.assertIn(old, files[name])
        files[name] = files[name].replace(old, new)
        write(self.d, files)
        r = run(self.d, gate)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn(expect, r.stdout)

    def test_g1_no_exclusion(self):
        self.mutate('01_scope.md', '물리적 AI(로봇) — 수업 기간', '〔채울 것〕', 'G1', '범위 제외')
    def test_g1_no_branch(self):
        self.mutate('01_scope.md', '| 현황 |', '| 〔현황 / 기회·과제 / 정책〕 |', 'G1', '갈래')
    def test_g1_leader_blank(self):
        self.mutate('01_scope.md', '박주이 2026. 10. 31.', '〔리더 판단〕', 'G1', '리더 승인')
    def test_g2_missing_item(self):
        self.mutate('02_impact.md', '| ④ |', '| ① |', 'G2', '④')
    def test_g2_size_without_source(self):
        self.mutate('02_impact.md', 'GAO-25-108519 2쪽', '〔채울 것〕', 'G2', '출처가 없음')
    def test_g2_mock_with_size(self):
        self.mutate('02_impact.md', 'KISTEP 2025 18쪽', '모의 패널 — 확인 필요', 'G2', '모의 패널')
    def test_g3_selected_without_leader(self):
        self.mutate('03_watch_261107.md', 'S-261107-01 (박주이)', '〔리더 판단〕', 'G3', '리더 선정')
    def test_g3_untraceable(self):
        self.mutate('03_signals/S-261107-01.md', 'https://example.org/notice', '어디선가 봄', 'G3', '추적')
    def test_g4_bad_nature(self):
        self.mutate('04_evidence.md', '| 측정 |', '| 대충 |', 'G4', '성격')
    def test_g4_analysis_without_file(self):
        self.mutate('04_evidence.md', 'ta/analysis/count.py → out.csv', '내가 셈', 'G4', '결과 파일')
    def test_g5_mock_in_body(self):
        self.mutate('06_report.md', '- I1~I6', '- 모의 패널 P1이 우려함', 'G5', '모의 패널')
    def test_g6_status_quo_not_first(self):
        self.mutate('05_options.md', '| O0 | 현상 유지 |', '| O0 | 규제 신설 |', 'G6', '현상 유지')
    def test_g6_rank_column(self):
        self.mutate('05_options.md', '| 근거 |\n', '| 근거 | 순위 |\n', 'G6', '순위')
    def test_g6_panel_label(self):
        self.mutate('07_panel_citizen_261121.md', ' — 증거 아님', '', 'G6', '증거 아님')

    def test_g1_nested_list_counts_as_filled(self):
        """'- 자료:' 아래 하위 목록으로 채운 경우 비었다고 하지 않음(실제 호출 시험에서 나온 오탐)"""
        files = dict(GOOD)
        files['01_scope.md'] = files['01_scope.md'].replace('- 자료: 공개 보고서', '- 자료:\n  - 구할 수 있는 것: 공개 보고서\n  - 구하기 어려운 것: 내부 현황')
        write(self.d, files)
        r = run(self.d, 'G1')
        self.assertNotIn('자료 비었음', r.stdout)

    def test_g2_own_evidence_line(self):
        files = dict(GOOD)
        files['02_impact.md'] = files['02_impact.md'].replace('- 대상 기술 자체 근거: 크기 칸이 찬 행 4개 중 1건\n', '')
        write(self.d, files)
        self.assertIn('대상 기술 자체 근거', run(self.d, 'G2').stdout)

    def test_g3_two_tags(self):
        files = dict(GOOD)
        files['03_signals/S-261107-01.md'] = files['03_signals/S-261107-01.md'].replace('판별: 〔에이전트〕', '판별: 〔에이전트〕 그러나 〔유사 기술〕에 가까움')
        write(self.d, files)
        self.assertIn('판별 표시가 하나가 아님', run(self.d, 'G3').stdout)

    def test_blank_templates_fail(self):
        """빈 템플릿을 그대로 두면 통과하지 못해야 함"""
        tpl = {
            '01_scope.md': SKILLS / 'ta-scope/templates/01_scope.md',
            '02_impact.md': SKILLS / 'ta-impact/templates/02_impact.md',
            '02b_stakeholders.md': SKILLS / 'ta-impact/templates/02b_stakeholders.md',
            '04_evidence.md': SKILLS / 'ta-evidence/templates/04_evidence.md',
            '05_options.md': SKILLS / 'ta-options/templates/05_options.md',
        }
        for name, src in tpl.items():
            shutil.copy(src, self.d / name)
        for g in ('G1', 'G2', 'G4', 'G6'):
            r = run(self.d, g)
            self.assertEqual(r.returncode, 1, f'{g}: {r.stdout}')

if __name__ == '__main__':
    unittest.main()
