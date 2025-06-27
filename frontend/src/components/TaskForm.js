import React from 'react';
function TaskForm({ form, handleChange, addTask }) {
  return (
    <form className="row g-3" onSubmit={addTask}>
      <div className="col-md-3">
        <input type="number" className="form-control" name="arrival" placeholder="Arrival Time" value={form.arrival} onChange={handleChange} required />
      </div>
      <div className="col-md-3">
        <input type="number" className="form-control" name="burst" placeholder="Burst Time" value={form.burst} onChange={handleChange} required />
      </div>
      <div className="col-md-3">
        <input type="number" className="form-control" name="priority" placeholder="Priority" value={form.priority} onChange={handleChange} required />
      </div>
      <div className="col-md-3">
        <button type="submit" className="btn btn-primary w-100">Add Task</button>
      </div>
    </form>
  );
}
export default TaskForm;