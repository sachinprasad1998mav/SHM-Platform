import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const NodeChart = ({ data }) => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mt-8">
      <h3 className="text-lg font-bold mb-4 text-gray-700">Live Battery & Signal Trend</h3>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="time"
              tick={{fontSize: 12}}
              interval="preserveStartEnd"
            />
            <YAxis yAxisId="left" orientation="left" stroke="#3b82f6" />
            <YAxis yAxisId="right" orientation="right" stroke="#8b5cf6" />
            <Tooltip />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="battery"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              name="Battery %"
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="signal"
              stroke="#8b5cf6"
              strokeWidth={2}
              dot={false}
              name="Signal (dBm)"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default NodeChart;
