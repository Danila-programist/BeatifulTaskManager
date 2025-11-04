import { useState } from "react";
import Header from "../components/Header.jsx";
import SidebarMenu from "../components/SidebarMenu.jsx";
import TasksList from "../components/TaskList.jsx";
import UserProfile from "../components/UserProfile.jsx";
import AddTaskButton from "../components/AddTaskButton.jsx";

export default function Main() {
  const [activeTab, setActiveTab] = useState("all");
  const [tasksUpdated, setTasksUpdated] = useState(false); // чтобы TasksList перерендерился

  const renderContent = () => {
    switch (activeTab) {
      case "about":
        return <UserProfile />;
      case "all":
        return <TasksList key={tasksUpdated} />; // перерендер при добавлении
      default:
        return null;
    }
  };

  return (
    <div className="bg-light min-h-screen">
      <Header />
      <div className="flex">
        <SidebarMenu onSelect={setActiveTab} />
        <div className="flex-1 p-8">
          {renderContent()}
          {activeTab === "all" && (
            <AddTaskButton onTaskAdded={() => setTasksUpdated((prev) => !prev)} />
          )}
        </div>
      </div>
    </div>
  );
}
