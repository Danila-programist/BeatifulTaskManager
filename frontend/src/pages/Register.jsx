import { Button, Form, Input, Card } from "antd";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const onFinish = (values) => {
    console.log("Регистрация:", values);
    // здесь можно вызвать API для регистрации
    // после успешной регистрации перенаправляем на /auth/login
    navigate("/auth/login");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-light px-4">
      <Card className="w-full max-w-md p-8 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-accent mb-6 text-center">Создать аккаунт</h1>
        <Form
          layout="vertical"
          onFinish={onFinish}
          requiredMark={false}
        >
          <Form.Item
            label="Имя пользователя"
            name="username"
            rules={[{ required: true, message: "Пожалуйста, введите имя пользователя" }]}
          >
            <Input placeholder="Введите имя пользователя" />
          </Form.Item>

          <Form.Item
            label="Email"
            name="email"
            rules={[
              { required: true, message: "Пожалуйста, введите email" },
              { type: "email", message: "Неверный формат email" }
            ]}
          >
            <Input placeholder="Введите email" />
          </Form.Item>

          <Form.Item
            label="Пароль"
            name="password"
            rules={[{ required: true, message: "Пожалуйста, введите пароль" }]}
          >
            <Input.Password placeholder="Введите пароль" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              className="w-full bg-accent hover:bg-dark text-light py-2 rounded-lg transition-colors duration-200"
            >
              Зарегистрироваться
            </Button>
          </Form.Item>

          <p className="text-grayish text-center">
            Уже есть аккаунт?{" "}
            <span
              className="text-accent cursor-pointer"
              onClick={() => navigate("/auth/login")}
            >
              Войти
            </span>
          </p>
        </Form>
      </Card>
    </div>
  );
}
