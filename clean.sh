#!/bin/bash

# Clean build and dist directories
if [ -d "build" ]; then
    echo "Removing build directory..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "Removing dist directory..."
    rm -rf dist
fi

# Build the app using py2app
echo "Building the app..."
python setup.py py2app