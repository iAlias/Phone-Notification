# Phone Notifications Logger

**Versione 0.1.0**

Questo *custom component* per **Home Assistant** salva lo storico di **tutte le notifiche** che
arrivano sul tuo smartphone Android, integrato tramite l'App Companion.
Lo storico viene conservato in un file JSON nel folder `.storage` di Home Assistant
e resta disponibile anche dopo riavvii o aggiornamenti.

## Installazione

1. Copia la cartella **`custom_components/phone_notifications_logger`**
   (contenuta in questo repository) nella directory `config/custom_components`
   della tua installazione di Home Assistant.
2. Riavvia Home Assistant.

## Configurazione

Aggiungi nel tuo `configuration.yaml`:

```yaml
sensor:
  - platform: phone_notifications_logger
    sensor_entity_id: sensor.samsung_s21_active_notification_count_2
    name: "Notifiche Telefono"
    max_history: 1000   # opzionale, default 1000
```

* `sensor_entity_id` – l'ID del sensore notifiche generato dall'App Companion.
* `name` – nome dell'entità che verrà creata.
* `max_history` – numero massimo di notifiche da mantenere nello storico.

Dopo il riavvio troverai un nuovo **sensore** con:
* **Stato** = titolo (o testo) dell'ultima notifica ricevuta.
* **Attributi**:
  * `history_count` – numero totale di notifiche nello storico.
  * `last_notification` – JSON con timestamp, titolo e testo dell'ultima notifica.

> Lo storico completo è salvato in `.storage/phone_notifications_logger_<sensor>.json`.
> Puoi leggerlo o elaborarlo con automazioni/Script a tuo piacere.

## Come funziona

Il componente:
1. Ascolta gli eventi `state_changed` del sensore Android selezionato.
2. Per ogni nuova notifica legge gli attributi `android.title` e `android.text`.
3. Aggiunge l'evento allo storico persistente (JSON).
4. Aggiorna lo stato dell'entità e relativi attributi.

## Sviluppo

Pull request e suggerimenti sono benvenuti!  
© 2025 – rilasciato sotto licenza MIT.

## Installazione via HACS

1. Vai in **HACS → Integrazioni → Menu (⋮) → Aggiungi repository personalizzato**.
2. Inserisci l'URL del repository GitHub (ad esempio `https://github.com/tuo_utente/phone_notifications_logger`) e seleziona **Integrazione**.
3. Dopo che HACS ha scaricato la lista, clicca su **Installa**.
4. Riavvia Home Assistant.
5. Aggiungi la configurazione YAML mostrata sopra o usa l'interfaccia per creare l'entità.

Da ora in poi, gli aggiornamenti arriveranno automaticamente tramite HACS.
