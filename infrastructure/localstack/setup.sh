#!/bin/bash

echo "Configurando recursos en LocalStack..."

# Crear bucket S3 para datos
awslocal s3 mb s3://flight-data

# Subir datos al bucket
awslocal s3 cp /opt/code/data/airports.json s3://flight-data/airports.json
awslocal s3 cp /opt/code/data/flights.json s3://flight-data/flights.json

# Crear tabla DynamoDB para caché (opcional)
awslocal dynamodb create-table \
    --table-name FlightCache \
    --key-schema AttributeName=route,KeyType=HASH \
    --attribute-definitions AttributeName=route,AttributeType=S \
    --billing-mode PAY_PER_REQUEST

echo "LocalStack configurado correctamente!"
echo "S3 bucket: flight-data"
echo "DynamoDB table: FlightCache"