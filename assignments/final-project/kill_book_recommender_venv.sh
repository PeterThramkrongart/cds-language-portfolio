#!/usr/bin/env bash

VENVNAME=book_recommender_venv
jupyter kernelspec uninstall $VENVNAME
rm -r $VENVNAME