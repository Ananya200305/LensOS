import React, { useState } from "react";
import { Search } from "lucide-react";

const demoImages = [
  {
    id: 1,
    image_url: "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
    caption: "Golden sunset over mountains",
    tags: ["sunset", "nature", "mountain"],
  },
  {
    id: 2,
    image_url: "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
    caption: "Luxury watch and perfume setup",
    tags: ["luxury", "watch", "style"],
  },
  {
    id: 3,
    image_url: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    caption: "Leopard resting on tree branch",
    tags: ["wildlife", "animal"],
  },
  {
    id: 4,
    image_url: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
    caption: "Sunset at tropical beach",
    tags: ["sunset", "beach"],
  },
];

export default function DemoContent() {
  const [step, setStep] = useState(0);
  const [images, setImages] = useState(demoImages);
  const [query, setQuery] = useState("");

  const steps = [
    "Welcome to LensOS. This is your AI-powered photo gallery.",
    "You can search images using meaning, not filenames.",
    "Let’s try searching for 'sunset'.",
    "Results are ranked using semantic similarity.",
  ];

  const handleNext = async () => {
    if (step === 2) {
      const word = "sunset";
      let current = "";

      for (let char of word) {
        current += char;
        setQuery(current);
        await new Promise((r) => setTimeout(r, 50));
      }

      const filtered = demoImages.filter((img) =>
        img.caption.toLowerCase().includes("sunset")
      );

      setImages(filtered);
    }

    setStep((prev) => prev + 1);
  };

  return (
    <div className="text-white">

      {/* HEADER */}
      <h2 className="text-xl font-semibold mb-6">Demo Gallery</h2>

      {/* SEARCH */}
      <div className="flex items-center bg-[#010102] border border-[#1E293B] rounded-full px-4 py-2 w-full mb-8">
        <input
          value={query}
          readOnly
          className="bg-transparent outline-none text-sm w-full text-gray-300"
        />
        <Search size={18} />
      </div>

      {/* GRID */}
      <div className="grid grid-cols-2 gap-4">
        {images.map((img) => (
          <div key={img.id} className="bg-[#101010] p-3 rounded-xl">
            <img src={img.image_url} className="rounded-lg mb-2 h-32 w-full object-cover" />
            <p className="text-xs">{img.caption}</p>
          </div>
        ))}
      </div>

      {/* STEP OVERLAY INSIDE MODAL */}
      {step < steps.length && (
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 bg-[#111827] px-5 py-3 rounded-xl shadow-2xl border border-white/10">
          <p className="text-sm mb-2">{steps[step]}</p>
          <button
            onClick={handleNext}
            className="bg-indigo-950 px-3 py-1 rounded text-sm"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}