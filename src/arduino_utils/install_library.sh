#!/bin/bash

# Function to display usage information
usage() {
  echo "Usage: $0 <source_directory> <destination_directory>"
  exit 1
}

# Check if the correct number of arguments are provided
if [ "$#" -ne 1 ]; then
  usage
fi

SOURCE_DIR="$1"
DEST_DIR="/home/$USER/Arduino/libraries/"

# Check if source directory exists and is a directory
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: Source directory '$SOURCE_DIR' does not exist or is not a directory."
  exit 1
fi

# Check if source directory is non-empty
if [ -z "$(ls -A "$SOURCE_DIR")" ]; then
  echo "Error: Source directory '$SOURCE_DIR' is empty."
  exit 1
fi

# Check if destination directory exists and is a directory
if [ ! -d "$DEST_DIR" ]; then
  echo "Error: Destination directory '$DEST_DIR' does not exist or is not a directory."
  exit 1
fi

# Copy each subdirectory from source to destination
for SUBDIR in "$SOURCE_DIR"/*/; do
  if [ -d "$SUBDIR" ]; then
    cp -r "$SUBDIR" "$DEST_DIR"
    echo "Copied $SUBDIR to $DEST_DIR"
  fi
done

echo "All subdirectories have been copied successfully."
