#!/bin/bash

# R2R SSH Tunnel Manager
# Управление SSH туннелем к R2R API в Google Cloud

INSTANCE="r2r-production"
ZONE="us-central1-a"
LOCAL_PORT="7272"
REMOTE_PORT="7272"

case "$1" in
  start)
    echo "🚀 Открытие SSH туннеля к R2R API..."

    # Проверяем, не запущен ли уже туннель
    if lsof -i :$LOCAL_PORT > /dev/null 2>&1; then
      echo "⚠️  Порт $LOCAL_PORT уже занят. Возможно туннель уже запущен."
      echo "   Используйте '$0 status' для проверки или '$0 stop' для остановки."
      exit 1
    fi

    # Запускаем туннель в фоне
    gcloud compute ssh $INSTANCE --zone=$ZONE -- -L $LOCAL_PORT:localhost:$REMOTE_PORT -N -f

    # Ждем установки туннеля
    sleep 2

    # Проверяем успешность
    if lsof -i :$LOCAL_PORT > /dev/null 2>&1; then
      echo "✅ SSH туннель успешно открыт!"
      echo "   R2R API доступен на: http://localhost:$LOCAL_PORT"
      echo ""
      echo "   Тестовый запрос:"
      echo "   curl http://localhost:7272/v3/health"
    else
      echo "❌ Не удалось открыть туннель"
      exit 1
    fi
    ;;

  stop)
    echo "🛑 Остановка SSH туннеля..."

    # Находим PID процесса ssh с туннелем
    TUNNEL_PID=$(lsof -ti :$LOCAL_PORT)

    if [ -z "$TUNNEL_PID" ]; then
      echo "ℹ️  SSH туннель не запущен"
      exit 0
    fi

    kill $TUNNEL_PID
    sleep 1

    if ! lsof -i :$LOCAL_PORT > /dev/null 2>&1; then
      echo "✅ SSH туннель остановлен"
    else
      echo "⚠️  Не удалось остановить туннель (PID: $TUNNEL_PID)"
      exit 1
    fi
    ;;

  status)
    echo "📊 Статус SSH туннеля:"
    echo ""

    if lsof -i :$LOCAL_PORT > /dev/null 2>&1; then
      TUNNEL_PID=$(lsof -ti :$LOCAL_PORT)
      echo "✅ Туннель запущен (PID: $TUNNEL_PID)"
      echo "   Порт: $LOCAL_PORT"
      echo ""

      # Тестируем подключение
      if curl -s http://localhost:$LOCAL_PORT/v3/health > /dev/null 2>&1; then
        echo "✅ R2R API отвечает"
        curl -s http://localhost:$LOCAL_PORT/v3/health | jq .
      else
        echo "⚠️  Туннель открыт, но R2R API не отвечает"
      fi
    else
      echo "❌ Туннель не запущен"
      echo ""
      echo "   Запустить: $0 start"
    fi
    ;;

  restart)
    echo "🔄 Перезапуск SSH туннеля..."
    $0 stop
    sleep 1
    $0 start
    ;;

  test)
    echo "🧪 Тестирование R2R API через туннель..."
    echo ""

    if ! lsof -i :$LOCAL_PORT > /dev/null 2>&1; then
      echo "❌ SSH туннель не запущен. Запустите сначала: $0 start"
      exit 1
    fi

    echo "1. Health Check..."
    curl -s http://localhost:$LOCAL_PORT/v3/health | jq .
    echo ""

    echo "2. Login test..."
    RESPONSE=$(curl -s -X POST http://localhost:$LOCAL_PORT/v3/users/login \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "username=admin@example.com&password=change_me_immediately")

    ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.results.access_token.token')

    if [ "$ACCESS_TOKEN" != "null" ] && [ -n "$ACCESS_TOKEN" ]; then
      echo "✅ Аутентификация успешна"
      echo "   Token: ${ACCESS_TOKEN:0:50}..."
      echo ""

      echo "3. Collections..."
      curl -s http://localhost:$LOCAL_PORT/v3/collections \
        -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.results[] | {name: .name, docs: .document_count}'
    else
      echo "❌ Ошибка аутентификации"
      echo "$RESPONSE" | jq .
    fi
    ;;

  *)
    echo "R2R SSH Tunnel Manager"
    echo ""
    echo "Использование: $0 {start|stop|status|restart|test}"
    echo ""
    echo "Команды:"
    echo "  start    - Открыть SSH туннель к R2R API"
    echo "  stop     - Остановить SSH туннель"
    echo "  status   - Показать статус туннеля"
    echo "  restart  - Перезапустить туннель"
    echo "  test     - Протестировать подключение к API"
    echo ""
    echo "Примеры:"
    echo "  $0 start          # Открыть туннель"
    echo "  $0 status         # Проверить статус"
    echo "  $0 test           # Протестировать API"
    echo ""
    exit 1
    ;;
esac
