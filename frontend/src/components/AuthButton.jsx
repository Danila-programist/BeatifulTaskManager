import { Button, Flex } from "antd";
import { useNavigate } from "react-router-dom";

export default function AuthButtons() {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate("/auth/login");
  };

  const handleRegisterClick = () => {
    navigate("/auth/register");
  };

  const handleMouseEnter = (e) => {
    e.currentTarget.style.backgroundColor = "#1E1E1E"; // темный при наведении
  };

  const handleMouseLeave = (e) => {
    e.currentTarget.style.backgroundColor = "#7C3AED"; // фиолетовый по умолчанию
  };

  return (
    <Flex direction="vertical" className="flex-col items-center gap-4 mt-[200px]">
      <Button
        onClick={handleLoginClick}
        className="bg-accent border-none shadow-md px-8 py-2 rounded-lg text-light transition-colors duration-200"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        style={{ color: "#F8FAFC" }}
      >
        Войти
      </Button>
      <Button
        onClick={handleRegisterClick}
        className="bg-accent border-none shadow-md px-8 py-2 rounded-lg text-light transition-colors duration-200"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        style={{ color: "#F8FAFC" }}
      >
        Зарегистрироваться
      </Button>
    </Flex>
  );
}
