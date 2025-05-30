import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import 'leaflet/dist/leaflet.css';

const customIcon = new L.Icon({
  iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

function FlyToLocation({ lat, lon }) {
  const map = useMap();
  useEffect(() => {
    if (lat && lon) {
      console.log("📍 Flying to:", lat, lon);
      map.flyTo([lat, lon], 15); 
    }
  }, [lat, lon, map]);
  return null;
}

function App() {
  const [people, setPeople] = useState({});
  const [lastPosition, setLastPosition] = useState(null);

  useEffect(() => {
    console.log("🚀 App loaded");

    function connectWebSocket() {
      const ws = new WebSocket("ws://localhost:8000/ws/positions");

      ws.onopen = () => {
        console.log("✅ WebSocket connected");
      };

      ws.onerror = (err) => {
        console.error("❌ WebSocket error:", err);
      };

      ws.onclose = () => {
        console.log("🔌 WebSocket closed, retrying in 1s...");
        setTimeout(() => connectWebSocket(), 1000);
      };

      ws.onmessage = (event) => {
        console.log("📨 Received:", event.data);
        const person = JSON.parse(event.data);
        setPeople(prev => ({
          ...prev,
          [person.id]: person
        }));
        setLastPosition({ lat: person.lat, lon: person.lon });
      };
    }

    connectWebSocket();
  }, []);

  return (
    <MapContainer center={[50.06, 19.94]} zoom={13} style={{ height: "100vh", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {lastPosition && <FlyToLocation lat={lastPosition.lat} lon={lastPosition.lon} />}
      {Object.values(people).map(p => (
        <Marker key={p.id} position={[p.lat, p.lon]} icon={customIcon}>
          <Popup>{p.first_name} {p.last_name}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default App;
