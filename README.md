# ta-kit — 수업용 기술영향평가 에이전트 팀

기술영향평가(Technology Assessment)를 **실제 기관의 절차대로** 연습하는 Claude Code 플러그인입니다. 미국 GAO, 한국 KISTEP, 유럽 기술평가기관(독일 TAB·네덜란드 Rathenau·영국 POST·EU JRC)의 절차를 수업용으로 줄여, 역할 6개와 게이트 6개로 나눴습니다.

> 이 팀은 실제 기술영향평가를 대신하지 않습니다. 시민 참여·전문가 회의·관계 기관 의견 같은 단계는 하지 않으며, 보고서 8장 '생략한 단계'에 그 사실을 적게 되어 있습니다.

## 단계와 역할

| 단계 | 하는 일 | 역할(에이전트) | 스킬 | 게이트 |
|---|---|---|---|---|
| 범위 결정과 평가 질문 | 초기 상황 분석, 평가 질문, 범위와 범위 제외, 설계 매트릭스 | 조사관 `ta-scout` | `ta-scope` | G1 평가 설계 승인 |
| 영향 식별 | 영향 행렬(크기는 사실, 중요도는 사람), 이해관계자, 공백 | 정리관 `ta-mapper` | `ta-impact` | G2 영향 균형 |
| 지평 탐색과 상시 모니터링 | 신호 카드, 주간 감시 보고(선정은 사람) | 감시관 `ta-watcher` | `ta-horizon` | G3 신호 입구 |
| 증거 평가 | 증거 유형·성격, 충분성 판정, 불확실성 | 분석관 `ta-analyst` | `ta-evidence` | G4 증거 충분성 |
| 정책 옵션과 외부 검토 | 옵션 표(현상 유지 첫 행·순위 없음), 보고서 조립 | 분석관 `ta-analyst` | `ta-options` | G5 출처 독립 대조 · G6 옵션·외부 검토 |
| 참여 예행연습 | AI 페르소나 모의 패널(증거 아님) | 모의 패널관 `ta-panel` | `ta-panel` | G6 예행 |
| 모든 게이트 판정 | 쓰지 않은 사람이 확인 | 검수관 `ta-reviewer`(읽기 전용) | — | G1~G6 |

전체 진행·게이트 순서·뜯어보기는 `ta-orchestrator` 스킬이 맡습니다.

## 수업용과 실무용

수업용으로 만들었지만 절차 자체는 기관 절차의 축약이라 실무 사전 검토에도 쓸 수 있습니다. 실무로 쓸 때는 두 가지만 다릅니다.

- 리더 자리에 강의자 대신 평가 책임자가 앉고, 게이트 승인은 그 사람이 합니다
- 모의 패널(AI 페르소나)은 실제 참여 단계를 대신하지 못하므로, 보고서 8장 '생략한 단계'를 그대로 두고 실제 참여 절차를 따로 계획합니다

공통 사례(AI 에이전트)로 9~16주차를 진행한 기준 결과물과 주차별 시작 폴더는 사례 저장소 [ta-ai-agent](https://github.com/parkjui92/ta-ai-agent)에 있습니다.

**사람(리더)이 하는 일**: 범위 확정, 영향의 중요도 판단, 신호 선정, 게이트 승인. 에이전트는 이 칸을 채우지 않습니다.

## 쓰는 법

설치한 뒤 Claude Code에서 짧게 말하면 됩니다.

| 하고 싶은 것 | 이렇게 말하기 |
|---|---|
| 평가 질문 정하기 | 평가 질문 정하자 |
| 영향 정리하기 | 영향 행렬 만들어줘 |
| 동향 감시하기 | 이번 주 감시 보고 만들어줘 |
| 증거 정리하기 | 증거가 충분한지 봐줘 |
| 정책 옵션과 보고서 | 정책 옵션 만들고 보고서로 묶어줘 |
| AI 페르소나 검토 | 시민 패널 모의 검토 돌려줘 |
| 처음부터 끝까지 | 기술영향평가 전체 진행해줘 |
| 이 팀 구조 뜯어보기 | 이 팀 구조가 어디서 왔는지 보여줘 |

결과물은 프로젝트의 `ta/` 폴더에 쌓입니다. 폴더 규약은 [skills/ta-orchestrator/references/workspace.md](skills/ta-orchestrator/references/workspace.md).

## 게이트 기계 점검(선택)

```bash
python3 skills/ta-orchestrator/scripts/ta_check.py ta/ --gate all
```

형식(칸이 채워졌나, 첫 옵션이 현상 유지인가 등)만 봅니다. 내용 판단은 검수관이 합니다. 시험: `python3 -m unittest discover -s skills/ta-orchestrator/tests`

## 모의 패널(AI 페르소나)에 대해

실제 평가의 참여 단계를 AI 페르소나로 예행연습합니다. 페르소나는 실제 선발 기준(KISTEP 시민포럼, 「인공지능기본법 시행령」 인공지능취약계층, GAO 전문가 균형)과 그 집단의 실제 공개 입장 자료로 짭니다. 결과는 **증거가 아니며** '사람에게 물어볼 질문'과 '빈 관점 후보'로만 씁니다. 언어 모델이 사람 표본을 대신할 때의 한계(응답 변이가 작음, 집단을 납작하게 그림 등)는 [agents/ta-panel.md](agents/ta-panel.md)에 근거 문헌과 함께 적었습니다.

## 근거

역할·게이트마다 어느 기관 절차에서 왔는지, 무엇을 생략했는지는 [skills/ta-orchestrator/references/basis.md](skills/ta-orchestrator/references/basis.md)에 있습니다. 주요 원문:

- GAO, *Technology Assessment Design Handbook*(GAO-21-347G, 2021)
- GAO, *Generative AI's Environmental and Human Effects*(GAO-25-107172, 2025) · *Science & Tech Spotlight: AI Agents*(GAO-25-108519, 2025) · *On the Horizon*(GAO-25-107542, 2024)
- KISTEP, 「2025년 기술영향평가」(대상기술: AI 에이전트) · 「2024년 기술영향평가」(안전·신뢰 AI)
- 「과학기술기본법」 제14조와 시행령 제23조 · 「인공지능기본법」 제35조와 시행령 제28조
- EU JRC, *Scanning Deep Tech Horizons*(2023) · European Commission, *Better Regulation Toolbox* Tool #18

## 라이선스

MIT. 인용한 보고서의 이용 조건은 각 원문을 따릅니다(GAO는 미국 정부 저작물, KISTEP 보고서는 공공누리 표시가 없어 인용·요약만).
