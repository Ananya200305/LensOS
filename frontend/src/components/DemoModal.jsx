import React from "react";
import { X } from "lucide-react";
import DemoContent from "./DemoContent";

export default function DemoModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">

      {/* BACKDROP */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* MODAL */}
      <div className="relative bg-[#000000] w-[800px] max-h-[90vh] overflow-hidden rounded-2xl border border-white/10 shadow-2xl p-6">

        {/* CLOSE BUTTON */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white"
        >
          <X size={20} />
        </button>

        {/* CONTENT */}
        <DemoContent />

      </div>
    </div>
  );
}