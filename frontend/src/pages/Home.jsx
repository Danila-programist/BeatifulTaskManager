import GradientButton from "../components/GradientButton.jsx";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">TaskManager</h1>
      <p className="text-lg text-gray-600 mb-6">
        Управляй своими задачами просто и красиво
      </p>
      <GradientButton />
    </div>
  );
}
