import { useState } from "react";
import { Menu, Button, message } from "antd";
import {
  UserOutlined,
  AppstoreOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function SidebarMenu({ onSelect }) {
  const [selectedKey, setSelectedKey] = useState("all");
  const navigate = useNavigate();

  const items = [
    { key: "about", icon: <UserOutlined />, label: "Обо мне" },
    { key: "all", icon: <AppstoreOutlined />, label: "Все задачи" },
  ];

  const handleClick = (e) => {
    setSelectedKey(e.key);
    if (onSelect) onSelect(e.key);
  };

  // 🔹 Выход из аккаунта
  const handleLogout = async () => {
    try {
      await axios.post(
        "http://localhost:8000/api/v1/auth/logout",
        {},
        { withCredentials: true }
      );
      message.success("Вы успешно вышли из аккаунта");
      navigate("/"); // редирект на логин
    } catch (error) {
      console.error("Ошибка при выходе:", error);
      message.error("Не удалось выйти из аккаунта");
    }
  };

  return (
    <div
      style={{
        width: 200,
        minHeight: "calc(100vh - 80px)",
        backgroundColor: "#F8FAFC",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        position: "relative",
        paddingBottom: "16px",
      }}
    >
      {/* Верхнее меню */}
      <Menu
        mode="inline"
        selectedKeys={[selectedKey]}
        onClick={handleClick}
        items={items.map((item) => ({
          ...item,
          style: {
            color: selectedKey === item.key ? "#F8FAFC" : "inherit",
            backgroundColor:
              selectedKey === item.key ? "#7C3AED" : "transparent",
          },
        }))}
        style={{ borderRight: "none", flexGrow: 1 }}
      />

      {/* Кнопка выхода */}
      <div
        style={{
          textAlign: "center",
          padding: "0 16px",
          position: "absolute",
          bottom: "100px", // 🔼 Поднимаем на 100px от низа
          left: 0,
          width: "80%",
        }}
      >
        <Button
          type="primary"
          danger
          icon={<LogoutOutlined />}
          onClick={handleLogout}
          block
          style={{
            transition: "all 0.2s ease-in-out",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.transform = "translateY(-2px)")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.transform = "translateY(0)")
          }
        >
          Выйти
        </Button>
      </div>
    </div>
  );
}
