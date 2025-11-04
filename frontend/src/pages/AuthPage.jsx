import AuthButtons from "../components/AuthButton.jsx";
import BackLink from "../components/BackLink.jsx";
import Header from "../components/Header.jsx";

export default function AuthPage() {

  return (
    <div className="bg-light min-h-screen">
      <Header />
      <AuthButtons />
      <BackLink to="/" text="Назад"/>
    </div>
  );
}
