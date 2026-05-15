import { RefreshCcw, Trash2 } from "lucide-react";

function ImageCard({ img, caption, tags, status, onDelete, onClick, onReprocess, isReprocessing }) {
  const tagList = Array.isArray(tags) ? tags : [];
  const isReady = status === "ready";
  const isProcessing = status === "processing" || status === "pending";
  const isFailed = status === "failed";

  const handleDelete = (event) => {
    event.stopPropagation();
    onDelete();
  };

  const handleReprocess = (event) => {
    event.stopPropagation();
    onReprocess?.();
  };

  return (
    <div
      className={`bg-[#000000] border rounded-2xl p-4 relative group transition ${
        isFailed ? "border-red-900/70" : "border-[#282829]"
      } ${isReady ? "cursor-pointer" : "cursor-default"}`}
      onClick={isReady ? onClick : undefined}
    >
      <div className="absolute left-3 top-3 z-10">
        <span
          className={`rounded-full px-3 py-1 text-[10px] font-medium uppercase tracking-[0.18em] ${
            isReady
              ? "bg-emerald-500/15 text-emerald-300"
              : isFailed
              ? "bg-red-500/15 text-red-300"
              : "bg-amber-500/15 text-amber-300"
          }`}
        >
          {status ?? "unknown"}
        </span>
      </div>

      {/* DELETE BUTTON */}
      <button
        onClick={handleDelete}
        className="absolute top-3 right-3 bg-black/60 p-2 rounded-lg opacity-0 group-hover:opacity-100 transition"
      >
        <Trash2 size={16} className="text-red-400" />
      </button>

      {(isFailed || isReady) && (
        <button
          onClick={handleReprocess}
          disabled={isReprocessing}
          className="absolute top-14 right-3 bg-black/60 p-2 rounded-lg opacity-0 group-hover:opacity-100 transition disabled:cursor-not-allowed disabled:opacity-60"
        >
          <RefreshCcw size={16} className="text-sky-300" />
        </button>
      )}

      <img
        src={img}
        alt="user upload"
        className={`w-full h-52 object-cover rounded-xl ${
          isProcessing ? "opacity-60" : ""
        }`}
      />

      <div className="mt-4">
        <h3 className="text-sm font-medium text-white">
          {caption || (isProcessing ? "Processing image..." : "Caption unavailable")}
        </h3>

        {isProcessing && (
          <p className="mt-2 text-xs text-amber-300">
            AI metadata and search indexing are still running.
          </p>
        )}

        {isFailed && (
          <p className="mt-2 text-xs text-red-300">
            Processing failed. Reprocess the image to try again.
          </p>
        )}

        {isReprocessing && (
          <p className="mt-2 text-xs text-sky-300">
            Reprocessing has been queued for this asset.
          </p>
        )}

        {/* TAGS */}
        <div className="flex flex-wrap gap-2 mt-3">
          {tagList.map((tag, index) => (
            <span
              key={index}
              className="text-xs bg-[#1c1c1c] px-3 py-1 rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ImageCard;
