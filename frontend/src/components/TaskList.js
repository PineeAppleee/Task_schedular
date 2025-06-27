import React from 'react';
function TaskList({ tasks }) {
  return (
    <ul className="list-group mb-4">
      {tasks.map((task, idx) => (
        <li className="list-group-item" key={idx}>
          Arrival: {task.arrival}, Burst: {task.burst}, Priority: {task.priority}
        </li>
      ))}
    </ul>
  );
}
export default TaskList;