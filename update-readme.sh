#!/bin/bash

# Get current date and time in UTC
CURRENT_DATE=$(date -u +"%Y-%m-%d")
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
USERNAME="LoveDoLove"

# Create README from template
cp README_TEMPLATE.md README.md

# Update placeholders
sed -i "s/{CURRENT_DATE}/$CURRENT_DATE/g" README.md
sed -i "s/{TIMESTAMP}/$TIMESTAMP/g" README.md
sed -i "s/{USERNAME}/$USERNAME/g" README.md