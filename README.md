# Olist 데이터 분석·AI 대시보드

브라질 온라인 쇼핑몰 **Olist**의 주문 데이터를 분석하고 수업에서 학습한 머신러닝 모델을 실행하는 **Streamlit 교육용 웹앱**입니다.

## 주요 기능

| 메뉴 | 기능 |
| --- | --- |
| 홈 | 실습 소개와 메뉴 안내 |
| 데이터 분석 | 지역·기간별 주문, 매출, 배송 지연, 리뷰 평점, 월별 추이와 상품군 분석 |
| 리뷰 감성 분석 | 포르투갈어 리뷰의 긍정·부정을 머신러닝으로 분류 |
| 상품 추천 | 동일 카테고리에서 특징이 비슷한 상품 5개 추천 |
| 판매자 유형 | 판매자 특성을 핵심 우량·신규 성장·휴면·저평점 위험으로 분류 |
| 판매자 이탈 위험 | 다음 3개월에 주문이 없을 가능성을 계산하여 판매자 관리 순위 제시 |
| 분석 Q&A | 사실표·모델 설명서·실습용 가상 규정집을 찾아 근거 ID와 함께 답변하는 RAG 챗봇 |

## 폴더 구성

```text
Olist/
├── app.py                 # 실행 파일
├── requirements.txt       # 필요한 Python 라이브러리
├── .gitignore
├── views/                 # 화면별 코드
│   ├── home.py
│   ├── analysis.py
│   ├── sentiment.py
│   ├── recommend.py
│   ├── segment.py
│   ├── churn.py
│   └── qa.py
├── utils/                 # 데이터·모델·RAG 처리 코드
├── model/                 # 학습 모델 4개(.pkl)
└── data/                  # 주문·상품·판매자 자료와 RAG 참고문서
```

## 실행 방법 (Windows / VS Code)

1. 저장소를 내려받습니다.
2. **`data/orders.parquet` 및 `data/items.parquet`가 존재하는지 확인합니다.** 현재 GitHub 등록본에는 이 두 파일이 없을 수 있으므로 아래 자료 준비를 참고하세요.
3. VS Code에서 저장소 폴더를 열고 터미널에서 아래 명령어를 차례로 실행합니다.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py --server.port 8501
```

4. 브라우저에서 `http://localhost:8501`에 접속합니다.

가상환경이 이미 활성화됐다면 `python -m streamlit run app.py --server.port 8501`을 사용해도 됩니다.

## 데이터 준비

**필요한 파일**

- `data/orders.parquet` — 주문 데이터
- `data/items.parquet` — 주문 상품 데이터
- `data/seller_table.csv` — 판매자 이탈 분석용 데이터
- `data/olist_facts.csv` — 분석 사실표
- `data/olist_model_guide.md` — 학습한 모델 설명서
- `data/olist_seller_policy.pdf` — RAG 학습용 **가상** 판매자 운영 규정집

자료 출처(수업용 Google Drive 원본 폴더): [Olist 실습 자료](https://drive.google.com/drive/folders/1E85eBWLumgiQl5h05XCullIBE9N9qbke)

특히 주문 데이터 2개가 없으면 **데이터 분석 메뉴는 실행할 수 없습니다.** 두 파일은 Drive 실습 자료의 `olist_dashboard/data` 폴더에서 내려받아 넣으세요.

## 학습 모델

| 파일 | 용도 |
| --- | --- |
| `model/part6_recommend.pkl` | KNN 기반 비슷한 상품 추천 |
| `model/part7_1_sentiment_ml.pkl` | TF-IDF·로지스틱 회귀 기반 리뷰 감성 분석 |
| `model/part8_seller_segment.pkl` | K-Means 기반 판매자 유형 분류 |
| `model/part9_seller_churn.pkl` | 로지스틱 회귀 기반 판매자 이탈 위험 계산 |

실습 모델은 **scikit-learn 1.6.1**을 기준으로 저장됐습니다. `requirements.txt`에 지정한 버전을 유지하세요. 포르투갈어 리뷰로 학습한 감성 모델은 한국어·영어 분석에 적합하지 않습니다.

## RAG 분석 Q&A

RAG는 질문과 관련된 **실습 자료를 먼저 검색한 뒤**, 그 근거를 이용해 답하도록 만든 방식입니다.

- A: 분석 사실표
- B: 사실표 + 모델 설명서
- C: 사실표 + 모델 설명서 + 가상 규정집

이 기능에는 **OpenAI API 키가 필요**하며 사용량에 따라 별도 비용이 발생할 수 있습니다. API 키는 GitHub에 올리지 말고 Streamlit 비밀 설정(`.streamlit/secrets.toml`) 또는 환경변수 `OPENAI_API_KEY`에 입력하세요.

가상 규정집은 실제 Olist 정책이 아니며, 질문 답변도 취재·보도 등 외부 용도로 사용하기 전에 원문 확인이 필요합니다.

## 참고 및 한계

- 이 프로젝트는 MBC 데이터 저널리즘 교육과정의 실습 결과물입니다.
- 판매자 '이탈'은 실제 폐업이 아니라 실습에서 정한 **향후 3개월간 주문 0건**을 뜻합니다.
- 추천 모델은 함께 구매한 상품이 아니라 **가격·크기·평점 등 특징이 유사한 상품**을 찾습니다.
- 모델 예측은 실습용 결과이며 실제 사업 판단에 바로 적용해서는 안 됩니다.
