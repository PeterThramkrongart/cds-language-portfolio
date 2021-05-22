#!/usr/bin/env bash

VENVNAME=network_analysis_venv
jupyter kernelspec uninstall $VENVNAME
rm -r $VENVNAME