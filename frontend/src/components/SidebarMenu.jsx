import React, { useState } from "react";
import { Menu } from "antd";
import {
  UserOutlined,
  UnorderedListOutlined,
  CheckCircleOutlined,
  AppstoreOutlined,
} from "@ant-design/icons";

export default function SidebarMenu({ onSelect }) {
  const [selectedKey, setSelectedKey] = useState("all"); 

  const items = [
    { key: "about", icon: <UserOutlined />, label: "Обо мне" },
    { key: "all", icon: <AppstoreOutlined />, label: "Все задачи" },
    { key: "current", icon: <UnorderedListOutlined />, label: "Текущие задачи" },
    { key: "completed", icon: <CheckCircleOutlined />, label: "Выполненные задачи" },
  ];

  const handleClick = (e) => {
    setSelectedKey(e.key);
    if (onSelect) onSelect(e.key);
  };

  return (
    <Menu
      style={{
        width: 200,
        minHeight: "calc(100vh - 80px)",
        backgroundColor: "#F8FAFC", 
      }}
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
    />
  );
}
