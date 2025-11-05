const PasswordCard = ({ service, username, onView, onEdit, onDelete }) => {
  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow-md flex flex-col gap-2 hover:bg-gray-700 transition">
      <h3 className="text-lg font-semibold">{service}</h3>
      <p className="text-sm text-gray-400">{username}</p>
      <div className="flex gap-2 mt-2">
        <button onClick={onView} className="text-blue-400 hover:text-blue-500">Ver</button>
        <button onClick={onEdit} className="text-green-400 hover:text-green-500">Editar</button>
        <button onClick={onDelete} className="text-red-400 hover:text-red-500">Eliminar</button>
      </div>
    </div>
  );
};

export default PasswordCard;
