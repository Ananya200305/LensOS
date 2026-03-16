import React from "react";
import { uploadAsset } from "../api/assetApi";
import { Upload } from "lucide-react";

function UploadButton({ onUpload }) {

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    await uploadAsset(file);
    onUpload();
  };

  return (
    <label className="flex items-center gap-2 bg-[#3d5571] hover:bg-[#24599c] px-6 py-3 rounded-full cursor-pointer text-sm">

      <Upload size={18} />

      Upload Image

      <input
        type="file"
        className="hidden"
        onChange={handleUpload}
      />

    </label>
  );
}

export default UploadButton;