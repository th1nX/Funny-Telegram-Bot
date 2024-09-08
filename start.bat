@echo off
IF EXIST .env (
pip install -r requirements.txt
main.py
pause
) ELSE (
echo CREATED .env FILE. && echo PLEASE CHECK IT AND SET IT UP THEN.
(echo API_ID = WRITE_YOUR_API_ID_INSTEAD && echo API_HASH = WRITE_YOUR_API_HASH_INSTEAD && echo PHONE_NUMBER = WRITE_ACCOUNT_PHONE_NUMBER_INSTEAD && echo ALLOWED_TGIDS = []) > .env
)
