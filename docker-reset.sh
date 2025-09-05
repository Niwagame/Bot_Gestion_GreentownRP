#!/bin/bash
# ==========================================================
# Script : docker-reset.sh
# Objet  : Rebuild + relance des services Docker Compose
# Options:
#   -n, --no-cache      : build sans cache
#   -r, --recreate      : force la recréation des conteneurs
#   -s, --service NAME  : rebuild/relance un service précis
#   -p, --pull          : repuller les images
#   -l, --logs          : affiche les logs après le up (-f)
#   -D, --reset-db      : RÉINITIALISE la DB (compose down -v) → réimporte ./db/init/*.sql
#   -h, --help          : aide
# ==========================================================

set -euo pipefail

GREEN="\e[32m"; RED="\e[31m"; YELLOW="\e[33m"; BLUE="\e[34m"; RESET="\e[0m"

# Détection de la bonne commande compose
if command -v docker &>/dev/null && docker compose version &>/dev/null; then
  COMPOSE_CMD="docker compose"
elif command -v docker-compose &>/dev/null; then
  COMPOSE_CMD="docker-compose"
else
  echo -e "${RED}❌ Docker Compose introuvable.${RESET}"
  exit 1
fi

NO_CACHE=0
RECREATE=0
SERVICE=""
PULL=0
FOLLOW_LOGS=0
RESET_DB=0

usage() {
  sed -n '2,35p' "$0" | sed 's/^# \{0,1\}//'
}

# Parse options
while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--no-cache)   NO_CACHE=1; shift ;;
    -r|--recreate)   RECREATE=1; shift ;;
    -s|--service)    SERVICE="${2:-}"; shift 2 ;;
    -p|--pull)       PULL=1; shift ;;
    -l|--logs)       FOLLOW_LOGS=1; shift ;;
    -D|--reset-db)   RESET_DB=1; shift ;;
    -h|--help)       usage; exit 0 ;;
    *) echo -e "${YELLOW}Option inconnue: $1${RESET}"; usage; exit 1 ;;
  esac
done

# Si on reset DB: arrêter et PURGER les volumes du projet
if [[ $RESET_DB -eq 1 ]]; then
  echo -e "${RED}⚠ Réinitialisation de la base : arrêt des conteneurs + suppression des volumes du projet${RESET}"
  # --remove-orphans pour nettoyer les anciens services
  $COMPOSE_CMD down --volumes --remove-orphans || true
  echo -e "${GREEN}✅ Volumes supprimés. L’import des fichiers ./db/init/*.sql se fera au prochain démarrage.${RESET}"
else
  # Sinon, juste down "propre" sans toucher aux volumes, pour éviter volume in use au rebuild
  $COMPOSE_CMD down --remove-orphans || true
fi

# Options de build & up
BUILD_FLAGS=()
UP_FLAGS=(-d --build)

[[ $NO_CACHE -eq 1 ]] && BUILD_FLAGS+=(--no-cache)
[[ $RECREATE -eq 1 ]] && UP_FLAGS+=(--force-recreate)
[[ $PULL -eq 1 ]] && BUILD_FLAGS+=(--pull always)

echo -e "${BLUE}🔹 Rebuild des images${RESET}"
if [[ -n "$SERVICE" ]]; then
  $COMPOSE_CMD build "${BUILD_FLAGS[@]}" "$SERVICE"
else
  $COMPOSE_CMD build "${BUILD_FLAGS[@]}"
fi

echo -e "${BLUE}🔹 Relance des conteneurs${RESET}"
if [[ -n "$SERVICE" ]]; then
  $COMPOSE_CMD up "${UP_FLAGS[@]}" "$SERVICE"
else
  $COMPOSE_CMD up "${UP_FLAGS[@]}"
fi

echo -e "${GREEN}✅ Rebuild & relance terminés.${RESET}"
echo -e "${YELLOW}Astuce:${RESET} ${COMPOSE_CMD} ps"

if [[ $FOLLOW_LOGS -eq 1 ]]; then
  echo -e "${BLUE}🔹 Logs (Ctrl+C pour quitter)${RESET}"
  if [[ -n "$SERVICE" ]]; then
    $COMPOSE_CMD logs -f "$SERVICE"
  else
    $COMPOSE_CMD logs -f
  fi
fi
