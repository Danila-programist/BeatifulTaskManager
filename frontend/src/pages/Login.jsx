import LoginPassword from "../components/LoginPassword.jsx";
import Header from "../components/Header.jsx";
import BackLink from "../components/BackLink.jsx";


export default function Login() {
  return (
    <div className="bg-light min-h-screen">
          <Header />
          <LoginPassword />
          <BackLink to="/auth" text="Назад" />
    </div>
  );
}
