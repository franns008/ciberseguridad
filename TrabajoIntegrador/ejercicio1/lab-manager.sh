#!/bin/bash

# Script de gestión del laboratorio de ciberseguridad
# Uso: ./lab-manager.sh [start|stop|restart|audit|connect|clean]

case "$1" in
    start)
        echo "🚀 Iniciando laboratorio de ciberseguridad..."
        docker compose up --build -d
        echo "✅ Laboratorio iniciado"
        echo "📝 Usa './lab-manager.sh connect' para acceder al sistema"
        ;;
    
    stop)
        echo "🛑 Deteniendo laboratorio..."
        docker compose down
        echo "✅ Laboratorio detenido"
        ;;
    
    restart)
        echo "🔄 Reiniciando laboratorio..."
        docker compose down
        docker compose up --build -d
        echo "✅ Laboratorio reiniciado"
        ;;
    
    audit)
        echo "🔍 Ejecutando auditoría con Lynis..."
        docker exec -it vulnerable_os_target lynis audit system
        echo ""
        echo "📊 Para ver el reporte completo:"
        echo "docker exec -it vulnerable_os_target cat /var/log/lynis-report.dat"
        ;;
    
    quick-audit)
        echo "⚡ Ejecutando auditoría rápida con Lynis..."
        docker exec -it vulnerable_os_target lynis audit system --quick
        ;;
    
    warnings)
        echo "⚠️  Mostrando solo warnings críticos..."
        docker exec vulnerable_os_target bash -c "lynis audit system --quick --warnings-only 2>/dev/null | grep 'WARNING\\|\\[ WARNING \\]'"
        ;;
    
    report)
        echo "📄 Copiando reporte de Lynis..."
        mkdir -p ./reports
        docker exec vulnerable_os_target cp /var/log/lynis-report.dat /var/log/lynis-reports/ 2>/dev/null || true
        docker exec vulnerable_os_target cp /var/log/lynis.log /var/log/lynis-reports/ 2>/dev/null || true
        echo "✅ Reportes guardados en ./reports/"
        ;;
    
    connect)
        echo "🔗 Conectando al sistema vulnerable..."
        docker exec -it vulnerable_os_target /bin/bash
        ;;
    
    clean)
        echo "🧹 Limpiando laboratorio..."
        # Detener y eliminar contenedor específico si existe
        if docker ps -a --format '{{.Names}}' | grep -qw vulnerable_os_target; then
            echo "🔽 Deteniendo y eliminando contenedor 'vulnerable_os_target'..."
            docker rm -f vulnerable_os_target 2>/dev/null || true
        fi

        # Traer abajo los servicios de compose y eliminar volúmenes y órfanos
        docker compose down -v --remove-orphans 2>/dev/null || true

        # Eliminar cualquier contenedor creado a partir de la imagen tpi-vulnerable_os
        image_containers=$(docker ps -a --filter ancestor=tpi-vulnerable_os --format '{{.ID}}') || true
        if [ -n "${image_containers}" ]; then
            echo "🗑️ Eliminando contenedores creados desde la imagen 'tpi-vulnerable_os'..."
            docker rm -f ${image_containers} 2>/dev/null || true
        fi

        # Forzar eliminación de la imagen si existe
        if docker images -q tpi-vulnerable_os >/dev/null 2>&1; then
            echo "🧧 Eliminando imagen 'tpi-vulnerable_os'..."
            docker image rm -f tpi-vulnerable_os 2>/dev/null || true
        fi

        # Eliminar la red por nombre si existe (comúnmente tpi_default)
        if docker network ls --format '{{.Name}}' | grep -qw tpi_default; then
            echo "🌐 Eliminando red 'tpi_default'..."
            docker network rm tpi_default 2>/dev/null || true
        fi

        echo "✅ Limpieza completa del laboratorio"
        ;;
    
    *)
        echo "🎓 Gestor del laboratorio"
        echo ""
        echo "Uso: $0 {start|stop|restart|audit|quick-audit|warnings|report|connect|clean}"
        echo ""
        echo "Comandos disponibles:"
        echo "  start       - Iniciar el laboratorio"
        echo "  stop        - Detener el laboratorio"
        echo "  restart     - Reiniciar el laboratorio"
        echo "  audit       - Ejecutar auditoría completa de Lynis"
        echo "  quick-audit - Ejecutar auditoría rápida de Lynis"
        echo "  warnings    - Mostrar solo warnings críticos"
        echo "  report      - Copiar reportes a carpeta local"
        echo "  connect     - Conectar al sistema vulnerable"
        echo "  clean       - Limpiar completamente el laboratorio"
        echo ""
        echo "Ejemplo: $0 start"
        ;;
esac