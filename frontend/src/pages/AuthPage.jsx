import { Button, Flex } from "antd";
import { useNavigate } from "react-router-dom";

export default function AuthPage() {
  const navigate = useNavigate();

  return (
    <Flex direction="column" align="center" justify="center" className="min-h-screen gap-4 bg-light">
      <h1 className="text-5xl font-bold text-accent mb-6">TaskManager</h1>
      <p className="text-grayish mb-8">Войдите или создайте аккаунт, чтобы управлять задачами</p>
      <Flex gap="4">
        <Button
          size="large"
          className="bg-accent text-light px-6 py-2 rounded-lg shadow-md"
          onClick={() => navigate("/auth/login")}
        >
          Войти
        </Button>
        <Button
          size="large"
          className="bg-dark text-light px-6 py-2 rounded-lg shadow-md"
          onClick={() => navigate("/auth/register")}
        >
          Создать аккаунт
        </Button>
      </Flex>
    </Flex>
  );
}
