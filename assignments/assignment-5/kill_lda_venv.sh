#!/usr/bin/env bash

VENVNAME=lda_venv
jupyter kernelspec uninstall $VENVNAME
rm -r $VENVNAME