import RegisterForm from "../components/RegisterForm.jsx";
import Header from "../components/Header.jsx";
import BackLink from "../components/BackLink.jsx";

export default function Login() {
  return (
    <div className="bg-light min-h-screen">
          <Header />
          <RegisterForm />
          <BackLink to="/auth" text="Назад" />
    </div>
  );
}
