function ImageCard({ img }) {
  return (
    <div className="bg-[#111827] rounded-xl overflow-hidden shadow-lg hover:scale-105 transition duration-300">
      <img
        src={img}
        alt="user upload"
        className="w-full h-48 object-cover"
      />
    </div>
  );
}

export default ImageCard;
