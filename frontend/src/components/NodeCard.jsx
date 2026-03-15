import React from 'react';
import { Battery, Signal, Clock } from 'lucide-react';

const NodeCard = ({ node }) => {
  const statusColors = {
    MONITOR: 'bg-green-100 text-green-800 border-green-200',
    SLEEP: 'bg-blue-100 text-blue-800 border-blue-200',
    CONFIGURED: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    NOT_CONFIGURED: 'bg-gray-100 text-gray-800 border-gray-200',
  };

  return (
    <div className="p-4 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="font-bold text-lg text-gray-700">Node #{node.id}</h3>
        <span className={`px-2 py-1 rounded text-xs font-semibold border ${statusColors[node.status] || 'bg-gray-100 text-gray-800 border-gray-200'}`}>
          {node.status}
        </span>
      </div>

      <div className="space-y-3">
        <div className="flex items-center text-sm text-gray-600">
          <Battery size={16} className="mr-2 text-blue-500" />
          <span>Battery: <span className="font-medium">{node.battery_level}%</span></span>
        </div>
        <div className="flex items-center text-sm text-gray-600">
          <Signal size={16} className="mr-2 text-purple-500" />
          <span>Signal: <span className="font-medium">{node.signal_strength} dBm</span></span>
        </div>
        <div className="flex items-center text-xs text-gray-500">
          <Clock size={14} className="mr-2" />
          <span>Last Ping: {new Date(node.last_ping).toLocaleTimeString()}</span>
        </div>
      </div>
    </div>
  );
};

export default NodeCard;
