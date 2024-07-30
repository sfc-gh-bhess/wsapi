#!/bin/bash

# Prompt user for input
read -p "What is the image repository URL (SHOW IMAGE REPOSITORIES IN SCHEMA)? " repository_url
read -p "What warehouse can the API use? " warehouse
read -p "What compute pool will be used? " compute_pool

# Paths to the files
makefile="./Makefile"
wsapi_yaml="./wsapi.yaml"

# Copy files
cp $makefile.template $makefile
cp $wsapi_yaml.template $wsapi_yaml

# Replace placeholders in Makefile file using | as delimiter
sed -i "" "s|<<REPOSITORY>>|$repository_url|g" $makefile
sed -i "" "s|<<WAREHOUSE>>|$warehouse|g" $makefile
sed -i "" "s|<<COMPUTE_POOL>>|$compute_pool|g" $makefile

# Replace placeholders in SPCS YAML file using | as delimiter
sed -i "" "s|<<REPOSITORY>>|$repository_url|g" $wsapi_yaml

echo "Placeholder values have been replaced!"
echo "Run 'make help' to view the targets."
