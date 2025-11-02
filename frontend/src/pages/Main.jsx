import { useState } from "react";
import Header from "../components/Header.jsx";
import SidebarMenu from "../components/SidebarMenu.jsx";

export default function Main() {
  const [activeTab, setActiveTab] = useState("about");

  const renderContent = () => {
    switch (activeTab) {
      case "about":
        return <div>Информация обо мне</div>;
      case "current":
        return <div>Текущие задачи</div>;
      case "completed":
        return <div>Выполненные задачи</div>;
      default:
        return null;
    }
  };

  return (
    <div className="bg-light min-h-screen">
      <Header />
      <div className="flex">
        <SidebarMenu onSelect={setActiveTab} />
        <div className="flex-1 p-8">{renderContent()}</div>
      </div>
    </div>
  );
}
