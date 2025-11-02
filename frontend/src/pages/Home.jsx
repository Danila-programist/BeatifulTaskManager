import HomeButton from "../components/HomeButton.jsx";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-light">
      <h1 className="text-5xl font-bold mb-4 text-accent">TaskManager</h1>
      <p className="text-lg text-grayish mb-8">
        Управляй своими задачами просто и красиво
      </p>
      <HomeButton />
    </div>
  );
}

