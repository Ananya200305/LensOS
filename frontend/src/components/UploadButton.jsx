import React from "react";
import { Upload } from "lucide-react";

function UploadButton({ onUpload, isUploading }) {

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    await onUpload(file);  
  };

  return (
    <label
      className={`flex items-center gap-2 px-6 py-3 rounded-full text-sm transition ${
        isUploading
          ? "bg-gray-500 cursor-not-allowed"
          : "bg-[#3d5571] hover:bg-[#24599c] cursor-pointer"
      }`}
    >
      <Upload size={18} />

      {isUploading ? "Uploading..." : "Upload Image"}

      <input
        type="file"
        className="hidden"
        onChange={handleUpload}
        disabled={isUploading}
      />
    </label>
  );
}

export default UploadButton;
