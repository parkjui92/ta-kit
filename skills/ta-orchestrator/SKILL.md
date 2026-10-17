---
name: ta-orchestrator
description: "수업용 기술영향평가(Technology Assessment) 에이전트 팀의 전체 진행자. 범위 결정과 평가 질문 → 영향 식별 → 지평 탐색 → 증거 평가 → 정책 옵션과 외부 검토를 조사관·정리관·감시관·분석관·모의 패널관·검수관 6역할과 게이트 6개(G1~G6)로 진행하고, 단계마다 리더(사람)의 승인을 받는다. '기술영향평가 해 보자', '기술영향평가 전체 진행', 'TA 보고서 만들기', '게이트 판정', '어디까지 했지', '이 팀 구조 보여줘(뜯어보기)', '기준 결과물 만들기' 요청에 사용한다. 한 단계만 할 때는 ta-scope · ta-impact · ta-horizon · ta-evidence · ta-options · ta-panel을 직접 써도 된다."
---

# 기술영향평가팀 진행

실제 기관(미국 GAO · 한국 KISTEP · 유럽 기술평가기관)의 절차를 수업용으로 줄인 팀이다. 역할과 게이트가 어디서 왔는지는 [references/basis.md](references/basis.md)에 있다.

**먼저 읽는다**: [references/workspace.md](references/workspace.md)(폴더 규약) · [references/gates.md](references/gates.md)(게이트 기준)

## 역할

| 역할 | 에이전트 | 단계 스킬 |
|---|---|---|
| 리더(사람) | — | 승인·판단 |
| 조사관 | `ta-scout` | `ta-scope` |
| 정리관 | `ta-mapper` | `ta-impact` |
| 감시관 | `ta-watcher` | `ta-horizon` |
| 분석관 | `ta-analyst` | `ta-evidence` · `ta-options` |
| 모의 패널관 | `ta-panel` | `ta-panel` |
| 검수관(읽기 전용) | `ta-reviewer` | 모든 게이트 |

에이전트 이름에 플러그인 이름이 붙어 보이면(`ta-kit:ta-scout`) 그 이름으로 부른다.

## 모드

### 1. 단계 모드 (수업 기본)

리더가 한 단계만 하려 하면 그 단계 스킬로 넘긴다. 어느 단계인지 모르면 `ta/` 폴더를 보고 다음 단계를 제안한다.

| 있는 파일 | 다음 단계 |
|---|---|
| 없음 또는 `00_request.md`만 | 범위 결정 → `ta-scope` |
| `01_scope.md`(G1 승인) | 영향 식별 → `ta-impact` |
| `02_impact.md`(G2 통과) | 지평 탐색 → `ta-horizon` |
| `03_watch_*.md` | 증거 평가 → `ta-evidence` |
| `04_evidence.md`(G4 통과) | 정책 옵션 → `ta-options` |
| `05_options.md` | 모의 패널 예행 → `ta-panel`, 보고서 조립·G5·G6 |

지난 단계 파일이 없으면 수업 공용 저장소의 시작 폴더에서 복사해 시작하도록 안내한다(한 주를 놓쳐도 시작할 수 있게).

### 2. 전체 모드 (강의자의 기준 결과물 만들기)

`00_request.md`부터 `06_report.md`까지 차례로 진행한다. **단계마다 게이트를 지나고 리더 승인을 받은 뒤에** 다음으로 간다. 승인 없이 다음 단계로 넘어가지 않는다.

1. 조사관 → `01_scope.md` → G1
2. 정리관 → `02_impact.md`·`02b_stakeholders.md` → G2
3. 감시관 → `03_signals/`·`03_watch_*.md` → G3(리더 선정)
4. 분석관 → `04_evidence.md` → G4
5. 분석관 → `05_options.md`
6. 모의 패널관 → `07_panel_*`(예행)
7. 분석관 → `06_report.md` 조립
8. 검수관 → G5 · G6

### 3. 뜯어보기 모드 (13주차)

"이 팀 구조 보여줘", "역할이 어디서 왔나"면 [references/basis.md](references/basis.md)로 답한다. 순서:
1. 결과물(`06_report.md`)만 먼저 보여 주고 역할·순서·게이트를 리더가 예상하게 한다
2. 그다음 이 플러그인의 `agents/`와 `skills/` 파일을 열어 대조한다
3. 생략한 단계([references/omitted-steps.md](references/omitted-steps.md))와 실제 보고서(KISTEP 「2025년 기술영향평가」 등)를 맞대어 '빠진 역할'을 찾게 한다

## 게이트 돌리는 법

1. 기계 점검(파이썬이 있으면):
   ```bash
   python3 <이 스킬 폴더>/scripts/ta_check.py ta/ --gate G1
   ```
   `--gate all`이면 있는 파일을 모두 본다. [필수]가 나오면 작성 에이전트에게 돌려보낸다
2. 검수관 판정: `ta-reviewer`를 부르고 게이트 번호·파일·기계 점검 결과를 준다. **작성한 에이전트에게 판정을 맡기지 않는다**
3. 판정서를 `ta/gates/G<n>_YYMMDD.md`로 저장하고 리더에게 진행/보류를 묻는다
4. `_log.md`에 단계·게이트·결과를 한 줄씩 남긴다

## 원칙

- **리더가 하는 일을 에이전트가 하지 않는다**: 범위 확정, 영향의 중요도, 신호 선정, 게이트 승인
- **모의 패널은 증거가 아니다**: 보고서 7.2에만 적는다
- **실제 참여를 대신하지 않는다**: 시민 참여·전문가 회의·관계 기관 의견은 보고서 8장 '생략한 단계'에 적는다
- **정책 옵션은 권고가 아니다**: 현상 유지 첫 행, 순위 없음
- **출처 없는 사실은 근거가 아니다**: 원문을 열어 확인한 것만 단정한다
