import { useEffect, useState } from "react";

import { getRooms, Room } from "../api";

export function Rooms() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getRooms()
      .then(setRooms)
      .catch((e: Error) => setError(e.message));
  }, []);

  return (
    <>
      <h2>Rooms</h2>
      {error && <p className="error">Could not load rooms: {error}</p>}
      <div className="grid">
        {rooms.map((room) => (
          <article key={room.id} className="card">
            <h3>{room.name}</h3>
            <p className="theme">{room.theme}</p>
            <p>
              {room.minPartySize}–{room.maxPartySize} players ·{" "}
              {room.durationMinutes} min
            </p>
          </article>
        ))}
      </div>
    </>
  );
}
