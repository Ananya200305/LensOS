import {React, useState} from "react";
import { useNavigate } from "react-router-dom";
import DemoModal from "../components/DemoModal";

const images = [
  "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
  "https://images.unsplash.com/photo-1492724441997-5dc865305da7",
  "https://images.unsplash.com/photo-1500648767791-00dcc994a43e",
  "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
  "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
  "https://images.unsplash.com/photo-1470770841072-f978cf4d019e",
];

export default function LandingPage() {
  const [showDemo, setShowDemo] = useState(false)
  const navigate = useNavigate()

  const handleLoginClick = () => {
    navigate("/login")
  }

  const handleSignupClick = () => {
    navigate("/signup")
  }

  return (
    <div className="bg-[#000000] text-white min-h-screen font-sans">

      {/* NAVBAR */}
      <nav className="flex justify-between items-center px-10 py-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-md border border-gray-500 flex items-center justify-center">
            ⌘
          </div>
          <span className="text-lg font-semibold">LensOS</span>
        </div>

        <div className="flex items-center gap-6">
          <button className="text-gray-300 hover:text-white" onClick={handleLoginClick}>
            Login
          </button>

          <button className="bg-blue-600 px-5 py-2 rounded-full hover:bg-blue-500 transition" onClick={handleSignupClick}>
            Sign Up
          </button>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="max-w-7xl mx-auto px-10 py-16 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">

        {/* LEFT TEXT */}
        <div>
          <h1 className="text-5xl font-bold leading-tight mt-6">
            Search your photos by{" "}
            <span className="text-blue-500">meaning</span>, not filenames
          </h1>

          <p className="text-gray-400 mt-6 text-lg">
            AI-powered captions, automatic tagging and semantic retrieval
            for image collections.
          </p>

          <div className="flex gap-4 mt-8">
            <button className="bg-blue-600 px-6 py-3 rounded-lg hover:bg-blue-500" onClick={handleLoginClick}>
              Get Started →
            </button>

            <button className="bg-[#141a2b] px-6 py-3 rounded-lg hover:bg-[#1d243a]" onClick={() => setShowDemo(true)}>
              View Demo
            </button>
          </div>
        </div>

        {/* HERO IMAGE */}
        <div className="bg-[#0d1324] p-4 rounded-2xl shadow-xl">
          <div className="relative rounded-xl overflow-hidden">
            <img
              src="https://images.unsplash.com/photo-1510127034890-ba27508e9f1c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              alt="camera"
              className="rounded-xl"
            />

            {/* SEARCH OVERLAY */}
            <div className="absolute bottom-4 left-4 right-4 bg-black/60 backdrop-blur-md rounded-full px-5 py-3 flex items-center gap-2">
              <span>🔍</span>
              <span className="text-gray-300 text-sm">
                "Show me photos of happy moments from last summer..."
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* GALLERY STRIP */}
      <section className="bg-[#121212] max-w-7xl mx-auto px-10 py-16">
        <h2 className="text-3xl font-semibold mb-2">
          Your gallery, reimagined
        </h2>

        <p className="text-gray-400 mb-10">
          LensOS automatically sorts your library into beautiful,
          intuitive collections.
        </p>

        <div className="flex gap-6 overflow-x-auto pb-4">
          {images.map((img, index) => (
            <img
              key={index}
              src={img}
              className="w-40 h-40 rounded-xl object-cover flex-shrink-0"
            />
          ))}
        </div>
      </section>

      {/* FEATURES */}
      <section className="max-w-7xl mx-auto px-10 py-20 grid md:grid-cols-3 gap-12">

        <div>
          <h3 className="text-xl font-semibold mb-3">AI Captions</h3>
          <p className="text-gray-400">
            Auto-generated natural language descriptions for your images
            using vision-language models.
          </p>
        </div>

        <div>
          <h3 className="text-xl font-semibold mb-3">
            Automatic Tags
          </h3>
          <p className="text-gray-400">
            Structured object and scene labeling extracted from image
            captions.
          </p>
        </div>

        <div>
          <h3 className="text-xl font-semibold mb-3">
            Semantic Search
          </h3>
          <p className="text-gray-400">
            Search images by meaning using vector embeddings instead of
            keywords.
          </p>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-gray-800 py-8 px-10 flex justify-between text-gray-400 text-sm">
        <span>LensOS</span>

        <div className="flex gap-6">
          <span>Privacy</span>
          <span>Terms</span>
        </div>

        <span>© 2026 LensOS</span>
      </footer>

      <DemoModal isOpen={showDemo} onClose={() => setShowDemo(false)} />

    </div>
  );
}