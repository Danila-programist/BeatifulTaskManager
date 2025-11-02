import { Button, Flex } from "antd";
import { useNavigate } from "react-router-dom";

export default function HomeButton() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/auth"); 
  };

  return (
    <Flex gap="small" justify="center">
      <Button
        onClick={handleClick}
        className="bg-accent border-none shadow-md px-6 py-2 rounded-lg transition-colors duration-200 text-light"
        onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#1E1E1E")}
        onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#7C3AED")}
        style={{ color: "#F8FAFC" }} 
      >
        Начать работу
      </Button>
    </Flex>
  );
}
