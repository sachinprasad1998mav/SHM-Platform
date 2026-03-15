import React, { useState, useEffect } from 'react';
import NodeCard from './components/NodeCard';
import NodeChart from './components/NodeChart';

function App() {
  const [nodes, setNodes] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [filter, setFilter] = useState('ALL');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/nodes/')
      .then(res => res.json())
      .then(data => setNodes(data))
      .catch(err => console.error("Fetch error:", err));

    const socket = new WebSocket('ws://127.0.0.1:8000/nodes/ws/nodes');

    socket.onmessage = (event) => {
      const updatedNode = JSON.parse(event.data);

      setNodes(prevNodes => {
        const exists = prevNodes.find(n => n.id === updatedNode.id);
        if (exists) {
          return prevNodes.map(n => n.id === updatedNode.id ? updatedNode : n);
        }
        return [...prevNodes, updatedNode];
      });

      setChartData(prev => {
        const newEntry = {
          time: new Date().toLocaleTimeString().split(' ')[0],
          battery: updatedNode.battery_level,
          signal: updatedNode.signal_strength
        };
        return [...prev.slice(-14), newEntry];
      });
    };

    return () => socket.close();
  }, []);

  const filteredNodes = filter === 'ALL'
    ? nodes
    : nodes.filter(n => n.status === filter);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 italic">NIRIXENSE</h1>
          <p className="text-gray-500 font-medium">Structural Health Monitoring Platform</p>
        </div>
        <div className="text-right">
          <span className="text-xs font-bold text-green-600 bg-green-100 px-2 py-1 rounded-full uppercase tracking-wider">
            Live System Active
          </span>
        </div>
      </header>

      <div className="flex gap-2 mb-8 bg-white p-2 rounded-lg shadow-sm w-fit border border-gray-100">
        {['ALL', 'MONITOR', 'SLEEP', 'CONFIGURED'].map(status => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-1.5 rounded-md text-sm font-semibold transition-all ${
              filter === status
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            {status.replace('_', ' ')}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredNodes.length > 0 ? (
          filteredNodes.map(node => (
            <NodeCard key={node.id} node={node} />
          ))
        ) : (
          <div className="col-span-full py-12 text-center text-gray-400 italic">No nodes found in this category...</div>
        )}
      </div>

      <div className="mt-12">
        <NodeChart data={chartData} />
      </div>

      <footer className="mt-16 pt-8 border-t border-gray-200 text-center text-gray-400 text-sm">
        &copy; 2026 Nirixense SHM Mini Platform - Architectural Assignment
      </footer>
    </div>
  );
}

export default App;
