class PhoneNotificationsCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) {
      throw new Error("Devi specificare 'entity'.");
    }
    this.config = {
      title: "Notifiche Telefono",
      max_items: 5,
      ...config,
    };
  }

  getCardSize() {
    return (this.config.max_items || 5) + 1;
  }

  set hass(hass) {
    this._hass = hass;
    if (!this.card) {
      this.card = document.createElement("ha-card");
      this.card.header = this.config.title;
      this.content = document.createElement("div");
      this.content.className = "card-content";
      this.card.appendChild(this.content);
      this.appendChild(this.card);
    }
    this._render();
  }

  _render() {
    const stateObj = this._hass.states[this.config.entity];
    if (!stateObj) {
      this.content.innerHTML = "Entità non trovata";
      return;
    }
    const data = stateObj.attributes.notifications || [];
    const maxItems = parseInt(this.config.max_items, 10) || 5;
    const recent = data.slice(-maxItems).reverse();

    if (recent.length === 0) {
      this.content.innerHTML = "<em>Nessuna notifica</em>";
      return;
    }
    this.content.innerHTML = recent
      .map(n => `
        <div style="margin-bottom:6px;">
          <strong>${this._formatDate(n.timestamp)}</strong><br>
          <b>${n.title || ""}</b><br>
          ${n.text || ""}
        </div>
      `).join("<hr>");
  }

  _formatDate(ts) {
    if (!ts) return "";
    const d = new Date(ts);
    return d.toLocaleString();
  }

  static getStubConfig() {
    return {
      entity: "sensor.notifiche_telefono",
      max_items: 5,
    };
  }
}
customElements.define("phone-notifications-card", PhoneNotificationsCard);