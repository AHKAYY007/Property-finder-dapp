#!/bin/bash

# Create necessary directories
mkdir -p app/components

# Install dependencies
npm install

# Create global CSS file
echo "@tailwind base;
@tailwind components;
@tailwind utilities;" > app/globals.css 