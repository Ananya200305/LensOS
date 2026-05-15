import React, { useState, useEffect } from "react";
import UploadButton from "../components/UploadButton";
import ImageCard from "../components/ImageCard";
import Lightbox from "../components/Lightbox";
import {
  getAssets,
  deleteAsset,
  getAssetFilters,
  hybridSearchAssets,
  reprocessAsset,
  uploadAsset,
} from "../api/assetApi";
import { Search, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

const POLL_INTERVAL_MS = 5000;

function DashboardPage() {
  const [images, setImages] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [isSearching, setIsSearching] = useState(false);
  const [searchFeedback, setSearchFeedback] = useState("");
  const [availableFilters, setAvailableFilters] = useState({
    tags: [],
    detected_objects: [],
    scenes: [],
    environments: [],
    time_of_day: [],
  });
  const [searchFilters, setSearchFilters] = useState({
    tag: "",
    object: "",
    scene: "",
    environment: "",
    timeOfDay: "",
    sortBy: "relevance",
  });
  const [reprocessingIds, setReprocessingIds] = useState([]);

  const navigate = useNavigate();

  const fetchImages = async () => {
    try {
      const res = await getAssets();
      setImages(res.data);
      return res.data;
    } catch (error) {
      console.log(error);
      return [];
    }
  };

  const fetchFilterOptions = async () => {
    try {
      const res = await getAssetFilters();
      setAvailableFilters(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  const handleUpload = async (file) => {
    try {
      setIsUploading(true);
      const res = await uploadAsset(file);
      setImages((prev) => [
        {
          id: res.data.id,
          file_key: res.data.file_key,
          status: res.data.status,
          caption: null,
          tags: [],
          image_url: "",
        },
        ...prev,
      ]);
      await fetchImages();
    } catch (error) {
      console.log(error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteAsset(id);
      setImages((prev) => prev.filter((asset) => asset.id !== id));
      setSelectedIndex((prev) => {
        if (prev === null) return null;
        const nextImages = images.filter((asset) => asset.id !== id);
        if (nextImages.length === 0) return null;
        return Math.min(prev, nextImages.length - 1);
      });
    } catch (err) {
      console.log(err);
    }
  };

  const handleSearch = async () => {
    try {
      setIsSearching(true);
      setSearchFeedback("");
      const hasActiveFilters = Object.values(searchFilters).some(
        (value) => value && value !== "relevance"
      );

      if (!searchQuery.trim() && !hasActiveFilters) {
        await fetchImages();
        setSearchFeedback("Showing your full library.");
        return;
      }

      const payload = {
        query: searchQuery.trim() || "photo",
        tags: searchFilters.tag ? [searchFilters.tag] : [],
        objects: searchFilters.object ? [searchFilters.object] : [],
        scenes: searchFilters.scene ? [searchFilters.scene] : [],
        environment: searchFilters.environment || null,
        time_of_day: searchFilters.timeOfDay ? [searchFilters.timeOfDay] : [],
        page: 1,
        page_size: 24,
        sort_by: searchFilters.sortBy,
      };

      const res = await hybridSearchAssets(payload);
      const results = Array.isArray(res.data?.results) ? res.data.results : [];
      setSelectedIndex(null);
      setImages(results);
      setSearchFeedback(
        results.length > 0
          ? `Hybrid search returned ${results.length} result${results.length === 1 ? "" : "s"}.`
          : "Hybrid search finished, but no assets matched the current query and filters."
      );
    } catch (err) {
      console.log(err);
      setSearchFeedback("Hybrid search failed. Please check the backend response and try again.");
    } finally {
      setIsSearching(false);
    }
  };

  const handleReprocess = async (id) => {
    try {
      setReprocessingIds((prev) => [...new Set([...prev, id])]);
      await reprocessAsset(id);
      setImages((prev) =>
        prev.map((asset) =>
          asset.id === id
            ? {
                ...asset,
                status: "pending",
                caption: null,
                tags: [],
                detected_objects: [],
                scene_label: null,
                time_label: null,
                environment_label: null,
                processed_at: null,
                ranking_score: 0,
              }
            : asset
        )
      );
      await fetchImages();
      await fetchFilterOptions();
    } catch (error) {
      console.log(error);
    } finally {
      setReprocessingIds((prev) => prev.filter((assetId) => assetId !== id));
    }
  };

  const clearFilters = async () => {
    setSearchQuery("");
    setSearchFeedback("");
    setSearchFilters({
      tag: "",
      object: "",
      scene: "",
      environment: "",
      timeOfDay: "",
      sortBy: "relevance",
    });
    await fetchImages();
  };

  const handleLogout = () => {
    if (!window.confirm("Are you sure you want to logout?")) return;
    localStorage.removeItem("token");
    navigate("/login");
  };

  useEffect(() => {
    fetchImages();
    fetchFilterOptions();
  }, []);

  useEffect(() => {
    if (searchQuery.trim()) {
      return undefined;
    }

    const hasPendingAssets = images.some((image) =>
      image.status === "pending" || image.status === "processing"
    );

    if (!hasPendingAssets) {
      return undefined;
    }

    const intervalId = window.setInterval(() => {
      fetchImages();
    }, POLL_INTERVAL_MS);

    return () => window.clearInterval(intervalId);
  }, [images, searchQuery]);

  const selectedImage =
    selectedIndex !== null ? images[selectedIndex] : null;

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
              placeholder="Search with hybrid retrieval..."
              className="bg-transparent outline-none text-sm w-full text-gray-300"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />

            <button
              onClick={handleSearch}
              className="ml-3 p-2 rounded-full hover:bg-[#1E293B] disabled:opacity-50"
              disabled={isSearching}
            >
              <Search size={18} className="text-gray-400" />
            </button>
          </div>

          {/* RIGHT */}
          <div className="flex items-center gap-4">
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 bg-[#3d5571] px-5 py-2 rounded-full text-sm hover:bg-[#24599c]"
            >
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
                Manage your library while uploads process in the background
              </p>
            </div>

            <UploadButton onUpload={handleUpload} isUploading={isUploading} />
          </div>

          <div className="mb-8 rounded-3xl border border-[#1E293B] bg-[#05070b] p-5">
            <div className="mb-4 flex items-center justify-between gap-4">
              <div>
                <h2 className="text-sm font-semibold text-white">Hybrid Search Controls</h2>
                <p className="mt-1 text-xs text-gray-400">
                  Combine semantic query understanding with cinematic metadata filters.
                </p>
              </div>

              <button
                onClick={clearFilters}
                className="rounded-full border border-[#263244] px-4 py-2 text-xs text-gray-300 hover:bg-[#111827]"
              >
                Reset
              </button>
            </div>

            <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-6">
              <select
                value={searchFilters.tag}
                onChange={(e) => setSearchFilters((prev) => ({ ...prev, tag: e.target.value }))}
                className="rounded-2xl border border-[#1E293B] bg-black px-4 py-3 text-sm text-gray-200 outline-none"
              >
                <option value="">All tags</option>
                {availableFilters.tags.map((tag) => (
                  <option key={tag} value={tag}>
                    {tag}
                  </option>
                ))}
              </select>

              <select
                value={searchFilters.object}
                onChange={(e) => setSearchFilters((prev) => ({ ...prev, object: e.target.value }))}
                className="rounded-2xl border border-[#1E293B] bg-black px-4 py-3 text-sm text-gray-200 outline-none"
              >
                <option value="">All objects</option>
                {availableFilters.detected_objects.map((objectName) => (
                  <option key={objectName} value={objectName}>
                    {objectName}
                  </option>
                ))}
              </select>

              <select
                value={searchFilters.scene}
                onChange={(e) => setSearchFilters((prev) => ({ ...prev, scene: e.target.value }))}
                className="rounded-2xl border border-[#1E293B] bg-black px-4 py-3 text-sm text-gray-200 outline-none"
              >
                <option value="">All scenes</option>
                {availableFilters.scenes.map((scene) => (
                  <option key={scene} value={scene}>
                    {scene}
                  </option>
                ))}
              </select>

              <select
                value={searchFilters.environment}
                onChange={(e) => setSearchFilters((prev) => ({ ...prev, environment: e.target.value }))}
                className="rounded-2xl border border-[#1E293B] bg-black px-4 py-3 text-sm text-gray-200 outline-none"
              >
                <option value="">Any environment</option>
                {availableFilters.environments.map((environment) => (
                  <option key={environment} value={environment}>
                    {environment}
                  </option>
                ))}
              </select>

              <select
                value={searchFilters.timeOfDay}
                onChange={(e) => setSearchFilters((prev) => ({ ...prev, timeOfDay: e.target.value }))}
                className="rounded-2xl border border-[#1E293B] bg-black px-4 py-3 text-sm text-gray-200 outline-none"
              >
                <option value="">Any time</option>
                {availableFilters.time_of_day.map((timeValue) => (
                  <option key={timeValue} value={timeValue}>
                    {timeValue}
                  </option>
                ))}
              </select>

              <select
                value={searchFilters.sortBy}
                onChange={(e) => setSearchFilters((prev) => ({ ...prev, sortBy: e.target.value }))}
                className="rounded-2xl border border-[#1E293B] bg-black px-4 py-3 text-sm text-gray-200 outline-none"
              >
                <option value="relevance">Sort: relevance</option>
                <option value="semantic">Sort: semantic</option>
                <option value="recent">Sort: recent</option>
                <option value="oldest">Sort: oldest</option>
              </select>
            </div>

            <div className="mt-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <button
                onClick={handleSearch}
                disabled={isSearching}
                className="inline-flex items-center justify-center rounded-full bg-[#3d5571] px-5 py-3 text-sm font-medium text-white transition hover:bg-[#24599c] disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isSearching ? "Searching..." : "Run Hybrid Search"}
              </button>

              <p className="text-sm text-gray-400">
                {searchFeedback || "Choose filters, add a query if needed, then run hybrid search."}
              </p>
            </div>
          </div>

          {!searchQuery.trim() && images.some((image) => image.status === "pending" || image.status === "processing") && (
            <div className="mb-6 rounded-2xl border border-amber-500/20 bg-amber-500/8 px-5 py-4 text-sm text-amber-100">
              Some uploads are still being processed. This page refreshes automatically every few seconds.
            </div>
          )}

          {/* EMPTY STATE */}
          {images.length === 0 && (
            <p className="text-gray-400 text-center mt-20">
              {searchQuery.trim()
                ? "No ready images matched your search."
                : "No images yet. Upload your first photo."}
            </p>
          )}

          {/* GRID */}
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 xl:grid-cols-4">
            {images.map((img, index) => (
              <ImageCard
                key={img.id}
                img={img.image_url}
                caption={img.caption}
                tags={img.tags}
                status={img.status}
                onDelete={() => handleDelete(img.id)}
                onReprocess={() => handleReprocess(img.id)}
                isReprocessing={reprocessingIds.includes(img.id)}
                onClick={() => setSelectedIndex(index)}
              />
            ))}
          </div>

          {selectedImage && (
            <Lightbox
              images={images}
              index={selectedIndex}
              setIndex={setSelectedIndex}
              onClose={() => setSelectedIndex(null)}
              onDelete={handleDelete}
              onReprocess={handleReprocess}
              isReprocessing={selectedImage ? reprocessingIds.includes(selectedImage.id) : false}
            />
          )}
        </div>
      </div>
      {isUploading && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center">
          <div className="flex flex-col items-center gap-4">
            {/* Spinner */}
            <div className="w-12 h-12 border-4 border-white border-t-transparent rounded-full animate-spin"></div>

            {/* Text */}
            <p className="text-white text-lg font-semibold">Uploading...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default DashboardPage;
