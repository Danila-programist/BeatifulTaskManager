import { useNavigate } from "react-router-dom";

export default function BackLink({ to = "/auth", text = "Назад" }) {
  const navigate = useNavigate();

  return (
    <p
      onClick={() => navigate(to)}
      className="text-center text-grayish text-sm mt-2 cursor-pointer hover:underline"
      style={{ color: "#9CA3AF" }}
    >
      {text}
    </p>
  );
}
