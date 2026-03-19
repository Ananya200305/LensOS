import React, { useState, useEffect } from "react";
import UploadButton from "../components/UploadButton";
import ImageCard from "../components/ImageCard";
import { getAssets, deleteAsset, searchAsset, uploadAsset } from "../api/assetApi";
import { Search, LogOut } from "lucide-react";
import {useNavigate} from 'react-router-dom'

function DashboardPage() {
  const [images, setImages] = useState([]);
  const [searchQuery, setSearchQuery] = useState("")
  const [isUploading, setIsUploading] = useState(false)

  const navigate = useNavigate()

  const fetchImages = async () => {
    try {
      const res = await getAssets();
      setImages(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  const handleUpload = async (file) => {
    try {
      setIsUploading(true);
      await uploadAsset(file);
      await fetchImages();
    } catch (error) {
      console.log(error)
    }finally{
      setIsUploading(false)
    }
  }

  const handleDelete = async (id) => {
    try{
      await deleteAsset(id)
      fetchImages()
    }catch(err){
      console.log(err)
    }
  }

  const handleSearch = async () => {
    try {

      if (!searchQuery.trim()) {
        fetchImages();
        return;
      }

      const res = await searchAsset(searchQuery);
      setImages(res.data);

    } catch (err) {
      console.log(err);
    }
  };

  const handleLogout = () => {
    if (!window.confirm("Are you sure you want to logout?")) return;
    localStorage.removeItem("token")
    navigate('/login')
  }

  useEffect(() => {
    fetchImages();
  }, []);

  return (
    <div className="bg-[#000000] min-h-screen text-white">
      <div className={isUploading ? "pointer-events-none opacity-70" : ""}>
      {/* NAVBAR */}
      <div className="flex items-center justify-between px-10 py-5 border-b border-[#1E293B]">

        {/* LOGO */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-md border border-gray-500 flex items-center justify-center">
            ⌘
          </div>
          <span className="text-lg font-semibold">LensOS</span>
        </div>

        {/* SEARCH */}
        <div className="flex items-center bg-[#010102] border border-[#1E293B] rounded-full px-4 py-2 w-[500px]">

          <input
            type="text"
            placeholder="Search photos..."
            className="bg-transparent outline-none text-sm w-full text-gray-300"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />

          <button
            onClick={handleSearch}
            className="ml-3 p-2 rounded-full hover:bg-[#1E293B]"
          >
            <Search size={18} className="text-gray-400" />
          </button>

        </div>

        {/* RIGHT */}
        <div className="flex items-center gap-4">
          <button onClick={handleLogout} className="flex items-center gap-2 bg-[#3d5571] px-5 py-2 rounded-full text-sm hover:bg-[#24599c]">
            <LogOut size={16} />
            Logout
          </button>

          <img
            src="https://i.pravatar.cc/40"
            className="w-9 h-9 rounded-full"
          />
        </div>
      </div>

      {/* PAGE CONTENT */}
      <div className="px-10 py-10">

        {/* HEADER */}
        <div className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-semibold">All Photos</h1>
            <p className="text-gray-400 text-sm mt-1">
              Manage and organize your visual library
            </p>
          </div>

          <UploadButton onUpload={handleUpload} isUploading={isUploading} />
        </div>

        {/* EMPTY STATE */}
        {images.length === 0 && (
          <p className="text-gray-400 text-center mt-20">
            No images yet. Upload your first photo.
          </p>
        )}

        {/* GRID */}
        <div className="grid grid-cols-4 gap-8">
          {images.map((img) => (
            <ImageCard key={img.id} img={img.image_url} caption={img.caption} tags={img.tags} onDelete={() => handleDelete(img.id)} />
          ))}
        </div>

      </div>
    </div>
      {isUploading && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center">
    
          <div className="flex flex-col items-center gap-4">

            {/* Spinner */}
            <div className="w-12 h-12 border-4 border-white border-t-transparent rounded-full animate-spin"></div>

            {/* Text */}
            <p className="text-white text-lg font-semibold">
                Uploading...
            </p>

          </div>

        </div>
      )}
    </div>
  );
}

export default DashboardPage;