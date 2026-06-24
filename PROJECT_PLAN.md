# Apple Game Reinforcement Learning Agent

## 1. 프로젝트 개요

### 프로젝트명

Apple Game Reinforcement Learning Agent

### 프로젝트 목표

Apple Game의 플레이 전략을 학습하여 실제 게임에서 높은 점수를 획득하는 강화학습 에이전트를 개발한다.

### 최종 목표

* 실제 게임 규칙을 재현한 환경 구축
* 강화학습 기반 에이전트 학습
* 실제 게임과 유사한 보드에서 높은 점수 획득
* Random Agent 및 Greedy Agent 대비 성능 향상 검증

---

# 2. 게임 규칙 정의

## 보드

* 보드 크기: 가로 17개, 세로 10개 (최대 사과 수: 170개)
* 각 사과는 1~9의 숫자를 가짐
* 시작 시 랜덤 배치

예시

```text
1 5 3 2
9 2 7 1
4 6 1 8
```

---

## 행동 규칙

사용자는 직사각형 영역을 선택할 수 있다.

허용되는 형태

```text
1x1
1xN
Nx1
NxM
```

모든 직사각형 선택 가능

---

## 제거 조건

선택한 직사각형 내부 숫자 합이 정확히 10인 경우 제거

예시

```text
1 2
3 4
```

합 = 10

↓

제거

---

## 제거 결과

제거된 사과는 영구 삭제된다.

```text
1 2
3 4
```

↓

```text
0 0
0 0
```

---

## 빈칸 규칙

* 제거된 칸은 0으로 처리
* 직사각형 선택 가능
* 합 계산 시 0 포함

예시

```text
1 0
2 7
```

합 = 10

↓

제거 가능

---

## 점수 규칙

제거된 사과 개수만큼 점수 획득

예시

```text
1 + 9
```

↓

2개 제거

↓

2점

---

```text
1 2
3 4
```

↓

4개 제거

↓

4점

---

## 종료 조건

### 자동 종료

합이 10인 직사각형이 더 이상 존재하지 않음

### 강제 종료

사용자가 종료 버튼을 선택

---

# 3. 강화학습 환경 설계

## Observation (State)

초기 버전

```python
{
    "board": board,
    "score": score,
    "remaining_apples": remaining_apples,
    "turn_count": turn_count
}
```

향후 실험

```python
{
    "board": board
}
```

만 사용하는 버전도 검증

---

## Action

직사각형 좌표 방식 사용

```python
(x1, y1, x2, y2)
```

예시

```python
(2, 1, 4, 3)
```

의미

```text
좌상단 (2,1)
우하단 (4,3)
```

---

## Reward

즉시 보상

```python
reward = removed_apple_count
```

예시

```text
2개 제거 → +2
5개 제거 → +5
```

---

## Episode 종료

```python
done = no_valid_rectangle
```

---

## 최종 점수

```python
final_score = sum(reward)
```

에피소드 동안 획득한 reward 총합

---

# 4. 시스템 구조

## apple_env.py

역할

* reset()
* step()
* 종료 판정
* 점수 계산

---

## board_generator.py

역할

* 초기 보드 생성
* 숫자 분포 관리
* 랜덤 시드 관리

---

## action_finder.py

역할

* 현재 보드의 유효 행동 탐색
* 합이 10인 직사각형 계산

출력

```python
[
    (x1, y1, x2, y2),
    ...
]
```

---

## logger.py

역할

* 학습 로그 저장
* 디버깅 로그 저장
* 에피소드 결과 저장

예시

```json
{
  "episode": 120,
  "score": 97,
  "remaining": 12
}
```

---

# 5. 기준 플레이어(Baseline)

## Random Agent

행동

```python
random.choice(valid_actions)
```

목적

* 환경 검증
* 최소 성능 측정

---

## Greedy Agent

행동

```text
가장 많은 사과를 제거하는 직사각형 선택
```

목적

* 강화학습 비교 기준선(Baseline)

---

# 6. 강화학습 단계

## Phase 1

환경 구축

완료 조건

```text
랜덤 플레이 가능
```

---

## Phase 2

Random Agent 평가

측정

* 평균 점수
* 최고 점수
* 최저 점수

---

## Phase 3

Greedy Agent 평가

측정

* 평균 점수
* 최고 점수
* 최저 점수

---

## Phase 4

PPO Agent 학습

학습 목표

```text
PPO > Random Agent
PPO > Greedy Agent
```

---

## Phase 5

하이퍼파라미터 튜닝

실험 항목

* Learning Rate
* Batch Size
* Gamma
* Entropy Coefficient
* Clip Range

---

# 7. 실제 게임 데이터 수집

## 목적

강화학습 데이터 생성용이 아닌 환경 현실성 개선용

---

## 크롤러

수집 대상

```text
초기 보드 상태
```

---

## 분석 항목

### 숫자 분포

```text
1 : ?
2 : ?
3 : ?
4 : ?
5 : ?
6 : ?
7 : ?
8 : ?
9 : ?
```

---

### 유효 행동 수

```text
평균 직사각형 개수
최대 직사각형 개수
최소 직사각형 개수
```

---

### 평균 점수

```text
사용자 플레이 결과 분석
```

---

## 생성기 개선

기존

```python
random.randint(1, 9)
```

↓

실제 수집된 숫자 분포 반영

---

# 8. 최종 평가

비교 대상

| Agent  | 평균 점수 |
| ------ | ----- |
| Random | 측정    |
| Greedy | 측정    |
| PPO    | 측정    |

---

## 성공 기준

1. PPO > Random
2. PPO > Greedy
3. 실제 게임 보드에서도 높은 점수 유지

---

# 9. 향후 확장

## MCTS Agent 추가

강화학습과 비교 실험

---

## PPO + MCTS 결합

성능 향상 여부 검증

---

## CNN 기반 정책 네트워크

보드 패턴 학습

---

## Transformer 기반 정책 네트워크

장거리 패턴 학습

---

# 10. 우선 구현 순서

1. action_finder.py
2. apple_env.py
3. board_generator.py
4. Random Agent
5. Greedy Agent
6. PPO Agent
7. Logger
8. 크롤러
9. 실제 게임 평가

---

# 핵심 원칙

* 목표는 실제 게임에서 높은 점수 획득
* 강화학습은 목표 달성을 위한 수단
* 모든 판단 기준은 실제 게임 성능 향상 여부
* 환경 구현 및 행동 탐색 로직을 우선 완성

---
이 문서는 현재 설계 기준의 v0.1 초안으로 보고, 실제 구현을 시작하면서 보드 크기, 상태 표현, 행동 마스킹, PPO 모델 구조, 크롤러 설계를 추가하는 방식으로 버전업해야합니다.