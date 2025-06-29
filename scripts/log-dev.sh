#!/bin/bash

echo "Logs WordPress :"
./scripts/run-wp-dev-logs.sh

echo ""
echo "Logs PrestaShop :"
./scripts/run-pts-dev-logs.sh
