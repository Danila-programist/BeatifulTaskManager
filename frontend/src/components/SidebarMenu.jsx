import { useState } from "react";
import { Menu, Button, message } from "antd";
import { UserOutlined, AppstoreOutlined, LogoutOutlined } from "@ant-design/icons";
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

  const handleLogout = async () => {
    try {
      await axios.post("/api/v1/auth/logout", {}, { withCredentials: true });
      message.success("Вы успешно вышли из аккаунта");
      navigate("/");
    } catch (error) {
      console.error("Ошибка при выходе:", error);
      message.error("Не удалось выйти из аккаунта");
    }
  };

  return (
    <div
      className="flex flex-col w-52 bg-light p-4"
      style={{ minHeight: "80vh" }}
    >
      {/* Меню */}
      <Menu
        mode="inline"
        selectedKeys={[selectedKey]}
        onClick={handleClick}
        items={items.map((item) => ({
          ...item,
          style: {
            color: selectedKey === item.key ? "#F8FAFC" : "inherit",
            backgroundColor: selectedKey === item.key ? "#7C3AED" : "transparent",
          },
        }))}
        style={{ borderRight: "none", flexGrow: 1 }}
      />

      {/* Кнопка выхода */}
      <Button
        type="primary"
        danger
        icon={<LogoutOutlined />}
        onClick={handleLogout}
        block
        className="mt-auto transition-all duration-200"
        onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-2px)")}
        onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0)")}
      >
        Выйти
      </Button>
    </div>
  );
}
