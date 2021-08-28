#!/bin/bash

set -euo pipefail

read -p "Migration Name:" migration_name

flask db migrate -m "$migration_name"
