import { useState } from "react";
import { Button, message } from "antd";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function HomeButton() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      // Попытка проверить авторизацию
      await axios.get("/api/v1/tasks", {
        withCredentials: true,
      });
      navigate("/main"); // если успешный ответ, идём на main
    } catch (error) {
      navigate("/auth"); // если ошибка (не авторизован) — на auth
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      onClick={handleClick}
      loading={loading}
      className="bg-accent border-none shadow-md px-6 py-2 rounded-lg transition-colors duration-200 text-light"
      onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#1E1E1E")}
      onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#7C3AED")}
      style={{ color: "#fff" }}
    >
      Начать работу
    </Button>
  );
}
