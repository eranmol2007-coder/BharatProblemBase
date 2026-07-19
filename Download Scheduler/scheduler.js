let tasks = [];
let timers = {};
let logCount = 0;

// ── Init dropdowns ────────────────────────────────
function fillHours() {
  const sel = document.getElementById('fhour');
  for (let i = 1; i <= 12; i++) {
    const opt = document.createElement('option');
    opt.value = String(i).padStart(2, '0');
    opt.textContent = String(i).padStart(2, '0');
    if (i === 9) opt.selected = true;
    sel.appendChild(opt);
  }
}

function fillMinutes() {
  const sel = document.getElementById('fminute');
  for (let i = 0; i <= 59; i++) {
    const opt = document.createElement('option');
    opt.value = String(i).padStart(2, '0');
    opt.textContent = String(i).padStart(2, '0');
    if (i === 0) opt.selected = true;
    sel.appendChild(opt);
  }
}

fillHours();
fillMinutes();

// ── Navigation ────────────────────────────────────
function showPanel(name) {
  document.getElementById('panel-scheduler').style.display = name === 'scheduler' ? 'block' : 'none';
  document.getElementById('panel-log').style.display = name === 'log' ? 'block' : 'none';

  document.querySelectorAll('.nav-item').forEach((el, i) => {
    el.classList.toggle('active', (i === 0 && name === 'scheduler') || (i === 1 && name === 'log'));
  });

  if (name === 'log') {
    logCount = 0;
    const badge = document.getElementById('log-badge');
    badge.style.display = 'none';
    badge.textContent = '0';
  }
}

// ── Add task ──────────────────────────────────────
function addTask() {
  const name   = document.getElementById('fname').value.trim();
  const url    = document.getElementById('furl').value.trim();
  const days   = document.getElementById('fdays').value;
  const hour   = document.getElementById('fhour').value;
  const minute = document.getElementById('fminute').value;
  const ampm   = document.getElementById('fampm').value;

  if (!name || !url) { alert('Please fill in all fields.'); return; }

  const time24 = convertTo24(hour, minute, ampm);
  const displayTime = `${hour}:${minute} ${ampm}`;

  const task = { id: Date.now(), name, url, time: time24, displayTime, days, active: true, lastRun: null };
  tasks.push(task);
  saveTasks();
  scheduleTask(task);
  renderTasks();
  addLog('info', `Scheduled "${name}" — ${displayTime} · ${daysLabel(days)}`);

  document.getElementById('fname').value = '';
  document.getElementById('furl').value = '';
  document.getElementById('fhour').value = '09';
  document.getElementById('fminute').value = '00';
  document.getElementById('fampm').value = 'PM';
  document.getElementById('fdays').value = 'everyday';
}

// ── Schedule ──────────────────────────────────────
function scheduleTask(task) {
  if (timers[task.id]) clearInterval(timers[task.id]);

  timers[task.id] = setInterval(() => {
    if (!task.active) return;
    const now = new Date();
    const [h, m] = task.time.split(':').map(Number);
    const day = now.getDay();

    const match = {
      everyday:  true,
      weekdays:  day >= 1 && day <= 5,
      weekends:  day === 0 || day === 6,
      monday:    day === 1,
      tuesday:   day === 2,
      wednesday: day === 3,
      thursday:  day === 4,
      friday:    day === 5
    }[task.days];

    if (match && now.getHours() === h && now.getMinutes() === m && now.getSeconds() === 0) {
      triggerDownload(task);
    }
  }, 1000);
}

function triggerDownload(task) {
  const a = document.createElement('a');
  a.href = task.url;
  a.download = task.name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  task.lastRun = new Date().toISOString();
  saveTasks();
  addLog('success', `✓ Downloaded "${task.name}"`);
  renderTasks();
}

function toggleTask(id) {
  const task = tasks.find(t => t.id === id);
  if (!task) return;
  task.active = !task.active;
  saveTasks();
  addLog(task.active ? 'info' : 'warn', `"${task.name}" ${task.active ? 'resumed' : 'paused'}`);
  renderTasks();
}

function deleteTask(id) {
  const task = tasks.find(t => t.id === id);
  if (!task || !confirm(`Remove "${task.name}" from schedule?`)) return;
  clearInterval(timers[id]);
  delete timers[id];
  tasks = tasks.filter(t => t.id !== id);
  saveTasks();
  addLog('warn', `Removed "${task.name}"`);
  renderTasks();
}

function downloadNow(id) {
  const task = tasks.find(t => t.id === id);
  if (task) triggerDownload(task);
}

// ── Render ────────────────────────────────────────
function renderTasks() {
  const section = document.getElementById('tasks-section');
  const list    = document.getElementById('task-list');
  const empty   = document.getElementById('empty-state');

  const active = tasks.filter(t => t.active).length;
  document.getElementById('stat-active').textContent = active;
  document.getElementById('stat-total').textContent  = tasks.length;

  if (tasks.length === 0) {
    section.style.display = 'none';
    empty.style.display   = 'block';
    return;
  }

  section.style.display = 'block';
  empty.style.display   = 'none';

  list.innerHTML = tasks.map(t => `
    <div class="task-item">
      <div class="task-thumb">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8m8 4H8"/></svg>
      </div>
      <div class="task-body">
        <div class="task-name">${esc(t.name)}</div>
        <div class="task-url">${esc(t.url)}</div>
        <div class="task-meta">
          <span class="badge badge-time">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            ${esc(t.displayTime || formatTime(t.time))} · ${daysLabel(t.days)}
          </span>
          <span class="badge ${t.active ? 'badge-active' : 'badge-paused'}">
            ${t.active ? `
              <span class="pulsing-wave-container">
                <span class="pulsing-wave-core"></span>
              </span>
              Active
            ` : `
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="width:8px; height:8px;"><rect x="5" y="4" width="4" height="16"/><rect x="15" y="4" width="4" height="16"/></svg> Paused
            `}
          </span>
          ${t.active ? `
            <span class="badge badge-countdown" id="cd-${t.id}">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:9px; height:9px;"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l2 2"/></svg>
              <span class="cd-text">--:--:--</span>
            </span>
          ` : ''}
        </div>
      </div>
      <div class="task-actions">
        <button class="icon-btn" onclick="downloadNow(${t.id})" title="Download now">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 16v1a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
        </button>
        <label class="toggle-switch" title="${t.active ? 'Pause' : 'Resume'}">
          <input type="checkbox" ${t.active ? 'checked' : ''} onchange="toggleTask(${t.id})">
          <span class="slider"></span>
        </label>
        <button class="icon-btn danger" onclick="deleteTask(${t.id})" title="Remove">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M19 7l-.867 12.142A2 2 0 0 1 16.138 21H7.862a2 2 0 0 1-1.995-1.858L5 7m5 4v6m4-4v6m1-10V4a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v3M4 7h16"/></svg>
        </button>
      </div>
    </div>
  `).join('');
}

// ── Countdown ─────────────────────────────────────
function getCountdown(timeStr) {
  const now = new Date();
  const [h, m] = timeStr.split(':').map(Number);
  let next = new Date();
  next.setHours(h, m, 0, 0);
  if (next <= now) next.setDate(next.getDate() + 1);
  const diff = next - now;
  const hh = Math.floor(diff / 3600000);
  const mm = Math.floor((diff % 3600000) / 60000);
  const ss = Math.floor((diff % 60000) / 1000);
  return `${pad(hh)}:${pad(mm)}:${pad(ss)}`;
}

setInterval(() => {
  tasks.forEach(t => {
    if (!t.active) return;
    const el = document.getElementById(`cd-${t.id}`);
    if (el) {
      const txt = el.querySelector('.cd-text');
      if (txt) txt.textContent = getCountdown(t.time);
    }
  });
}, 1000);

// ── Log ───────────────────────────────────────────
function addLog(type, msg) {
  const list = document.getElementById('log-list');
  const empty = list.querySelector('.log-empty');
  if (empty) empty.remove();

  const ts  = new Date().toLocaleTimeString();
  const cls = { success: 'log-success', warn: 'log-warn', info: 'log-info' }[type];
  const el  = document.createElement('div');
  el.className = 'log-entry';
  el.innerHTML = `<span class="log-time">${ts}</span><span class="${cls}">${esc(msg)}</span>`;
  list.prepend(el);

  if (list.children.length > 50) list.lastChild.remove();

  // Badge on log nav item
  logCount++;
  const badge = document.getElementById('log-badge');
  badge.style.display = 'inline';
  badge.textContent = logCount;
}

function clearLog() {
  const list = document.getElementById('log-list');
  list.innerHTML = '<div class="log-empty">No activity yet.</div>';
  logCount = 0;
  document.getElementById('log-badge').style.display = 'none';
}

// ── Helpers ───────────────────────────────────────
function convertTo24(hour, minute, ampm) {
  let h = parseInt(hour);
  if (ampm === 'AM' && h === 12) h = 0;
  if (ampm === 'PM' && h !== 12) h += 12;
  return `${pad(h)}:${minute}`;
}

function formatTime(t) {
  const [h, m] = t.split(':').map(Number);
  return `${h % 12 || 12}:${pad(m)} ${h >= 12 ? 'PM' : 'AM'}`;
}

function daysLabel(d) {
  return { everyday: 'Every day', weekdays: 'Weekdays', weekends: 'Weekends',
           monday: 'Mondays', tuesday: 'Tuesdays', wednesday: 'Wednesdays',
           thursday: 'Thursdays', friday: 'Fridays' }[d] || d;
}

function pad(n) { return String(n).padStart(2, '0'); }

function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ── Persist ───────────────────────────────────────
function saveTasks() {
  localStorage.setItem('scheduler-tasks', JSON.stringify(tasks));
}

function loadTasks() {
  const saved = localStorage.getItem('scheduler-tasks');
  if (!saved) return;
  tasks = JSON.parse(saved);
  tasks.forEach(t => {
    if (!t.displayTime) t.displayTime = formatTime(t.time);
    scheduleTask(t);
  });
  renderTasks();
}

loadTasks();

// ── Retro Notion Ticking Flip Clock ────────────────
function updateFlipClock() {
  const now = new Date();
  let hours = now.getHours();
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  const hh = String(hours).padStart(2, '0');
  
  const days = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
  const dayName = days[now.getDay()];
  
  // Scheduler panel clock elements
  const hrEl = document.getElementById('clock-hour-num');
  const minEl = document.getElementById('clock-min-num');
  const ampmEl = document.getElementById('clock-ampm');
  const dayEl = document.getElementById('clock-day');
  
  if (hrEl) hrEl.textContent = hh;
  if (minEl) minEl.textContent = minutes;
  if (ampmEl) ampmEl.textContent = ampm;
  if (dayEl) dayEl.textContent = dayName;

  // Log panel clock elements
  const hrElLog = document.getElementById('clock-hour-num-log');
  const minElLog = document.getElementById('clock-min-num-log');
  const ampmElLog = document.getElementById('clock-ampm-log');
  const dayElLog = document.getElementById('clock-day-log');
  
  if (hrElLog) hrElLog.textContent = hh;
  if (minElLog) minElLog.textContent = minutes;
  if (ampmElLog) ampmElLog.textContent = ampm;
  if (dayElLog) dayElLog.textContent = dayName;
}
setInterval(updateFlipClock, 1000);
updateFlipClock();