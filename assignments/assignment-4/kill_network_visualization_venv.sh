#!/usr/bin/env bash

VENVNAME=network_visualization_venv
jupyter kernelspec uninstall $VENVNAME
rm -r $VENVNAME