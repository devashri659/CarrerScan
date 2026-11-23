@echo off
title CareerScan - Job Offer Risk Checker
cd /d "%~dp0"
echo ========================================================
echo   Starting CareerScan Web Application...
echo   URL: http://127.0.0.1:5000
echo ========================================================
python app.py
pause
