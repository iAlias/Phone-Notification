# Phone Notifications Logger

**Versione 0.2.0**

Questo *custom component* per **Home Assistant** salva lo storico di tutte
le notifiche Android e include una **Lovelace card** per visualizzarle.

## Installazione via HACS

1. Aggiungi questo repository come *Integrazione* personalizzata in HACS.
2. Installa e riavvia Home Assistant.

## Configurazione sensore

```yaml
sensor:
  - platform: phone_notifications_logger
    sensor_entity_id: sensor.samsung_s21_active_notification_count_2
    name: "Notifiche Telefono"
    max_history: 1000
```

## Card Lovelace

Dopo l'installazione HACS copierà il file
`/hacsfiles/phone_notifications_logger/phone_notifications_card.js`.

Aggiungi una card manuale:

```yaml
type: custom:phone-notifications-card
entity: sensor.notifiche_telefono
max_items: 10
title: "Storico Notifiche"
```

La card mostrerà le ultime `max_items` notifiche con data/ora, titolo e testo.