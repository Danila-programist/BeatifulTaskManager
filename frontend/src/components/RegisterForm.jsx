import { Button, Form, Input, message } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function RegisterForm() {
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
      await axios.post(
        "/api/v1/auth/register",
        {
          username: values.username,
          email: values.email,
          password: values.password,
          first_name: values.firstName,
          last_name: values.lastName,
        },
        { withCredentials: true } 
      );

      message.success("Регистрация успешна!");
      navigate("/auth/login"); 
    } catch (error) {
      console.error("Registration failed:", error.response?.data || error.message);
      message.error("Ошибка регистрации. Проверьте введённые данные.");
    }
  };

  return (
    <div className="flex justify-center mt-[150px]">
      <Form
        name="register"
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
          label="Email"
          name="email"
          rules={[
            { required: true, message: "Пожалуйста, введите email!" },
            { type: "email", message: "Введите корректный email!" },
          ]}
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

        <Form.Item
          label="Имя"
          name="firstName"
          rules={[{ required: true, message: "Пожалуйста, введите имя!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Фамилия"
          name="lastName"
          rules={[{ required: true, message: "Пожалуйста, введите фамилию!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item>
          <Button
            htmlType="submit"
            className="bg-accent text-light w-full transition-colors duration-200"
            style={{ color: "#F8FAFC" }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#1E1E1E")}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#7C3AED")}
          >
            Зарегистрироваться
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
