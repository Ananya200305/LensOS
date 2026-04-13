import { X, ChevronLeft, ChevronRight } from "lucide-react";
import { useEffect } from "react";

function Lightbox({ images, index, setIndex, onClose }) {
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

  return (
    <div className="fixed inset-0 bg-black flex flex-col z-50">
      {/*TOP BAR */}
      <div className="flex justify-between items-center px-6 py-4 border-b border-[#1E293B]">
        <p className="text-sm text-gray-400">
          {index + 1} / {images.length}
        </p>
        <p className="text-sm text-gray-300 text-center max-w-2xl">
          {image.caption}
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
        <div className="flex justify-between items-center">
          <div className="flex gap-3">
            <button
              onClick={() => downloadOriginal(image)}
              className="px-3 py-1 bg-[#1E293B] rounded hover:bg-[#334155]"
            >
              Download
            </button>

            <button className="px-3 py-1 bg-[#1E293B] rounded hover:bg-[#334155]">
              Edit
            </button>

            <button className="px-3 py-1 bg-red-600/80 rounded hover:bg-red-600">
              Delete
            </button>
          </div>

          <p className="text-xs text-gray-500">
            Score: {image.score?.toFixed(2) ?? "N/A"}
          </p>
        </div>
      </div>
    </div>
  );
}

export default Lightbox;
