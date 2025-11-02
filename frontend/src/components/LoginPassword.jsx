import { Button, Form, Input, message } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function LoginPassword() {
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
      const response = await axios.post("http://localhost:8000/api/v1/auth/login", {
        username: values.username,
        password: values.password,
      });

      const token = response.data.access_token; 
      localStorage.setItem("token", token); 

      message.success("Вы успешно вошли!");
      navigate("/"); 
    } catch (error) {
      console.error("Login failed:", error.response?.data || error.message);
      message.error("Ошибка входа. Проверьте логин и пароль.");
    }
  };

  return (
    <div className="flex justify-center mt-[150px]">
      <Form
        name="login"
        style={{ maxWidth: 400, width: "100%" }}
        onFinish={onFinish}
        layout="vertical"
      >
        <Form.Item
          label="Логин"
          name="username"
          rules={[{ required: true, message: "Пожалуйста, введите логин!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Пароль"
          name="password"
          rules={[{ required: true, message: "Пожалуйста, введите пароль!" }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            className="bg-accent hover:bg-dark text-light w-full"
          >
            Войти
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
