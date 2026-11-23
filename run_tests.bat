@echo off
title CareerScan - Test Suite
cd /d "%~dp0"
echo Running CareerScan Automated Test Suite...
python test_app.py
pause
