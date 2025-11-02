import AuthButtons from "../components/AuthButton.jsx";
import Header from "../components/Header.jsx";

export default function AuthPage() {

  return (
    <div className="bg-light min-h-screen">
      <Header />
      <AuthButtons />
    </div>
  );
}
