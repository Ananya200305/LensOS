import React from 'react'
import { uploadAsset } from '../api/assetApi'

function UploadButton({onUpload}) {
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    console.log(file)
    await uploadAsset(file);
    onUpload(); // refresh gallery
  };
  return (
    <div>
      <input type="file" onChange={handleUpload} />
    </div>
  )
}

export default UploadButton
