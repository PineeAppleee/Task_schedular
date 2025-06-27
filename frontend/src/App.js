import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import SchedulerResults from './components/SchedulerResults';
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function VerticalBars({ results }) {
  if (!results) return null;
  const algos = [
    { name: 'FCFS', value: results.fcfs.avg_turnaround_time },
    { name: 'SJF', value: results.sjf.avg_turnaround_time },
    { name: 'RR', value: results.rr.avg_turnaround_time }
  ];
  const maxVal = Math.max(...algos.map(a => a.value));
  return (
    <div className="vertical-bars">
      {algos.map(algo => (
        <div key={algo.name} className="vertical-bar" style={{ height: `${(algo.value / maxVal) * 70 + 10}vh`, background: results.ai_recommendation === algo.name ? 'linear-gradient(180deg,#00c6fb 0%,#005bea 100%)' : undefined }}>
          <span className="vertical-bar-value">{algo.value.toFixed(2)}</span>
          <div className="vertical-bar-label">{algo.name}</div>
        </div>
      ))}
    </div>
  );
}

function DetailsPanel({ results }) {
  if (!results) return null;
  return (
    <div className="details-panel">
      <h2 style={{ fontSize: '1.5em', marginBottom: 18 }}>Algorithm Details</h2>
      {['fcfs', 'sjf', 'rr'].map(algo => (
        <div key={algo} style={{ marginBottom: 18 }}>
          <div style={{ fontWeight: 600, color: '#b0b3b8', marginBottom: 4 }}>{algo.toUpperCase()}</div>
          <div>Avg Turnaround: <b>{results[algo].avg_turnaround_time.toFixed(2)}</b></div>
          <div>Avg Waiting: <b>{results[algo].avg_waiting_time.toFixed(2)}</b></div>
          <div>Avg Response: <b>{results[algo].avg_response_time.toFixed(2)}</b></div>
        </div>
      ))}
      <div style={{ marginTop: 18, fontSize: '1.2em', color: '#00c6fb' }}>
        <b>AI Recommendation:</b> {results.ai_recommendation}
      </div>
    </div>
  );
}

function App() {
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState({ arrival: '', burst: '', priority: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const addTask = (e) => {
    e.preventDefault();
    setTasks([...tasks, { ...form }]);
    setForm({ arrival: '', burst: '', priority: '' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const numericTasks = tasks.map(t => ({
      arrival: Number(t.arrival),
      burst: Number(t.burst),
      priority: Number(t.priority)
    }));
    const response = await fetch('http://localhost:5000/schedule', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tasks: numericTasks })
    });
    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <>
      <div className="misty-overlay" />
      <div className="app-container">
        <div className="bg-theme min-vh-100 py-5">
          <div className="container">
            <div className="card shadow-lg p-4 mb-5">
              <h2 className="mb-4 text-center">Task Scheduler</h2>
              <TaskForm form={form} handleChange={handleChange} addTask={addTask} />
              <hr />
              <h4>Tasks</h4>
              <TaskList tasks={tasks} />
              <button className="btn btn-success mb-3" onClick={handleSubmit} disabled={tasks.length === 0 || loading}>
                {loading ? 'Scheduling...' : 'Submit to Scheduler'}
              </button>
              <SchedulerResults result={result} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
export default App;
