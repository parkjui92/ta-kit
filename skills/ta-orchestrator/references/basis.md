# 팀 설계 근거표 — 이 역할·게이트는 어디서 왔나

리버스 엔지니어링(뜯어보기) 자료. 역할과 게이트마다 **실제 기관의 어느 절차에서 왔는지**, 그리고 **이 팀이 무엇을 생략했는지**를 적는다. 쪽수는 원문 인쇄 쪽.

## 출처 약칭

| 약칭 | 원문 | 이용 조건 |
|---|---|---|
| GAO-H | GAO, *Technology Assessment Design Handbook*, GAO-21-347G, 2021. 2. — https://www.gao.gov/products/gao-21-347g | 미국 정부 저작물, 재배포 가능 |
| GAO-GenAI | GAO, *Artificial Intelligence: Generative AI's Environmental and Human Effects*, GAO-25-107172, 2025. 4. — https://www.gao.gov/products/gao-25-107172 | 같음 |
| GAO-Horizon | GAO, *On the Horizon: Three Science and Technology Trends that Could Affect Society*, GAO-25-107542, 2024. 11. | 같음 |
| GAO-Agents | GAO, *Science & Tech Spotlight: AI Agents*, GAO-25-108519, 2025. 9. | 같음(사진은 스톡 이미지) |
| KISTEP-25 | KISTEP, 「2025년 기술영향평가」(대상기술: AI 에이전트), 2026. 2. — https://www.kistep.re.kr/reportDetail.es?mid=a10305020000&rpt_tp=831-006&rpt_no=RES0220260029 | 공공누리 표시 없음 → 인용·요약만 |
| KISTEP-24 | KISTEP, 「2024년 기술영향평가」(대상기술: 안전·신뢰 AI), 2025. 3. | 같음 |
| 법 | 「과학기술기본법」 제14조, 같은 법 시행령 제23조 / 「인공지능 발전과 신뢰 기반 조성 등에 관한 기본법」 제35조, 같은 법 시행령 제28조 | 법령 |
| TAB | 독일 연방의회 기술영향평가처 — 주제 선정 절차, 배경보고서 Nr. 26(ChatGPT, 2023) | KITopen 라이선스(학술·개인 사용) |
| JRC | EU JRC, *Scanning Deep Tech Horizons*(2023) | EU 재사용 정책 |
| EU-TB | European Commission, *Better Regulation Toolbox* Tool #18 영향 식별 | EU 재사용 정책 |
| Leopold | Leopold 외(1971), USGS Circular 645 영향 행렬 | 미국 정부 저작물 |
| Stilgoe | Stilgoe·Owen·Macnaghten(2013), Research Policy 42(9) | 저작권 문헌, 인용만 |
| DBT | 덴마크 기술위원회 합의회의 절차 | 인용만 |

## 역할

| 역할 | 하는 일 | 기관 근거 | 이 팀이 생략한 것 |
|---|---|---|---|
| 리더(사람) | 의뢰·범위 확정, 게이트 승인, 중요도·신호 선정 | GAO 요청자·수임 회의(GAO-H 부록 Ⅲ p.48), 과기정통부 대상 확정(KISTEP-25 5쪽) | 의회·부처 협의 |
| 조사관 | 초기 상황 분석, 문서 증거 수집 | GAO 초기 상황 분석(GAO-H p.16), KISTEP 분석평가그룹 동향 분석(KISTEP-25 5쪽) | 전문가 면담, 현장 방문 |
| 정리관 | 영향 식별, 이해관계자 목록, 공백 표시 | EU-TB Tool #18 1단계(140쪽), GAO 스케일링 행렬(GAO-H p.58), Leopold 크기·중요도 분리 | 정량 영향 모형 |
| 감시관 | 신호 수집·입구 규칙·주간 보고 | GAO 상시 모니터링(GAO-H p.19·26), GAO-Horizon, JRC 입구 규칙(11쪽), TAB 지평 탐색 기준 | 전문가 의미 부여 워크숍, 텍스트 마이닝 대량 수집 |
| 분석관 | 증거 평가, 정책 옵션 분석, 보고서 조립 | GAO 메시지 합의 전 분석(GAO-H 부록 Ⅲ p.50), 옵션 분석 차원(p.19·62) | 통계적 일반화 표본, 편익-비용 분석 |
| 모의 패널관 | AI 페르소나로 시민·전문가·관계 기관 검토 예행 | 형식만 빌림: KISTEP 시민포럼(KISTEP-25 7~8쪽), GAO 전문가 회의·기관 기술 의견(GAO-GenAI p.33·35~36) | **실제 참여 자체**. 모의 결과는 증거가 아님 |
| 검수관 | 게이트 판정, 출처 독립 대조 | GAO 출처 독립 대조(GAO-H 부록 Ⅲ p.50), KISTEP 위원회 결과 검토(KISTEP-25 5쪽), 영국 POST 출간 전 검토 | 법률 검토, 교열·공식 발간 |

## 게이트

| 게이트 | 기관 근거 |
|---|---|
| G1 평가 설계 승인 | GAO 수임 회의·설계 검토 회의(GAO-H 부록 Ⅲ p.48~49), 질문 세 갈래(p.20), TAB 수행 가능성 의견서, KISTEP 선정 기준(KISTEP-25 6쪽) |
| G2 영향 균형 | 시행령 제23조② 4개 항목, KISTEP 긍정·부정 구조, Leopold, EU-TB Tool #18 |
| G3 신호 입구 | JRC 입구 규칙, TAB 지평 탐색 기준, 선정은 사람 |
| G4 증거 충분성 | GAO 메시지 합의 회의(GAO-H 부록 Ⅲ p.50), 증거 유형(부록 Ⅳ), 불확실성 표 6(p.26) |
| G5 출처 독립 대조 | GAO indexing and referencing(부록 Ⅲ p.50) |
| G6 옵션·외부 검토 | GAO 옵션 표·현상 유지·순위 없음(GAO-GenAI p.29~30, GAO-H p.20·63), 외부 검토(GAO-GenAI p.33), KISTEP 우선순위 지표(KISTEP-25 40쪽), 결과 활용 경로(시행령 제23조⑥⑦) |

## 뜯어보기에서 함께 볼 질문

- 같은 'AI 에이전트'를 GAO는 2쪽(GAO-Agents), KISTEP은 240쪽(KISTEP-25)으로 다뤘다. 깊이가 다르면 무엇이 달라지나
- KISTEP-24는 스스로 "영향 영역을 시행령 항목대로 기계적으로 나눠 핵심이슈 파악이 어렵다"고 적었다(요약 xiii쪽). 우리 팀의 정리관은 이 실패를 피했나
- 우리 결과와 KISTEP-25 10대 정책 제언을 나란히 놓으면, 우리에게 없는 역할은 무엇인가

## 주의

- GAO 핸드북 문장 대부분은 '할 수 있다(may)'다. "GAO는 반드시 이렇게 한다"로 말하지 않는다. 의무인 것은 품질보증체계 준수, 충분하고 적절한 증거, 한계 공개 정도다
- 평가 유형은 "합의된 단일 분류가 없다"(GAO-H p.2 각주 7). 수업의 두 축 그림(언제 평가하나 × 누가 평가하나)은 수업용 정리다
