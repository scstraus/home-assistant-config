class MercuryWeatherCard extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (!this.content) {
      this.innerHTML = `<ha-card><div id="container"></div></ha-card>`;
      this.content = this.querySelector("#container");
      
      this.content.addEventListener('click', (e) => {
        const target = e.target.closest('[data-entity]');
        if (target) {
          this._handleMoreInfo(target.getAttribute('data-entity'));
        }
      });

      this.attachStyles();
    }
    this.render();
  }

  _handleMoreInfo(entityId) {
    this.dispatchEvent(new CustomEvent('hass-more-info', {
      detail: { entityId }, bubbles: true, composed: true,
    }));
  }

  setConfig(config) {
    if (!config.weather_entity) throw new Error("Please define a weather_entity");
    if (!config.overview_entities || config.overview_entities.length !== 4) {
      throw new Error("Please define exactly 4 overview_entities");
    }
    
    this.config = {
      wind_unit: 'kph',
      min_gauge_spacing: 10,
      overview_font_size: '1.25em',
      padding_size: '16px',
      gap_size: '24px',
      // Optional: sun_entity for day/night icon detection (e.g. sun.sun)
      // Optional: icon_path to override the default /hacsfiles/mercury-weather-card path
      ...config,
      current_weather: {
        temp_font_size: '7.5em',
        description_vertical_offset: '0px',
        ...(config.current_weather || {})
      },
      temperature_gauges: {
        min_temp: -20,
        max_temp: 45,
        gauge_height: 180,
        forecast_icon_color: 'var(--primary-text-color)',
        time_font_size: '1.15em',
        time_font_bold: true,
        ...(config.temperature_gauges || {})
      },
      precipitation_gauges: {
        gauge_height: 48,
        font_size: '1em',
        ...(config.precipitation_gauges || {})
      }
    };

    this.colorRanges = [
      { from: -30, to: -17, color: 'rgb(242,249,255)' }, { from: -17, to: -15.5, color: 'rgb(228,242,254)' },
      { from: -15.5, to: -14.5, color: 'rgb(215,236,254)' }, { from: -14.5, to: -13.5, color: 'rgb(201,229,253)' },
      { from: -13.5, to: -12, color: 'rgb(187,223,253)' }, { from: -12, to: -11, color: 'rgb(173,216,252)' },
      { from: -11, to: -10, color: 'rgb(159,210,252)' }, { from: -10, to: -9, color: 'rgb(145,203,251)' },
      { from: -9, to: -8, color: 'rgb(131,197,250)' }, { from: -8, to: -6.5, color: 'rgb(117,190,249)' },
      { from: -6.5, to: -5.5, color: 'rgb(103,184,248)' }, { from: -5.5, to: -4.5, color: 'rgb(89,177,247)' },
      { from: -4.5, to: -3.5, color: 'rgb(75,171,246)' }, { from: -3.5, to: -2, color: 'rgb(61,164,245)' },
      { from: -2, to: -1, color: 'rgb(47,157,244)' }, { from: -1, to: 0, color: 'rgb(33,150,243)' },
      { from: 0, to: 1, color: 'rgb(44,153,234)' }, { from: 1, to: 2, color: 'rgb(55,157,224)' },
      { from: 2, to: 3.5, color: 'rgb(66,160,215)' }, { from: 3.5, to: 4.5, color: 'rgb(77,164,205)' },
      { from: 4.5, to: 5.5, color: 'rgb(88,167,196)' }, { from: 5.5, to: 6.5, color: 'rgb(99,171,186)' },
      { from: 6.5, to: 8, color: 'rgb(110,174,177)' }, { from: 8, to: 9, color: 'rgb(121,178,168)' },
      { from: 9, to: 10, color: 'rgb(132,181,159)' }, { from: 10, to: 11, color: 'rgb(143,185,150)' },
      { from: 11, to: 12, color: 'rgb(154,188,141)' }, { from: 12, to: 13, color: 'rgb(165,192,132)' },
      { from: 13, to: 14.5, color: 'rgb(176,195,123)' }, { from: 14.5, to: 15.5, color: 'rgb(187,199,114)' },
      { from: 15.5, to: 16.5, color: 'rgb(198,202,105)' }, { from: 16.5, to: 18, color: 'rgb(209,205,96)' },
      { from: 18, to: 19, color: 'rgb(220,208,87)' }, { from: 19, to: 20, color: 'rgb(231,211,78)' },
      { from: 20, to: 21, color: 'rgb(242,214,69)' }, { from: 21, to: 22, color: 'rgb(253,217,60)' },
      { from: 22, to: 23.5, color: 'rgb(247,206,58)' }, { from: 23.5, to: 24.5, color: 'rgb(240,194,55)' },
      { from: 24.5, to: 25.5, color: 'rgb(234,183,53)' }, { from: 25.5, to: 26.5, color: 'rgb(227,171,50)' },
      { from: 26.5, to: 28, color: 'rgb(221,160,48)' }, { from: 28, to: 29, color: 'rgb(214,148,45)' },
      { from: 29, to: 30, color: 'rgb(208,137,43)' }, { from: 30, to: 31, color: 'rgb(201,125,40)' },
      { from: 31, to: 32, color: 'rgb(195,114,38)' }, { from: 32, to: 33.5, color: 'rgb(188,102,35)' },
      { from: 33.5, to: 34.5, color: 'rgb(182,91,33)' }, { from: 34.5, to: 35.5, color: 'rgb(175,79,30)' },
      { from: 35.5, to: 36.5, color: 'rgb(169,68,28)' }, { from: 36.5, to: 38, color: 'rgb(162,56,25)' },
      { from: 38, to: 39, color: 'rgb(155,45,23)' }, { from: 39, to: 40, color: 'rgb(148,33,20)' },
      { from: 40, to: 41, color: 'rgb(141,22,18)' }, { from: 41, to: 42, color: 'rgb(134,11,15)' },
      { from: 42, to: 49, color: 'rgb(127,0,12)' }
    ];
  }

  getTempColor(temp) {
    const range = this.colorRanges.find(r => temp >= r.from && temp < r.to);
    return range ? range.color : (temp >= 49 ? 'rgb(127,0,12)' : 'rgb(242,249,255)');
  }

  convertWind(value, currentUnit, targetUnitKey) {
    const val = parseFloat(value);
    if (isNaN(val)) return value;
    let ms;
    const unit = currentUnit.toLowerCase();
    if (unit.includes('km/h') || unit === 'kph') ms = val / 3.6;
    else if (unit.includes('mph')) ms = val / 2.23694;
    else if (unit.includes('ft/s') || unit === 'fps') ms = val / 3.28084;
    else if (unit.includes('kn') || unit.includes('knot')) ms = val / 1.94384;
    else if (unit.includes('m/s') || unit === 'ms') ms = val;
    else return val; 
    switch (targetUnitKey) {
      case 'kph': return ms * 3.6; case 'mph': return ms * 2.23694;
      case 'fps': return ms * 3.28084; case 'kn':  return ms * 1.94384;
      case 'ms':  return ms; default: return val;
    }
  }

  getWindDisplayLabel(unitKey) {
    const labels = { 'kph': 'km/h', 'mph': 'mph', 'ms': 'm/s', 'fps': 'ft/s', 'kn': 'knots' };
    return labels[unitKey] || unitKey;
  }

  getWeatherIcon(state) {
    const iconMap = {
      'clear-night': 'mdi:weather-night', 'cloudy': 'mdi:weather-cloudy',
      'fog': 'mdi:weather-fog', 'hail': 'mdi:weather-hail',
      'lightning': 'mdi:weather-lightning', 'lightning-rainy': 'mdi:weather-lightning-rainy',
      'partlycloudy': 'mdi:weather-partly-cloudy', 'pouring': 'mdi:weather-pouring',
      'rainy': 'mdi:weather-rainy', 'snowy': 'mdi:weather-snowy',
      'sunny': 'mdi:weather-sunny', 'windy': 'mdi:weather-windy'
    };
    return iconMap[state] || 'mdi:weather-cloudy';
  }

  // Returns true if it's currently daytime, using sun.sun entity if available,
  // otherwise falling back to checking the HA weather state itself.
  _isDaytime() {
    // Prefer explicit sun_entity config
    const sunEntityId = this.config.sun_entity || 'sun.sun';
    const sunState = this._hass.states[sunEntityId];
    if (sunState) {
      return sunState.state === 'above_horizon';
    }
    // Fallback: use current weather state - clear-night implies night
    const weatherState = this._hass.states[this.config.weather_entity];
    if (weatherState && weatherState.state === 'clear-night') return false;
    // Last resort: use local time (6am–8pm = day)
    const hour = new Date().getHours();
    return hour >= 6 && hour < 20;
  }

  // Maps a HA weather condition + day/night to a platinum-weather-card animated SVG filename.
  // Icon list uses:
  //   a-<name>-day.svg   — animated, daytime variant
  //   a-<name>-night.svg — animated, nighttime variant
  //   a-<name>.svg       — animated, no day/night distinction
  _svgFilename(condition, isDay) {
    const dn = isDay ? 'day' : 'night';
    const map = {
      // HA state          animated filename (day/night aware where available)
      'sunny':             `a-clear-day.svg`,
      'clear-night':       `a-clear-night.svg`,
      'partlycloudy':      `a-cloudy-3-${dn}.svg`,
      'cloudy':            `a-cloudy.svg`,
      'fog':               `a-fog-${dn}.svg`,
      'hail':              `a-hail.svg`,
      'lightning':         `a-isolated-thunderstorms-${dn}.svg`,
      'lightning-rainy':   `a-scattered-thunderstorms-${dn}.svg`,
      'pouring':           `a-rainy-3-${dn}.svg`,
      'rainy':             `a-rainy-3-${dn}.svg`,
      'snowy':             `a-snowy-3-${dn}.svg`,
      'snowy-rainy':       `a-rain-and-snow-mix.svg`,
      'windy':             `a-wind.svg`,
      'windy-variant':     `a-wind.svg`,
      'exceptional':       `a-unknown.svg`,
    };
    return map[condition] || `a-cloudy.svg`;
  }

  // Returns the base URL where SVGs are served.
  // /hacsfiles/<card-name>/ is the correct browser URL for files stored at
  // /config/www/community/<card-name>/ (i.e. /www/community/<card-name>/).
  // An explicit icon_path in config always wins.
  _iconBase() {
    if (this.config && this.config.icon_path) {
      return this.config.icon_path.replace(/\/$/, '');
    }
    return '/hacsfiles/mercury-weather-card';
  }

  // Builds an <img> that chains through fallback URLs on 404 using onerror.
  _svgImgHtml(condition, isDay, cssClass) {
    const filename = this._svgFilename(condition, isDay);
    const base = this._iconBase();

    // Build fallback list:
    // 1. Primary: correct HACS path (or user-configured path)
    // 2. Static variant (s- prefix) as first fallback in case animated not present
    // 3. Generic (no day/night) animated fallback
    // 4. Static generic fallback
    const staticFilename = filename.replace(/^a-/, 's-');
    const genericAnimated = filename.replace(/-day\.svg$/, '.svg').replace(/-night\.svg$/, '.svg');
    const genericStatic = staticFilename.replace(/-day\.svg$/, '.svg').replace(/-night\.svg$/, '.svg');

    const candidates = [...new Set([
      `${base}/${filename}`,
      `${base}/${staticFilename}`,
      `${base}/${genericAnimated}`,
      `${base}/${genericStatic}`,
    ])];

    const [primary, ...rest] = candidates;
    const fallbacksJson = JSON.stringify(rest).replace(/'/g, '&#39;');
    return `<img class="${cssClass}" src="${primary}" data-svg-fallbacks='${fallbacksJson}' alt="${condition}"
      onerror="var f=JSON.parse(this.dataset.svgFallbacks||'[]');if(f.length){this.src=f.shift();this.dataset.svgFallbacks=JSON.stringify(f);}else{this.style.display='none';}">`;
  }

  getStateLabel(state) {
    const labels = {
      'clear-night':     'Clear night',
      'cloudy':          'Cloudy',
      'fog':             'Foggy',
      'hail':            'Hail',
      'lightning':       'Lightning',
      'lightning-rainy': 'Lightning',
      'partlycloudy':    'Partly cloudy',
      'pouring':         'Pouring rain',
      'rainy':           'Rainy',
      'snowy':           'Snowy',
      'snowy-rainy':     'Snow and rain',
      'sunny':           'Sunny',
      'windy':           'Windy',
      'windy-variant':   'Windy',
      'exceptional':     'Exceptional',
    };
    return labels[state] || state.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  }

  formatTime(dateStr) {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;
    let hours = date.getHours();
    const ampm = hours >= 12 ? 'p' : 'a';
    hours = hours % 12 || 12; 
    return hours + ampm;
  }

  render() {
    const stateObj = this._hass.states[this.config.weather_entity];
    if (!stateObj || !stateObj.attributes.forecast) return;
    const forecast = stateObj.attributes.forecast;

    this.content.style.gap = this.config.gap_size;
    this.querySelector('ha-card').style.padding = this.config.padding_size;

    // ── Current weather overview (icon + temp + state label) ──────────────────
    const currentState = stateObj.state;
    const currentTemp = stateObj.attributes.temperature;
    const tempUnit = stateObj.attributes.temperature_unit ||
      (this._hass.config?.unit_system?.temperature) || '°C';
    const stateLabel = this.getStateLabel(currentState);
    const isDay = this._isDaytime();
    const currentOverviewHtml = `
      <div class="current-overview" data-entity="${this.config.weather_entity}">
        <div class="current-top" style="margin-bottom: calc(-60px + ${this.config.current_weather.description_vertical_offset});">
          ${this._svgImgHtml(currentState, isDay, 'current-icon')}
          <div class="current-temp">
            <span class="current-temp-number" style="font-size: ${this.config.current_weather.temp_font_size};">${currentTemp !== undefined ? Math.round(currentTemp) : '--'}</span>
            <span class="current-temp-unit">${tempUnit}</span>
          </div>
        </div>
        <div class="current-state">${stateLabel}</div>
      </div>`;

    // ── Overview entities row ─────────────────────────────────────────────────
    let topHtml = `<div class="top-row" style="font-size: ${this.config.overview_font_size};">`;
    this.config.overview_entities.forEach((s) => {
      const sensorState = this._hass.states[s.entity];
      let value = sensorState ? sensorState.state : 'N/A';
      let unit = sensorState?.attributes.unit_of_measurement || '';
      if (s.label.toLowerCase().includes('humidity') && !isNaN(parseFloat(value))) {
        value = Math.round(parseFloat(value) / 5) * 5;
      }
      const windUnits = ['km/h', 'mph', 'm/s', 'ft/s', 'knots', 'kph', 'fps', 'ms', 'kn'];
      if (windUnits.some(u => unit.toLowerCase().includes(u))) {
        value = this.convertWind(value, unit, this.config.wind_unit);
        unit = this.getWindDisplayLabel(this.config.wind_unit);
      }
      const isTime = value.toString().includes(':') || (!isNaN(Date.parse(value)) && isNaN(value));
      if (!isTime && !isNaN(parseFloat(value))) {
        value = parseFloat(value).toFixed(s.decimals !== undefined ? s.decimals : 0);
      } else if (isTime && value.includes('T')) {
        const d = new Date(value);
        value = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
      }
      topHtml += `<div class="top-item" data-entity="${s.entity}"><div class="label">${s.label}</div><div class="value">${value}<span class="unit">${unit}</span></div></div>`;
    });
    topHtml += `</div>`;

    // ── Smart precipitation display check ─────────────────────────────────────
    let showPrecipRow = false;
    for (let i = 0; i < 18 && i < forecast.length; i++) {
      const prob = forecast[i].precipitation_probability || 0;
      const amount = forecast[i].precipitation || 0;
      if (prob > 30 || amount > 0.05) {
        showPrecipRow = true;
        break;
      }
    }

    const min = this.config.temperature_gauges.min_temp;
    const max = this.config.temperature_gauges.max_temp;
    const tempHeight = this.config.temperature_gauges.gauge_height;
    const iconColor = this.config.temperature_gauges.forecast_icon_color;
    const timeFontSize = this.config.temperature_gauges.time_font_size;
    const timeFontBold = this.config.temperature_gauges.time_font_bold ? 'bold' : 'normal';
    const precipHeight = this.config.precipitation_gauges.gauge_height;
    const precipFontSize = this.config.precipitation_gauges.font_size;
    const gaugeGap = this.config.min_gauge_spacing;

    // ── Temperature gauges ────────────────────────────────────────────────────
    let tempGaugesHtml = `<div class="gauges-container temp-container" style="height: ${tempHeight}px; gap: ${gaugeGap}px;" data-entity="${this.config.weather_entity}">`;
    for (let i = 0; i < 9; i++) {
      const f1 = forecast[i * 2], f2 = forecast[i * 2 + 1];
      if (!f1 || !f2) break;
      const avgTemp = (f1.temperature + f2.temperature) / 2;
      const heightPct = ((Math.max(min, Math.min(max, avgTemp)) - min) / (max - min)) * 100;

      tempGaugesHtml += `
        <div class="gauge-column">
          <div class="temp-text">${Math.round(avgTemp)}°</div>
          <div class="gauge-track temp-track">
            <div class="gauge-fill temp-fill" style="height: ${heightPct}%; background-color: ${this.getTempColor(avgTemp)};">
              <ha-icon icon="${this.getWeatherIcon(f1.condition)}" class="weather-icon" 
                       style="color: ${iconColor}; --mdc-icon-color: ${iconColor};">
              </ha-icon>
            </div>
          </div>
          <div class="time-text" style="font-size: ${timeFontSize}; font-weight: ${timeFontBold};">${this.formatTime(f1.datetime)}</div>
        </div>`;
    }
    tempGaugesHtml += `</div>`;

    // ── Precipitation gauges ──────────────────────────────────────────────────
    let precipGaugesHtml = '';
    if (showPrecipRow) {
        precipGaugesHtml = `<div class="gauges-container precip-container" style="height: ${precipHeight + 30}px; gap: ${gaugeGap}px;" data-entity="${this.config.weather_entity}">`;
        for (let i = 0; i < 9; i++) {
            const f1 = forecast[i * 2], f2 = forecast[i * 2 + 1];
            if (!f1 || !f2) break;
            const totalPrecip = (f1.precipitation || 0) + (f2.precipitation || 0);
            const maxProb = Math.max((f1.precipitation_probability || 0), (f2.precipitation_probability || 0));
            const displayProb = Math.round(maxProb / 5) * 5;
            const precipHeightPct = Math.min((totalPrecip / 10) * 100, 100);
            precipGaugesHtml += `
              <div class="gauge-column">
                   <div class="gauge-track precip-track" style="height: ${precipHeight}px;">
                       <div class="gauge-fill precip-fill" style="height: ${precipHeightPct}%;"></div>
                   </div>
                   <div class="precip-text" style="font-size: ${precipFontSize};">${displayProb}%</div>
              </div>
            `;
        }
        precipGaugesHtml += `</div>`;
    }

    this.content.innerHTML = currentOverviewHtml + topHtml + tempGaugesHtml + precipGaugesHtml;
  }

  attachStyles() {
    const style = document.createElement('style');
    style.textContent = `
      ha-card { color: #7b8691; transition: padding 0.3s ease; }
      #container { display: flex; flex-direction: column; transition: gap 0.3s ease; }
      .current-overview { cursor: pointer; }
      .current-top { display: flex; justify-content: space-between; align-items: flex-start; }
      .current-icon { width: 160px; height: 160px; object-fit: contain; position: relative; z-index: 1; }
      .current-temp { color: var(--primary-text-color); line-height: 1; display: block; text-align: right; position: relative; }
      .current-temp-number { font-weight: 200; line-height: 0.85; display: block; letter-spacing: -3px; padding-right: calc(1.6rem + 10px); margin-top: 1.2rem; }
      .current-temp-unit { font-size: 1.8em; font-weight: 300; letter-spacing: 0; line-height: 1; position: absolute; top: 1.2rem; right: 0; }
      .current-state { text-align: center; font-size: 1.8em; font-weight: 400; color: var(--primary-text-color); padding: 8px 0 8px 0; position: relative; z-index: 0; }
      .top-row { display: flex; justify-content: space-between; text-align: center; }
      .top-item { cursor: pointer; flex: 1; }
      .top-item .label { font-size: 0.9em; margin-bottom: 4px; }
      .top-item .value { color: var(--primary-text-color); font-weight: 500; }
      .top-item .unit { font-size: 0.8em; opacity: 0.8; }
      .gauges-container { display: flex; justify-content: space-between; width: 100%; cursor: pointer; }
      .gauge-column { display: flex; flex-direction: column; align-items: center; flex: 1; min-width: 0; height: 100%; }
      .gauge-track { position: relative; width: 100%; max-width: 38px; background-color: rgba(200, 200, 200, 0.15); overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; }
      .gauge-fill { width: 100%; position: relative; transition: height 0.5s ease; }
      .temp-container { align-items: flex-end; }
      .temp-track { flex-grow: 1; border-radius: 20px; }
      .temp-fill { border-top: 1px solid rgba(255,255,255,0.1); }
      .temp-text { font-size: 1em; margin-bottom: 5px; height: 18px; color: #7b8691; }
      .time-text { margin-top: 8px; color: #bdc3c7; }
      .weather-icon { position: absolute; bottom: 2px; left: 0; width: 100%; --mdc-icon-size: 100%; display: block; }
      .precip-container { align-items: flex-start; margin-top: -10px; }
      .precip-track { border-radius: 20px; flex-shrink: 0; } 
      .precip-fill { background-color: #42a5f5; border-radius: 0 0 20px 20px; }
      .precip-text { margin-top: 6px; height: 18px; color: #7b8691; }
    `;
    this.appendChild(style);
  }
}
customElements.define('mercury-weather-card', MercuryWeatherCard);
