#!/bin/bash
# pwcheck.sh - Cross-platform password strength checker wrapper

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default Python command
PYTHON_CMD="python3"

# Check if Python3 exists, fallback to python
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${YELLOW}Using 'python' instead of 'python3'${NC}"
fi

# Check if pwcheck.py exists
if [[ ! -f "pwcheck.py" ]]; then
    echo -e "${RED}Error: pwcheck.py not found!${NC}"
    exit 1
fi

usage() {
    echo "Usage: $0 [OPTIONS] [PASSWORD]"
    echo "  -i, --interactive  Interactive mode"
    echo "  -b, --batch FILE   Batch file (one password per line)"
    echo "  -p, --pipe         Read passwords from stdin"
    echo "  -h, --help         Show this help"
}

case "$1" in
    -i|--interactive)
        $PYTHON_CMD pwcheck.py -i
        ;;
    -b|--batch)
        shift
        $PYTHON_CMD pwcheck.py -b "$1"
        ;;
    -p|--pipe)
        $PYTHON_CMD pwcheck.py -b /dev/stdin
        ;;
    -h|--help)
        usage
        ;;
    "")
        $PYTHON_CMD pwcheck.py
        ;;
    *)
        $PYTHON_CMD pwcheck.py "$@"
        ;;
esac