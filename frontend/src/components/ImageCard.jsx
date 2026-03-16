import { Trash2 } from "lucide-react";

function ImageCard({ img, caption, tags, onDelete }) {

  const tagList = tags ? JSON.parse(tags) : [];

  return (
    <div className="bg-[#000000] border border-[#282829] rounded-2xl p-4 relative group">

      {/* DELETE BUTTON */}
      <button
        onClick={onDelete}
        className="absolute top-3 right-3 bg-black/60 p-2 rounded-lg opacity-0 group-hover:opacity-100 transition"
      >
        <Trash2 size={16} className="text-red-400" />
      </button>

      <img
        src={img}
        alt="user upload"
        className="w-full h-52 object-cover rounded-xl"
      />

      <div className="mt-4">

        <h3 className="text-sm font-medium text-white">
          {caption}
        </h3>

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