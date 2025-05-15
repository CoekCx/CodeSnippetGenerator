@echo off
title Code Snippet Generator

set "BAT_DIR=%~dp0"

wt -w 0 --maximized cmd /c "CD /D \"%BAT_DIR%src\" && py main.py"
