1. This spiderbot is for downloading stock data of US market via yahoo finance
2. The 3 csv files (AMEX,NASDAQ,NYSE) were downloaded from https://www.nasdaq.com/screening/company-list.aspx. For the purpose of reducing bugs in code, i modified those files slightly.
3. Any stocks weren’t downloaded successfully because of date reason will be written in error_log.txt in its own folder.
4. Special bug: PRN is a stock in NASDAQ, which is also a reserved name from DOS days(https://superuser.com/questions/688145/cannot-create-con-csv-or-prn-csv-in-win7), so i can only delete it from NASDAQ.csv and download it separately in as name "PRN~.csv" at the end of the downloading process.
5. There is very little chance that the bot will stuck at a point(downloaded over 10000 stocks data and stocked 3 times ), but i think it's internet reason.

Author:

Huang Mengda

huangmengda15@mails.ucas.ac.cn
