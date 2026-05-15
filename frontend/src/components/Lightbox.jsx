import { X, ChevronLeft, ChevronRight, Trash2, RefreshCcw } from "lucide-react";
import { useEffect, useState } from "react";
import { getAssetIntelligence } from "../api/assetApi";

function Lightbox({ images, index, setIndex, onClose, onDelete, onReprocess, isReprocessing }) {
  const [cinematicAnalysis, setCinematicAnalysis] = useState(null);
  const [isLoadingAnalysis, setIsLoadingAnalysis] = useState(false);

  if (index === null) return null;

  const next = () => {
    setIndex((prev) => (prev + 1) % images.length);
  };

  const prev = () => {
    setIndex((prev) => (prev === 0 ? images.length - 1 : prev - 1));
  };

  const generateFileName = (caption) => {
    if (!caption) return "image";

    // Ensure it's a string
    const safeCaption = String(caption);

    return safeCaption
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, "")
      .trim()
      .replace(/\s+/g, "_")
      .slice(0, 50);
  };

  const downloadOriginal = (image) => {
    const fileName = generateFileName(image.caption);

    const link = document.createElement("a");
    link.href = image.image_url;
    link.setAttribute("download", `${fileName}.jpg`);
    link.setAttribute("target", "_blank"); // fallback

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === "ArrowRight") next();
      if (e.key === "ArrowLeft") prev();
      if (e.key === "Escape") onClose();
    };

    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [index]);

  const image = images[index];
  const isReady = image?.status === "ready";

  useEffect(() => {
    let isCancelled = false;

    const loadCinematicAnalysis = async () => {
      if (!image?.id || image.status !== "ready") {
        setCinematicAnalysis(null);
        setIsLoadingAnalysis(false);
        return;
      }

      try {
        setIsLoadingAnalysis(true);
        const response = await getAssetIntelligence(image.id);
        if (!isCancelled) {
          setCinematicAnalysis(response.data);
        }
      } catch (error) {
        if (!isCancelled) {
          console.log(error);
          setCinematicAnalysis(null);
        }
      } finally {
        if (!isCancelled) {
          setIsLoadingAnalysis(false);
        }
      }
    };

    loadCinematicAnalysis();

    return () => {
      isCancelled = true;
    };
  }, [image?.id, image?.status]);

  const handleDelete = () => {
    onDelete(image.id);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black flex flex-col z-50">
      {/*TOP BAR */}
      <div className="flex justify-between items-center px-6 py-4 border-b border-[#1E293B]">
        <p className="text-sm text-gray-400">
          {index + 1} / {images.length}
        </p>
        <p className="text-sm text-gray-300 text-center max-w-2xl">
          {image.caption || "Processing image..."}
        </p>

        <button onClick={onClose} className="text-gray-400 hover:text-white">
          <X size={24} />
        </button>
      </div>

      {/*IMAGE AREA */}
      <div className="flex-1 flex flex-col items-center justify-center relative px-4">
        {/* Left */}
        <button
          onClick={prev}
          className="absolute left-4 p-2 rounded-full bg-black/40 hover:bg-black/60"
        >
          <ChevronLeft size={28} className="text-white" />
        </button>

        {/* Image */}
        <img
          src={image.image_url}
          alt={image.caption || "Selected asset"}
          className="max-h-[75vh] max-w-[85vw] object-contain rounded-lg"
        />

        {/* Right */}
        <button
          onClick={next}
          className="absolute right-4 p-2 rounded-full bg-black/40 hover:bg-black/60"
        >
          <ChevronRight size={28} className="text-white" />
        </button>
      </div>

      {/*BOTTOM ACTION BAR */}
      <div className="border-t border-[#1E293B] px-6 py-4 bg-black/80 backdrop-blur">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="min-w-0 flex-1">
            <p className="mb-2 text-[11px] uppercase tracking-[0.22em] text-gray-500">
              Cinematic Analysis
            </p>

            {isReady && isLoadingAnalysis && (
              <p className="text-sm text-gray-400">Loading scene intelligence...</p>
            )}

            {!isReady && (
              <p className="text-sm text-gray-400">
                Cinematic analysis will be available once processing is complete.
              </p>
            )}

            {isReady && !isLoadingAnalysis && cinematicAnalysis && (
              <div className="flex flex-wrap gap-2 text-xs text-gray-200">
                {cinematicAnalysis.scene_label && (
                  <span className="rounded-full border border-[#334155] px-3 py-1">
                    Scene: {cinematicAnalysis.scene_label}
                  </span>
                )}
                {cinematicAnalysis.environment_label && (
                  <span className="rounded-full border border-[#334155] px-3 py-1">
                    Environment: {cinematicAnalysis.environment_label}
                  </span>
                )}
                {cinematicAnalysis.time_label && (
                  <span className="rounded-full border border-[#334155] px-3 py-1">
                    Time: {cinematicAnalysis.time_label}
                  </span>
                )}
                {cinematicAnalysis.detected_objects?.map((objectName) => (
                  <span
                    key={objectName}
                    className="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-amber-100"
                  >
                    {objectName}
                  </span>
                ))}
              </div>
            )}
          </div>

          <div className="flex justify-between items-center gap-4">
            <div className="flex gap-3">
            <button
              onClick={() => downloadOriginal(image)}
              disabled={!isReady}
              className="px-3 py-1 bg-[#1E293B] rounded hover:bg-[#334155] disabled:cursor-not-allowed disabled:opacity-50"
            >
              Download
            </button>

            <button
              onClick={handleDelete}
              className="flex items-center gap-2 px-3 py-1 bg-red-600/80 rounded hover:bg-red-600"
            >
              <Trash2 size={14} />
              Delete
            </button>

            <button
              onClick={() => onReprocess?.(image.id)}
              disabled={isReprocessing || !image?.id}
              className="flex items-center gap-2 px-3 py-1 bg-sky-700/80 rounded hover:bg-sky-600 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <RefreshCcw size={14} />
              {isReprocessing ? "Queued" : "Reprocess"}
            </button>
            </div>

            <div className="text-right text-xs text-gray-500">
              <p>Status: {image.status ?? "unknown"}</p>
              <p>Score: {image.score?.toFixed(2) ?? "N/A"}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Lightbox;
