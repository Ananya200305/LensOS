import React from 'react'
import {Check} from 'lucide-react'

function ValidationItem({ valid, text }) {
  return (
    <div className={`flex items-center gap-2 ${
      valid ? "text-green-400" : "text-gray-500"
    }`}>
      <span>
        {valid ? <Check size={16} strokeWidth={0.5} /> : "•"}
      </span>
      <span>{text}</span>
    </div>
  );
}

export default ValidationItem
