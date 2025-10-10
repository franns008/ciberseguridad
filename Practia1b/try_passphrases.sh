#!/usr/bin/env bash

IMG="Totodile.jpg"   # <-- ajustá si el nombre es distinto
OUTDIR="stegh_out"
mkdir -p "$OUTDIR"

# Variantes ampliadas de "muy facil"
passlist=(
  "muy fácil."
  "muy facil"
  "facil"
  "muyfacil"
  "muy fácil"
  "muyfácil"
  "fácil"
  "facíl"
  "muy_facil"
  "muy-facil"
  "MUY FACIL"
  "Muy Facil"
  "muy  facil"      # doble espacio
  "muy    facil"    # varios espacios
  "muyfacíl"        # variante con tilde mal colocada
  "muyfac1l"        # l por 1
  "muyfac1l "       # con espacio al final
  "muyfacil!"       # con signo
  "muyfacil123"
  "muyfacil."
)

# Limpiamos log anterior
: > "$OUTDIR/log.txt"

for pw in "${passlist[@]}"; do
  echo "== Probando: [$pw] ==" | tee -a "$OUTDIR/log.txt"
  # -p pasa la passphrase, -f fuerza sobreescritura de salida si la versión lo soporta
  # redirigimos stdout+stderr al log
  steghide extract -sf "$IMG" -p "$pw" -f >> "$OUTDIR/log.txt" 2>&1
  rc=$?
  if [[ $rc -eq 0 ]]; then
    echo "=> exit ok para [$pw]" | tee -a "$OUTDIR/log.txt"
  else
    echo "=> exit error para [$pw] (rc=$rc)" | tee -a "$OUTDIR/log.txt"
  fi
  echo "" >> "$OUTDIR/log.txt"
done

echo "Hecho. Revisá $OUTDIR/log.txt"
