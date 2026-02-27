import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Bell,
  Clock,
  Slash,
  Activity,
  ShieldAlert,
  BarChart3,
  Database,
  Send,
  History
} from 'lucide-react';
import './index.css';

const API_BASE = 'http://localhost:8001/api/v1';

function App() {
  const [metrics, setMetrics] = useState({ total: 0, now_rate: 0, later_rate: 0, never_rate: 0 });
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    user_id: 'user_123',
    event_type: 'transactional',
    message: '',
    priority_hint: 'medium',
    source: 'system'
  });

  const fetchLogs = async () => {
    try {
      const { data } = await axios.get(`${API_BASE}/audit`);
      setLogs(data);
    } catch (e) { console.error(e); }
  };

  const fetchMetrics = async () => {
    try {
      const { data } = await axios.get(`${API_BASE}/metrics`);
      setMetrics(data);
    } catch (e) { console.error(e); }
  };

  useEffect(() => {
    fetchLogs();
    fetchMetrics();
    const interval = setInterval(() => {
      fetchLogs();
      fetchMetrics();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/notify`, formData);
      setFormData({ ...formData, message: '' });
      fetchLogs();
      fetchMetrics();
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <header style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ padding: '0.75rem', background: 'var(--accent-primary)', borderRadius: '0.75rem' }}>
          <ShieldAlert size={32} color="white" />
        </div>
        <div>
          <h1 style={{ marginBottom: 0 }}>CyePro Intelligence</h1>
          <p style={{ color: 'var(--text-muted)' }}>AI-Native Notification Prioritization Engine</p>
        </div>
      </header>

      <section className="metrics-grid">
        <div className="glass-card metric-card">
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Total Processed</span>
          <div className="metric-value">{metrics.total}</div>
          <BarChart3 size={16} color="var(--accent-primary)" />
        </div>
        <div className="glass-card metric-card">
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Now Rate</span>
          <div className="metric-value" style={{ color: 'var(--accent-success)' }}>{metrics.now_rate}%</div>
          <Bell size={16} color="var(--accent-success)" />
        </div>
        <div className="glass-card metric-card">
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Later Rate</span>
          <div className="metric-value" style={{ color: 'var(--accent-warning)' }}>{metrics.later_rate}%</div>
          <Clock size={16} color="var(--accent-warning)" />
        </div>
        <div className="glass-card metric-card">
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Suppression Rate</span>
          <div className="metric-value" style={{ color: 'var(--accent-danger)' }}>{metrics.never_rate}%</div>
          <Slash size={16} color="var(--accent-danger)" />
        </div>
      </section>

      <main className="main-content">
        <div className="glass-card">
          <h3><Send size={18} style={{ marginRight: '0.5rem' }} /> Test Event Engine</h3>
          <form onSubmit={handleSubmit}>
            <label>User ID</label>
            <input value={formData.user_id} onChange={e => setFormData({ ...formData, user_id: e.target.value })} />

            <label>Event Type</label>
            <select value={formData.event_type} onChange={e => setFormData({ ...formData, event_type: e.target.value })}>
              <option value="transactional">Transactional (OTP, Security)</option>
              <option value="social">Social (Likes, Comments)</option>
              <option value="promotional">Promotional (Sales, Marketing)</option>
              <option value="system">System (Updates, Sync)</option>
            </select>

            <label>Priority Hint</label>
            <select value={formData.priority_hint} onChange={e => setFormData({ ...formData, priority_hint: e.target.value })}>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>

            <label>Message Content</label>
            <textarea
              rows={4}
              value={formData.message}
              onChange={e => setFormData({ ...formData, message: e.target.value })}
              placeholder="e.g., Your password was reset."
            />

            <button className="btn" type="submit" disabled={loading} style={{ width: '100%', marginTop: '1rem' }}>
              {loading ? 'Analyzing...' : 'Dispatch Event'}
            </button>
          </form>
        </div>

        <div className="glass-card">
          <h3><History size={18} style={{ marginRight: '0.5rem' }} /> Live Audit Feed (XAI)</h3>
          <div style={{ overflowX: 'auto' }}>
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Message</th>
                  <th>Decision</th>
                  <th>AI Reasoning</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log, i) => (
                  <tr key={i}>
                    <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      {new Date(log.created_at).toLocaleTimeString()}
                    </td>
                    <td>
                      <div style={{ fontWeight: 600 }}>{log.event_type}</div>
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>{log.message}</div>
                    </td>
                    <td>
                      <span className={`badge badge-${log.decision.toLowerCase()}`}>
                        {log.decision}
                      </span>
                    </td>
                    <td style={{ fontSize: '0.875rem', fontStyle: 'italic', maxWidth: '300px' }}>
                      {log.reason}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
