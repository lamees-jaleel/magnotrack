/**
 * MagnoTrack - Industrial IoT Monitoring Dashboard Client
 * Handles real-time polling, Chart.js updates, tab navigation, and pagination.
 */

// State Management
const state = {
  autoRefresh: true,
  refreshIntervalMs: 2500,
  timerId: null,
  isFetching: false,
  hasReceivedInitialData: false,
  historyPage: 0,
  historyLimit: 25,
  historyTotal: 0,
  cumulativeChart: null,
  activityChart: null
};

// DOM Elements
const dom = {
  // Nav & Badges
  connectionPill: document.getElementById('connection-pill'),
  connectionText: document.getElementById('connection-text'),
  statusBanner: document.getElementById('status-banner'),
  bannerIcon: document.getElementById('banner-icon'),
  bannerMessage: document.getElementById('banner-message'),
  refreshBtn: document.getElementById('refresh-btn'),
  autoRefreshCheck: document.getElementById('auto-refresh-check'),
  utcClock: document.getElementById('utc-clock'),

  // KPIs
  totalEvents: document.getElementById('total-events'),
  sensorStateBadge: document.getElementById('sensor-state-badge'),
  sensorStateText: document.getElementById('sensor-state-text'),
  sensorDigitalPin: document.getElementById('sensor-digital-pin'),
  sensorIconBadge: document.getElementById('sensor-icon-badge'),
  eventsLast60s: document.getElementById('events-last-60s'),
  rateBadge: document.getElementById('rate-badge'),
  lastEventTime: document.getElementById('last-event-time'),
  lastEventRelative: document.getElementById('last-event-relative'),
  deviceStatusText: document.getElementById('device-status-text'),
  deviceIdTag: document.getElementById('device-id-tag'),
  deviceUptimeLabel: document.getElementById('device-uptime-label'),

  // Tables
  liveStreamTbody: document.getElementById('live-stream-tbody'),
  fullHistoryTbody: document.getElementById('full-history-tbody'),
  historyLimitSelect: document.getElementById('history-limit-select'),
  historyTotalCount: document.getElementById('history-total-count'),
  pagePrevBtn: document.getElementById('page-prev-btn'),
  pageNextBtn: document.getElementById('page-next-btn'),
  paginationInfo: document.getElementById('pagination-info'),
  exportCsvBtn: document.getElementById('export-csv-btn'),
  refreshHistoryBtn: document.getElementById('refresh-history-btn'),

  // Charts
  chart1Empty: document.getElementById('chart1-empty'),
  chart2Empty: document.getElementById('chart2-empty')
};

// Format milliseconds into HH:MM:SS
function formatUptime(ms) {
  if (ms === null || ms === undefined || isNaN(ms)) return "00:00:00";
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return `${String(hours).padStart(2, '0')}h ${String(minutes).padStart(2, '0')}m ${String(seconds).padStart(2, '0')}s`;
}

// Format ISO date string into readable local & UTC times
function formatTimestamp(isoStr) {
  if (!isoStr) return { local: "Never", utc: "Never", relative: "No detections yet" };
  const d = new Date(isoStr);
  if (isNaN(d.getTime())) return { local: "Invalid Date", utc: "Invalid Date", relative: "" };

  const pad = (n) => String(n).padStart(2, '0');
  const utc = `${d.getUTCFullYear()}-${pad(d.getUTCMonth()+1)}-${pad(d.getUTCDate())} ${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}:${pad(d.getUTCSeconds())}`;
  const local = d.toLocaleTimeString();

  // Compute relative time
  const now = new Date();
  const diffSec = Math.max(0, Math.floor((now.getTime() - d.getTime()) / 1000));
  let relative = "Just now";
  if (diffSec >= 60 && diffSec < 3600) {
    relative = `${Math.floor(diffSec / 60)}m ago`;
  } else if (diffSec >= 3600) {
    relative = `${Math.floor(diffSec / 3600)}h ago`;
  } else if (diffSec > 0) {
    relative = `${diffSec}s ago`;
  }

  return { local, utc, relative };
}

// Tab Switching
function initTabs() {
  const navLinks = document.querySelectorAll('.nav-link[data-tab]');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const tabName = link.getAttribute('data-tab');
      switchToTab(tabName);
    });
  });
}

function switchToTab(tabName) {
  document.querySelectorAll('.nav-link[data-tab]').forEach(el => {
    el.classList.toggle('active', el.getAttribute('data-tab') === tabName);
  });
  document.querySelectorAll('.tab-content').forEach(el => {
    el.classList.toggle('active', el.id === `tab-${tabName}`);
  });

  if (tabName === 'history') {
    fetchHistory();
  }
}

// Initialize Chart.js Instances
function initCharts() {
  const chartFont = {
    family: "'JetBrains Mono', monospace",
    size: 11
  };

  const gridConfig = {
    color: '#1e2d4d',
    drawBorder: false
  };

  // 1. Cumulative Events Line Chart
  const ctx1 = document.getElementById('cumulativeEventsChart').getContext('2d');
  const gradient1 = ctx1.createLinearGradient(0, 0, 0, 260);
  gradient1.addColorStop(0, 'rgba(6, 182, 212, 0.35)');
  gradient1.addColorStop(1, 'rgba(6, 182, 212, 0.0)');

  state.cumulativeChart = new Chart(ctx1, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Total Events',
        data: [],
        borderColor: '#06b6d4',
        borderWidth: 2.5,
        backgroundColor: gradient1,
        fill: true,
        tension: 0.35,
        pointBackgroundColor: '#06b6d4',
        pointBorderColor: '#070a13',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 300 },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0d1527',
          borderColor: '#1e2d4d',
          borderWidth: 1,
          titleFont: chartFont,
          bodyFont: chartFont,
          callbacks: {
            label: (ctx) => ` Cumulative Events: ${ctx.parsed.y}`
          }
        }
      },
      scales: {
        x: {
          grid: gridConfig,
          ticks: { color: '#64748b', font: chartFont, maxTicksLimit: 8 }
        },
        y: {
          grid: gridConfig,
          ticks: { color: '#64748b', font: chartFont, precision: 0 },
          beginAtZero: true
        }
      }
    }
  });

  // 2. Activity Deltas & Magnet Status Bar Chart
  const ctx2 = document.getElementById('activityRateChart').getContext('2d');
  state.activityChart = new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Events in Interval',
          data: [],
          backgroundColor: '#10b981',
          borderRadius: 4,
          maxBarThickness: 24
        },
        {
          label: 'Magnet Detected State',
          data: [],
          type: 'line',
          borderColor: '#f43f5e',
          borderWidth: 2,
          borderDash: [4, 4],
          pointBackgroundColor: '#f43f5e',
          pointRadius: 3,
          yAxisID: 'yFlux'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 300 },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: { color: '#94a3b8', font: chartFont, boxWidth: 12 }
        },
        tooltip: {
          backgroundColor: '#0d1527',
          borderColor: '#1e2d4d',
          borderWidth: 1,
          titleFont: chartFont,
          bodyFont: chartFont
        }
      },
      scales: {
        x: {
          grid: gridConfig,
          ticks: { color: '#64748b', font: chartFont, maxTicksLimit: 8 }
        },
        y: {
          grid: gridConfig,
          ticks: { color: '#64748b', font: chartFont, precision: 0 },
          beginAtZero: true
        },
        yFlux: {
          position: 'right',
          display: false,
          min: 0,
          max: 1.2
        }
      }
    }
  });
}

// Update KPI cards and connection badges
function updateKPIs(stats) {
  // 1. Total Events
  dom.totalEvents.textContent = Number(stats.total_events).toLocaleString();

  // 2. Sensor Status
  if (stats.current_sensor_state) {
    dom.sensorStateBadge.className = 'sensor-state-badge state-active';
    dom.sensorStateText.textContent = 'MAGNET DETECTED';
    dom.sensorDigitalPin.textContent = 'LOW (Triggered)';
    dom.sensorIconBadge.className = 'card-icon-badge amber';
  } else {
    dom.sensorStateBadge.className = 'sensor-state-badge state-idle';
    dom.sensorStateText.textContent = 'NO MAGNET';
    dom.sensorDigitalPin.textContent = 'HIGH (Idle)';
    dom.sensorIconBadge.className = 'card-icon-badge cyan';
  }

  // 3. Events Per Minute
  const epm = stats.events_last_60s;
  dom.eventsLast60s.textContent = epm;
  if (epm === 0) {
    dom.rateBadge.textContent = 'IDLE';
    dom.rateBadge.className = 'badge badge-subtle';
  } else if (epm < 15) {
    dom.rateBadge.textContent = 'ACTIVE';
    dom.rateBadge.className = 'badge badge-emerald';
  } else {
    dom.rateBadge.textContent = 'HIGH RATE';
    dom.rateBadge.className = 'badge badge-rose';
  }

  // 4. Last Event Timestamp
  if (stats.latest_event_timestamp) {
    const formatted = formatTimestamp(stats.latest_event_timestamp);
    dom.lastEventTime.textContent = formatted.local;
    dom.lastEventRelative.textContent = `${formatted.relative} (${formatted.utc} UTC)`;
  } else {
    dom.lastEventTime.textContent = 'Never';
    dom.lastEventRelative.textContent = 'No detections recorded yet';
  }

  // 5. Device Connection & Banner
  dom.deviceIdTag.textContent = stats.device_id || 'magnotrack-01';
  dom.deviceUptimeLabel.textContent = `Uptime: ${formatUptime(stats.uptime_ms)}`;

  if (stats.total_readings_logged === 0) {
    // Waiting for first reading
    dom.connectionPill.className = 'status-pill waiting';
    dom.connectionText.textContent = 'WAITING FOR DATA';
    dom.deviceStatusText.textContent = 'STANDBY';
    dom.deviceStatusText.style.color = '#f59e0b';

    dom.statusBanner.className = 'status-banner banner-warning';
    dom.bannerIcon.textContent = '⏳';
    dom.bannerMessage.textContent = 'Waiting for ESP32 data... Connect your ESP32 to Wi-Fi to start streaming telemetry.';
  } else if (stats.is_online) {
    // Device is actively transmitting
    dom.connectionPill.className = 'status-pill online';
    dom.connectionText.textContent = 'ESP32 ONLINE';
    dom.deviceStatusText.textContent = 'ONLINE';
    dom.deviceStatusText.style.color = '#10b981';

    dom.statusBanner.className = 'status-banner hidden';
  } else {
    // Device was seen before, but timed out (>30s)
    dom.connectionPill.className = 'status-pill offline';
    dom.connectionText.textContent = 'ESP32 OFFLINE';
    dom.deviceStatusText.textContent = 'OFFLINE';
    dom.deviceStatusText.style.color = '#f43f5e';

    const lastSeenFormatted = formatTimestamp(stats.last_seen_timestamp);
    dom.statusBanner.className = 'status-banner banner-danger';
    dom.bannerIcon.textContent = '⚠️';
    dom.bannerMessage.textContent = `ESP32 Offline: No heartbeat received for >30s (Last heartbeat: ${lastSeenFormatted.relative}). Check device power and Wi-Fi hotspot.`;
  }
}

// Fetch and update charts
async function updateCharts() {
  try {
    const res = await fetch('/api/chart-data?limit=30');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const hasData = data.labels && data.labels.length > 0;
    dom.chart1Empty.classList.toggle('visible', !hasData);
    dom.chart2Empty.classList.toggle('visible', !hasData);

    if (hasData) {
      // Update Cumulative Chart
      state.cumulativeChart.data.labels = data.labels;
      state.cumulativeChart.data.datasets[0].data = data.event_counts;
      state.cumulativeChart.update('none');

      // Update Activity Chart
      state.activityChart.data.labels = data.labels;
      state.activityChart.data.datasets[0].data = data.activity_deltas;
      state.activityChart.data.datasets[1].data = data.sensor_states;
      state.activityChart.update('none');
    }
  } catch (err) {
    console.warn('Failed to fetch chart data:', err);
  }
}

// Render row for live stream or history
function buildTableRow(r) {
  const ts = formatTimestamp(r.created_at);
  const statusBadge = r.magnet_detected
    ? '<span class="badge badge-rose">MAGNET DETECTED</span>'
    : '<span class="badge badge-subtle">NO MAGNET</span>';

  return `
    <tr>
      <td class="cell-mono">#${r.id}</td>
      <td class="cell-mono">${escapeHtml(r.device_id)}</td>
      <td class="cell-mono" style="font-weight:700; color:#06b6d4;">${r.event_count}</td>
      <td>${statusBadge}</td>
      <td class="cell-mono">${formatUptime(r.uptime_ms)}</td>
      <td class="cell-mono">${ts.utc}</td>
      ${r.relative !== undefined ? `<td class="cell-mono" style="color:#94a3b8">${ts.relative}</td>` : ''}
    </tr>
  `;
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (m) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[m]));
}

// Update recent readings preview on Dashboard
async function updateLiveStreamTable() {
  try {
    const res = await fetch('/api/history?limit=5&offset=0');
    if (!res.ok) return;
    const data = await res.json();

    if (!data.readings || data.readings.length === 0) {
      dom.liveStreamTbody.innerHTML = '<tr class="empty-row"><td colspan="6">No telemetry received yet. Waiting for ESP32...</td></tr>';
      return;
    }

    dom.liveStreamTbody.innerHTML = data.readings.map(r => buildTableRow(r)).join('');
  } catch (err) {
    console.warn('Failed to fetch live stream table:', err);
  }
}

// Fetch Full Paginated History
async function fetchHistory() {
  const offset = state.historyPage * state.historyLimit;
  try {
    dom.fullHistoryTbody.innerHTML = '<tr class="empty-row"><td colspan="7">Loading records from PostgreSQL...</td></tr>';
    const res = await fetch(`/api/history?limit=${state.historyLimit}&offset=${offset}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    state.historyTotal = data.total;
    dom.historyTotalCount.textContent = `Total Records: ${data.total}`;

    if (!data.readings || data.readings.length === 0) {
      dom.fullHistoryTbody.innerHTML = '<tr class="empty-row"><td colspan="7">No records found in database.</td></tr>';
      dom.pagePrevBtn.disabled = true;
      dom.pageNextBtn.disabled = true;
      dom.paginationInfo.textContent = 'Page 0 of 0';
      return;
    }

    const totalPages = Math.ceil(data.total / state.historyLimit) || 1;
    dom.paginationInfo.textContent = `Page ${state.historyPage + 1} of ${totalPages}`;
    dom.pagePrevBtn.disabled = state.historyPage <= 0;
    dom.pageNextBtn.disabled = state.historyPage >= totalPages - 1;

    dom.fullHistoryTbody.innerHTML = data.readings.map(r => {
      const ts = formatTimestamp(r.created_at);
      const statusBadge = r.magnet_detected
        ? '<span class="badge badge-rose">MAGNET DETECTED</span>'
        : '<span class="badge badge-subtle">NO MAGNET</span>';

      return `
        <tr>
          <td class="cell-mono">#${r.id}</td>
          <td class="cell-mono">${escapeHtml(r.device_id)}</td>
          <td class="cell-mono" style="font-weight:700; color:#06b6d4;">${r.event_count}</td>
          <td>${statusBadge}</td>
          <td class="cell-mono">${formatUptime(r.uptime_ms)}</td>
          <td class="cell-mono">${ts.utc}</td>
          <td class="cell-mono" style="color:#94a3b8">${ts.relative}</td>
        </tr>
      `;
    }).join('');

  } catch (err) {
    console.error('Failed to fetch history:', err);
    dom.fullHistoryTbody.innerHTML = `<tr class="empty-row"><td colspan="7" style="color:#f43f5e">Error loading history: ${escapeHtml(err.message)}</td></tr>`;
  }
}

// Export History to CSV
async function exportHistoryToCsv() {
  try {
    dom.exportCsvBtn.disabled = true;
    dom.exportCsvBtn.innerHTML = 'Exporting...';

    // Fetch up to 200 records for export
    const res = await fetch('/api/history?limit=200&offset=0');
    if (!res.ok) throw new Error('Failed to fetch records for export');
    const data = await res.json();

    if (!data.readings || data.readings.length === 0) {
      alert('No data available to export.');
      return;
    }

    const headers = ['ID', 'Device ID', 'Event Count', 'Magnet Detected', 'Uptime (ms)', 'Created At (UTC)'];
    const rows = data.readings.map(r => [
      r.id,
      `"${r.device_id}"`,
      r.event_count,
      r.magnet_detected ? 'TRUE' : 'FALSE',
      r.uptime_ms,
      `"${r.created_at}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map(e => e.join(','))].join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `magnotrack_readings_${new Date().toISOString().slice(0, 19)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    alert(`CSV export failed: ${err.message}`);
  } finally {
    dom.exportCsvBtn.disabled = false;
    dom.exportCsvBtn.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
      Export CSV
    `;
  }
}

// Master Polling Function
async function pollDashboard() {
  if (state.isFetching) return;
  state.isFetching = true;

  try {
    const res = await fetch('/api/stats');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const stats = await res.json();

    updateKPIs(stats);
    await updateCharts();
    await updateLiveStreamTable();

    state.hasReceivedInitialData = true;
  } catch (err) {
    console.error('Polling error:', err);
    dom.connectionPill.className = 'status-pill offline';
    dom.connectionText.textContent = 'BACKEND UNREACHABLE';
    dom.statusBanner.className = 'status-banner banner-danger';
    dom.bannerIcon.textContent = '❌';
    dom.bannerMessage.textContent = 'Unable to reach MagnoTrack backend server. Check server status or network connection.';
  } finally {
    state.isFetching = false;
  }
}

// Event Listeners
function initListeners() {
  // Manual Refresh
  dom.refreshBtn.addEventListener('click', async () => {
    dom.refreshBtn.classList.add('spinning');
    await pollDashboard();
    setTimeout(() => dom.refreshBtn.classList.remove('spinning'), 600);
  });

  // Auto-Refresh Toggle
  dom.autoRefreshCheck.addEventListener('change', (e) => {
    state.autoRefresh = e.target.checked;
    if (state.autoRefresh) {
      startPolling();
    } else {
      stopPolling();
    }
  });

  // Full History Toolbar
  dom.historyLimitSelect.addEventListener('change', (e) => {
    state.historyLimit = parseInt(e.target.value, 10);
    state.historyPage = 0;
    fetchHistory();
  });

  dom.pagePrevBtn.addEventListener('click', () => {
    if (state.historyPage > 0) {
      state.historyPage--;
      fetchHistory();
    }
  });

  dom.pageNextBtn.addEventListener('click', () => {
    const totalPages = Math.ceil(state.historyTotal / state.historyLimit);
    if (state.historyPage < totalPages - 1) {
      state.historyPage++;
      fetchHistory();
    }
  });

  dom.refreshHistoryBtn.addEventListener('click', () => {
    fetchHistory();
  });

  dom.exportCsvBtn.addEventListener('click', exportHistoryToCsv);
}

// Start and Stop Auto-Polling
function startPolling() {
  stopPolling();
  state.timerId = setInterval(pollDashboard, state.refreshIntervalMs);
}

function stopPolling() {
  if (state.timerId) {
    clearInterval(state.timerId);
    state.timerId = null;
  }
}

// Live Clock
function initClock() {
  setInterval(() => {
    const now = new Date();
    const pad = (n) => String(n).padStart(2, '0');
    dom.utcClock.textContent = `UTC ${pad(now.getUTCHours())}:${pad(now.getUTCMinutes())}:${pad(now.getUTCSeconds())}`;
  }, 1000);
}

// Initialization on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initCharts();
  initListeners();
  initClock();

  // Initial immediate fetch
  pollDashboard();
  startPolling();
});
