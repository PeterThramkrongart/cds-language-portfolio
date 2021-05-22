#!/usr/bin/env bash

VENVNAME=got_venv
jupyter kernelspec uninstall $VENVNAME
rm -r $VENVNAME