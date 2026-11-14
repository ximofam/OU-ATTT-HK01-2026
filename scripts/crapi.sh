#!/usr/bin/env bash
set -euo pipefail

SCRIPT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_ROOT="${SCRIPT_ROOT}/.runtime/crapi"
ACTION="${1:-help}"

usage() {
  printf '%s\n' \
    'Usage: bash scripts/crapi.sh {setup|up|down|status|logs|revision}' \
    '  setup     Clone official OWASP/crAPI main into .runtime/crapi (once)' \
    '  up        Start official crAPI Docker Compose with LISTEN_IP=127.0.0.1' \
    '  down      Stop/remove Compose containers and network; keep volumes' \
    '  status    Show running service status' \
    '  logs      Follow Compose logs' \
    '  revision  Show checked-out upstream commit' \
    '  note      Use CRAPI_MINIMAL=1 for optional upstream minimal limits'
}

require_git() {
  command -v git >/dev/null 2>&1 || { echo 'Git is required.' >&2; exit 1; }
}

require_compose() {
  command -v docker >/dev/null 2>&1 || { echo 'Docker is required.' >&2; exit 1; }
  docker compose version >/dev/null 2>&1 || { echo 'Docker Compose V2 is required.' >&2; exit 1; }
}

setup() {
  require_git
  if [[ -d "${UPSTREAM_ROOT}/.git" ]]; then
    echo "crAPI already downloaded at ${UPSTREAM_ROOT}; no update performed."
    return
  fi
  if [[ -e "${UPSTREAM_ROOT}" ]]; then
    echo "Refusing to overwrite existing ${UPSTREAM_ROOT}" >&2
    exit 1
  fi
  mkdir -p -- "${SCRIPT_ROOT}/.runtime"
  git clone --depth 1 --branch main https://github.com/OWASP/crAPI.git "${UPSTREAM_ROOT}"
}

compose() {
  require_compose
  [[ -f "${UPSTREAM_ROOT}/deploy/docker/docker-compose.yml" ]] || {
    echo 'crAPI checkout missing; run: bash scripts/crapi.sh setup' >&2
    exit 1
  }
  local args=(-f docker-compose.yml)
  if [[ "${CRAPI_MINIMAL:-0}" == "1" ]]; then
    if [[ -f "${UPSTREAM_ROOT}/deploy/docker/docker-compose.minimal.yml" ]]; then
      args+=(-f docker-compose.minimal.yml)
    else
      echo 'Minimal Compose override absent on this upstream revision; using default Compose.' >&2
    fi
  fi
  (
    cd -- "${UPSTREAM_ROOT}/deploy/docker"
    LISTEN_IP=127.0.0.1 docker compose "${args[@]}" --compatibility "$@"
  )
}

case "${ACTION}" in
  setup)
    setup
    ;;
  up)
    setup
    compose up -d
    echo 'Browse http://127.0.0.1:8888 after services become healthy.'
    ;;
  down)
    compose down
    ;;
  status)
    compose ps
    ;;
  logs)
    compose logs -f
    ;;
  revision)
    require_git
    [[ -d "${UPSTREAM_ROOT}/.git" ]] || { echo 'Run setup first.' >&2; exit 1; }
    git -C "${UPSTREAM_ROOT}" rev-parse HEAD
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
