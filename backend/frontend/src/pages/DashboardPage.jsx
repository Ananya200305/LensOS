import React, { useState, useEffect } from "react";
import UploadButton from "../components/UploadButton";
import ImageCard from "../components/ImageCard";
import { getAssets } from "../api/assetApi";

function DashboardPage() {
  const [images, setImages] = useState([]);

  const fetchImages = async () => {
    try {
      const res = await getAssets();
      console.log(res.data);
      setImages(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchImages();
  }, []);

  return (
    <div className="bg-[#0f172a] min-h-screen p-10">
      
      {/* Top bar */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-white text-3xl font-semibold">All Photos</h1>
        <UploadButton onUpload={fetchImages} />
      </div>

      {/* Empty state */}
      {images.length === 0 && (
        <p className="text-gray-400 text-center mt-20">
          No images yet. Upload your first photo 📸
        </p>
      )}

      {/* Gallery grid */}
      <div className="grid grid-cols-4 gap-6">
        {images.map((img) => (
          <ImageCard key={img.id} img={img.image_url} />
        ))}
      </div>

    </div>
  );
}

export default DashboardPage;