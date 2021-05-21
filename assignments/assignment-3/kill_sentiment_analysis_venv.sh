#!/usr/bin/env bash

VENVNAME=sentiment_analysis_venv
jupyter kernelspec uninstall $VENVNAME
rm -r $VENVNAME