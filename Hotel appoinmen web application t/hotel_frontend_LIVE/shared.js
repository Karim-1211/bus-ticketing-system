// shared.js — imported by all dashboard pages
const API = 'https://hotel-api-549w.onrender.com';

function getToken() {
  const t = localStorage.getItem('token');
  if (!t) { window.location.href = 'login.html'; return null; }
  return t;
}

function authHeaders(isForm = false) {
  const t = getToken();
  const h = { 'Authorization': `Bearer ${t}` };
  if (!isForm) h['Content-Type'] = 'application/json';
  return h;
}

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API}${path}`, options);
  if (res.status === 401) { localStorage.clear(); window.location.href = 'login.html'; return; }
  return res;
}

// Toast notification
function showToast(msg, type = 'success') {
  let t = document.getElementById('toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'toast';
    t.className = 'toast';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.className = `toast ${type} show`;
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 3000);
}

// Render sidebar
function renderSidebar(active) {
  const username = localStorage.getItem('username') || 'Admin';
  const initial = username.charAt(0).toUpperCase();

  const nav = [
    { href: 'dashboard.html', icon: '📊', label: 'Dashboard' },
    { href: 'rooms.html',     icon: '🛏️',  label: 'Rooms' },
    { href: 'guests.html',    icon: '👥',  label: 'Guests' },
    { href: 'bookings.html',  icon: '📅',  label: 'Bookings' },
    { href: 'payments.html',  icon: '💳',  label: 'Payments' },
  ];

  const navHtml = nav.map(n => `
    <a href="${n.href}" class="nav-item ${active === n.label ? 'active' : ''}">
      <span class="icon">${n.icon}</span> ${n.label}
    </a>
  `).join('');

  return `
    <aside class="sidebar">
      <div class="sidebar-brand">
        <div class="icon">🏨</div>
        <h2>Grand Hotel</h2>
        <p>Management</p>
      </div>
      <nav class="sidebar-nav">
        <div class="nav-label">Menu</div>
        ${navHtml}
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">${initial}</div>
          <span class="user-name">${username}</span>
          <button class="logout-btn" onclick="logout()" title="Sign out">↩</button>
        </div>
      </div>
    </aside>
  `;
}

function logout() {
  localStorage.clear();
  window.location.href = 'login.html';
}

function formatDate(d) {
  if (!d) return '—';
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

function todayISO() {
  return new Date().toISOString().split('T')[0];
}
