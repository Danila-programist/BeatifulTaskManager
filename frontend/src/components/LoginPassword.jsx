import { Button, Form, Input, message } from "antd";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api/auth";

export default function LoginPassword() {
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
      await loginUser(values.username, values.password);
      message.success("Вы успешно вошли!");
      navigate("/main");
    } catch (error) {
      console.error("Login failed:", error.response?.data || error.message);
      message.error("Ошибка входа. Проверьте логин и пароль.");
    }
  };

  return (
    <div className="flex justify-center mt-[150px]">
      <Form name="login" style={{ maxWidth: 400, width: "100%" }} onFinish={onFinish} layout="vertical">
        <Form.Item label="Логин" name="username" rules={[{ required: true, message: "Пожалуйста, введите логин!" }]}>
          <Input />
        </Form.Item>
        <Form.Item label="Пароль" name="password" rules={[{ required: true, message: "Пожалуйста, введите пароль!" }]}>
          <Input.Password />
        </Form.Item>
        <Form.Item>
          <Button
            htmlType="submit"
            className="bg-accent text-light w-full transition-colors duration-200"
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#1E1E1E")}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#7C3AED")}
          >
            Войти
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
