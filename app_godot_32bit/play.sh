#!/usr/bin/env bash
# Lanzador de la Aplicación de Bacheo Inteligente 32-Bit (Godot Engine)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=========================================================="
echo "Iniciando Bacheo Inteligente Tijuana (LCDN UNRC)"
echo "Arquitectura: 32-Bit / 64-Bit GLES2 Universal"
echo "=========================================================="
if [ -f "$SCRIPT_DIR/build/Bacheo_Tijuana_PC.x86_64" ]; then
    "$SCRIPT_DIR/build/Bacheo_Tijuana_PC.x86_64" "$@"
elif [ -f "$SCRIPT_DIR/build/Bacheo_Tijuana_PC_32Bit" ]; then
    "$SCRIPT_DIR/build/Bacheo_Tijuana_PC_32Bit" "$@"
else
    /home/triche777/tools/godot3 --path "$SCRIPT_DIR" "$@"
fi
