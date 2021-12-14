
# 1.  주계부 만들기

## 1.1. 필수요건

- 기간별 입금액, 출금액, 자산평가액, 최고(최저)수익금(율) 확인

## 1.2. 제한요건

- 계좌 수 ~~1개~~ 제한 없음
- python, sql, MariaDB

## 1.3. DB 구성

```
--
 |-- accountbook --    <- 계좌정보: codelist 의 타입설명 확인필요
 |                |-- rel_seq ( 관련 seq 번호)
 |                |-- date (예: 20210101)
 |                |-- agent (예: 한국투자증권 = 001)
 |                |-- trnsc_type (계좌 변동사항: 주식 or 현금 = 0100 or 0200)
 |                |-- trnsc_type_detl (계좌 변동사항 상세: 매수, 매도, 입금 etc)
 |                |-- trnsc_amnt (변동 수량 or 금액)
 |
 | 
 |-- codelist ----- 
                  |-- lcls_cd (대상 컬럼명)
                  |-- comcd (코드: 대상 컬럼의 value)
                  |-- comcd_nm (코드 이름, 대체워딩)
                  |-- comcd_detl (코드상세 설명)
```

## 1.4. 파일구성

## 1.5. UI 구성

https://wikidocs.net/5222
https://1d1cblog.tistory.com/147
