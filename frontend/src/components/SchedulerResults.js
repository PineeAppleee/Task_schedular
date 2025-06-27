import React from 'react';
import { ProgressBar } from 'react-bootstrap';
const algoLabels = { fcfs: 'FCFS', sjf: 'SJF', rr: 'Round Robin' };
function SchedulerResults({ result }) {
  if (!result) return null;
  const getAvgTurnaround = (algo) => {
    if (!result[algo]) return 0;
    const arr = result[algo].map(t => t.turnaround);
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  };
  const bestAlgo = ['fcfs', 'sjf', 'rr'].reduce((best, algo) => getAvgTurnaround(algo) < getAvgTurnaround(best) ? algo : best, 'fcfs');
  return (
    <div className="mt-4">
      <h5 className="mb-3">Scheduling Results</h5>
      <div className="mb-4">
        <div className="mb-2 fw-bold">Average Turnaround Time (lower is better):</div>
        {['fcfs', 'sjf', 'rr'].map(algo => (
          <div key={algo} className="mb-3">
            <div className="d-flex justify-content-between align-items-center">
              <span className="fw-semibold" style={{color: result.ai_recommendation.toLowerCase() === algoLabels[algo].toLowerCase() ? '#00ffe7' : '#fff'}}>
                {algoLabels[algo]}
                {result.ai_recommendation.toLowerCase() === algoLabels[algo].toLowerCase() && (
                  <span className="badge badge-primary ms-2">AI Recommended</span>
                )}
                {bestAlgo === algo && (
                  <span className="badge badge-success ms-2">Best</span>
                )}
              </span>
              <span className="fw-bold">{getAvgTurnaround(algo).toFixed(2)}</span>
            </div>
            <ProgressBar
              now={100 - getAvgTurnaround(algo)}
              label={`${(100 - getAvgTurnaround(algo)).toFixed(0)}%`}
              animated
              striped
              variant={bestAlgo === algo ? 'success' : (result.ai_recommendation.toLowerCase() === algoLabels[algo].toLowerCase() ? 'primary' : 'info')}
              style={{height: '24px', transition: 'width 1s'}}
            />
          </div>
        ))}
      </div>
      <div className="alert alert-info mt-4">
        <strong>AI Recommendation:</strong> <span className="text-primary">{result.ai_recommendation}</span>
      </div>
      <details>
        <summary>Raw JSON Result</summary>
        <pre>{JSON.stringify(result, null, 2)}</pre>
      </details>
    </div>
  );
}
export default SchedulerResults;