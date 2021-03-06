
# 1.  주계부(AccountBook) 만들기

## 1.1. 필수요건

1. 제작환경
   - Raspberry Pi 4
   - Python 3.7.3
   - PyMySql 1.0.2
   - MariaDB 15.1
2. 기능 요구사항
   - 기간별 입금액
   - 출금액
   - 자산평가액
   - 최고(최저)수익금(율) 확인

## 1.2. 제한요건

- 계좌 수 ~~1개~~ 제한 없음

## 1.3. DB 구성

Task List
- [x] 종목코드, 평균(BEP)단가 입력을 위한 column 필요
- [ ] 주식거래 시 현금 보유금액 변동사항 자동 입력 필요

```
--
 |-- accountbook --    <- 계좌정보: codelist 의 타입설명 확인필요
 |                |-- rel_seq ( 관련 seq 번호)
 |                |-- date (예: 20210101)
 |                |-- agent (예: 한국투자증권 = 001)
 |                |-- trnsc_type (계좌 변동사항: 주식 or 현금 = 0100 or 0200)
 |                |-- trnsc_type_sub (주식: 종목코드, or 현금: 통화종류 = GOOG or C010)
 |                |-- trnsc_type_detl (계좌 변동사항 상세: 매수, 매도, 입금 etc)
 |                |-- trnsc_amnt (변동 수량 or 금액)
 |
 | 
 |-- codelist ----- 
 |                |-- lcls_cd (대상 컬럼명)
 |                |-- comcd (코드: 대상 컬럼의 value)
 |                |-- comcd_nm (코드 이름, 대체워딩)
 |                |-- comcd_detl (코드상세 설명)
 |
 |
 |-- savings ------ 
                  |-- date (예: 20210101)
                  |-- agent (코드 예: 한국투자증권 = 001)
                  |-- tgt_agent (코드 예: 한국투자증권 = 001)
                  |-- trnsc_reason (코드: 이체 사유, )
                  |-- trnsc_amnt (금액)
```

## 1.4. 파일구성

## 1.5. UI 구성

## 1.6. 사용법

1. 계좌의 주식을 변경할 때에는 주식매수도(0101, 0102) 중 하나를 선택한다.
2. 계좌의 외화를 변경할 때에는 외화화전(0211, 0212) 중 하나를 선택한다.
2. trnsc_type_detl 이 주식매수도(0101, 0102), 환전(0211, 0212) 인 경우에는 **반드시** 현금의 입출금(0201, 0202)이 따라야 한다. (check_reg.py 실행으로 확인가능)
